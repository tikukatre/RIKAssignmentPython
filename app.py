from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, Company, Owner, CompanyOwner
from forms import CompanyForm
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, func
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

#Avaleht ja osaühingute otsing
@app.route('/')
def home():
    #Osaühingute otsing
    query = request.args.get('q', '')
    if query:
        like_query = f"%{query}%"

        companies = (
            Company.query
            .outerjoin(CompanyOwner)
            .outerjoin(Owner)
            .options(joinedload(Company.company_owners).joinedload(CompanyOwner.owner))
            .filter(
                or_(
                    func.lower(Company.name).like(func.lower(like_query)),
                    Company.register_number.ilike(like_query),
                    func.lower(Owner.name).like(func.lower(like_query)),
                    func.lower(Owner.surname).like(func.lower(like_query)),
                    Owner.id_number.ilike(like_query),
                    Owner.register_number.ilike(like_query)
                )
            )
            .distinct()
            .all()
        )
    else:
        companies = Company.query.all()
    return render_template('home.html', companies=companies, query=query)

# Osaühingu loomise vorm
@app.route('/create/company', methods=['GET', 'POST'])
def create_company():
    form = CompanyForm()
    
    error = None
    # Valitud osanike salvestamine sessiooni
    selected_owner_ids = session.get('selected_owners', [])
    selected_owners = Owner.query.filter(Owner.id.in_(selected_owner_ids)).all()

    form_data = {}
    for key in request.form.keys():
        form_data[key] = request.form.get(key)

    # TODO:Vormi andmete hoiustamine ja sisestamine, et teatud olukordades ei peaks uuesti sisestama
    for key in ['name', 'register_number', 'date_founded', 'capital_size']:
        if f'form_{key}' in session:
            form_data[key] = session.pop(f'form_{key}')

    if form.validate_on_submit():
        try:
            #Osaühingu loomine
            company = Company(
                name=form.name.data,
                register_number=form.register_number.data,
                date_founded=datetime.strptime(request.form['date_founded'], "%Y-%m-%d").date(),
                capital_size=form.capital_size.data
            )
            db.session.add(company)
            db.session.flush()

            #Osanike osa suuruse summa
            total_shares = 0

            # Andmebaasis olemas olevate isikute lisamine osanikeks
            for owner in selected_owners:
                field_name = f"share_amount_owner_{owner.id}"
                share = int(request.form.get(field_name, 0))
                #Lisame osaniku osa suuruse summasse
                total_shares += share
                company.company_owners.append(
                    CompanyOwner(owner=owner, share_amount=share, role="founder")
                )

            # Uute isikute lisamine
            new_names = request.form.getlist('new_owner_name[]')
            new_types = request.form.getlist('new_owner_type[]')
            new_surnames = request.form.getlist('new_owner_surname[]')
            new_ids = request.form.getlist('new_owner_id_number[]')
            new_regs = request.form.getlist('new_owner_register_number[]')
            new_shares = request.form.getlist('new_owner_share_amount[]')
 
            for i in range(len(new_names)):
                if not new_names[i].strip() or not new_shares[i].strip():
                    continue  # Kui uusi osanikke pole, siis jätame vahele
               
                owner_type = new_types[i]

                if owner_type == 'person':
                    if not new_surnames[i].strip() or not new_ids[i].strip():
                        raise ValueError("Isikul peab olema ees- ja perekonnanimi ning isikukood.")
                elif owner_type == 'legal_entity':
                    if not new_regs[i].strip():
                        raise ValueError("Juriidilisel isikul peab olema registrikood.")

                share = int(new_shares[i])
                total_shares += share
                print(f"Total Shares: {total_shares}, Capital Size: {company.capital_size}")
                owner = Owner(
                    type=owner_type,
                    name=new_names[i],
                    surname=new_surnames[i] if owner_type == 'person' else None,
                    id_number=new_ids[i] if owner_type == 'person' else None,
                    register_number=new_regs[i] if owner_type == 'legal_entity' else None
                )
                db.session.add(owner)
                db.session.flush()  

                company.company_owners.append(
                    CompanyOwner(owner=owner, share_amount=share, role="founder")
                )

            # Kontrollime, et osade summa võrdub põhikapitaliga
            if total_shares != company.capital_size:
                db.session.rollback()
                error = f"Osanike osalus ({total_shares}) peab võrduma kogukapitali summaga ({company.capital_size})."
                print(error)
                raise ValueError(error)

            if not company.company_owners:
                db.session.rollback()
                error = "Osaühingul peab olema vähemalt üks osanik."
                print(error)
                raise ValueError(error)

            db.session.commit()
            session.pop('selected_owners', None)
            for key in list(session.keys()):
                if key.startswith("form_"):
                    session.pop(key)
                
            return redirect(url_for('home'))

        except Exception as e:
            db.session.rollback()
            error = str(e)
            print(error)
            return render_template(
                'create_company.html',
                form=form,
                form_data=form_data,
                search_results=search_results,
                selected_owners=selected_owners,
                current_date=datetime.now().date(),
                error=error,
            )
        

    # Osanike otsing
    query = request.args.get('q')
    search_results = []
    if query:
        search_results = Owner.query.filter(Owner.name.ilike(f"%{query}%")).all()

    return render_template(
        'create_company.html',
        form=form,
        form_data=form_data,
        search_results=search_results,
        selected_owners=selected_owners,
        current_date=datetime.now().date(),
        error=error,
    )

# Osaühingu andmete vaade
@app.route('/company/<int:company_id>')
def company_detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company_detail.html', company=company)

#Olemasoleva isiku osanikuks lisamine
@app.route('/add_owner/<int:owner_id>')
def add_owner(owner_id):
    selected = session.get('selected_owners', [])
    if owner_id not in selected:
        selected.append(owner_id)
    session['selected_owners'] = selected

    return redirect(url_for('create_company'))

#Olemasoleva isiku eemaldamine osanikest
@app.route('/remove_owner/<int:owner_id>')
def remove_owner(owner_id):
    selected = session.get('selected_owners', [])
    if owner_id in selected:
        selected.remove(owner_id)
    session['selected_owners'] = selected
    return redirect(url_for('create_company'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
