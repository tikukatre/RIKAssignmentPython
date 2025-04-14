from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CompanyOwner(db.Model):
    __tablename__ = 'company_owner'
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), primary_key=True)
    share_amount = db.Column(db.Integer, nullable=False) # osaniku osa suurus kogukapitalist
    role = db.Column(db.String(20), nullable=False)  # asutaja või mitte

    # Andmebaasi seosed
    company = db.relationship('Company', back_populates='company_owners')
    owner = db.relationship('Owner', back_populates='company_owners')


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Osaühingu nimi
    register_number = db.Column(db.String(7), nullable=True) # Registrikood
    date_founded = db.Column(db.Date, nullable=True) # Asutamiskuupäev
    capital_size = db.Column(db.Integer, nullable=True) # Kogukapital

    company_owners = db.relationship('CompanyOwner', back_populates='company', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Company {self.name}>'


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # Juriidiline isik või füüsiline isik
    name = db.Column(db.String(100), nullable=False) # Nimi
    surname = db.Column(db.String(100), nullable=True)  # Perekonnanimi (füüsilise isiku puhul)
    id_number = db.Column(db.String(50), nullable=True) # Isikukood (füüsilise isiku puhul)
    register_number = db.Column(db.String(7), nullable=True) # Registrikood (juriidilise isiku puhul)

    company_owners = db.relationship('CompanyOwner', back_populates='owner', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Owner {self.name} ({self.type})>"
