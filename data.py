from app import app, db
from models import Company, Owner, CompanyOwner
from datetime import date

# Algandmete loomine andmebaasi
def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        tuuli = Owner(type="person", name="Tuuli", surname="Anderson", id_number="28504015789")
        peeter = Owner(type="person", name="Peeter", surname="Tamm", id_number="98705122134")
        bank = Owner(type="legal_entity", name="LegalBank Ltd", register_number="2456123")
        maria = Owner(type="person", name="Maria", surname="Tootsi", id_number="40011215432")

        db.session.add_all([tuuli,peeter, bank, maria])
        db.session.flush()

        company1 = Company(
            name="Ipsum OÜ",
            register_number="1234567",
            date_founded=date(1991, 5, 20),
            capital_size=5000
        )
        db.session.add(company1)
        db.session.flush()

        company1.company_owners.append(CompanyOwner(owner=tuuli, share_amount=2500, role="founder"))
        company1.company_owners.append(CompanyOwner(owner=bank, share_amount=2500, role="shareholder"))

     
        company2 = Company(
            name="StartupHub OÜ",
            register_number="7654321",
            date_founded=date(2020, 1, 10),
            capital_size=3000
        )
        db.session.add(company2)
        db.session.flush()

        company2.company_owners.append(CompanyOwner(owner=peeter, share_amount=3000, role="founder"))

        company3 = Company(
            name="StartupX",
            register_number="2345678",
            date_founded=date(2018, 3, 15),
            capital_size=10000
        )
        db.session.add(company3)
        db.session.flush()
        company3.company_owners.append(CompanyOwner(owner=maria, share_amount=5640, role="founder"))
        company3.company_owners.append(CompanyOwner(owner=tuuli, share_amount=4000, role="shareholder"))
        company3.company_owners.append(CompanyOwner(owner=peeter, share_amount=360, role="shareholder"))

        db.session.commit()

        print("Algandmete loomine andmebaasi õnnestus!")

if __name__ == "__main__":
    seed_data()