from flask_sqlalchemy import SQLAlchemy

from app import app, db
from models import User, Animal, MedicalRecord, Gallery, ShelterInfo
from datetime import datetime, timedelta, date

from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        shelter = ShelterInfo(
            name="Remény Állatotthon",
            address="1234 Budapest, Kitaláció utca 5.",
            phone="+36 30 123 4567",
            email="info@remenyallatotthon.hu",
            description="Remény Állatotthon szeretettel gondozza az elhagyott állatokat, és segíti őket új otthonhoz.",
            donation_text="Támogass minket adód 1%-ával vagy önkéntes munkával!",
            donation_account="12345678-00000000-87654321"
        )
        db.session.add(shelter)

        admin_user = User(
            username="admin",
            email="admin",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()

        laszlo_user = User(
            username = "kutyaslaci",
            email = "kutyas@dr.hu",
            password = generate_password_hash("kutyaslaci61"),
            role = "user",
            created_at = date(2015, 1, 1),
        )



        marcsi = Animal(
            name="Marcsi",
            species="macska",
            breed="Európai házimacska",
            age=8,
            gender="nőstény",
            description="Első örökbefogadott kisállatunk.",
            image_url="https://images.pexels.com/photos/27616905/pexels-photo-27616905.jpeg?_gl=1*1f73vbq*_ga*MjI3MTY3MTM3LjE3NTQ5MzQ2OTI.*_ga_8JE65Q40S6*czE3NjExNDDI0MzYkbzE1JGcwJHQxNzYxMTQyNDM2JGo2MCRsMCRoMA..",
            medical_records=[
                MedicalRecord(
                    vaccine="Macska triász",
                    vaccine_date=date(2024, 3, 15),
                    disease=None,
                    treatment=None,
                    vet_name="Dr. Kiss Péter",
                    updated_at=datetime.now()
                )
            ]
        )
        db.session.add(marcsi)
        db.session.commit()

        bodri = Animal(
            name="Bodri",
            species="kutya",
            breed="Border collie",
            age=7,
            gender="kan",
            description="Nagy mozgásigényű kutyus, barátságos.",
            image_url="https://images.pexels.com/photos/1124002/pexels-photo-1124002.jpeg?_gl=1*1bnvjf*_ga*NTA1NjY0Njg0LjE3NzE2MDg0NTU.*_ga_8JE65Q40S6*czE3NzE2MTM1NTgkbzIkZzAkdDE3NzE2MTM1NTgkajYwJGwwJGgw",
            medical_records=[
                MedicalRecord(
                    vaccine="Veszettség elleni oltás",
                    vaccine_date=date(2024, 3, 15),
                    disease=None,
                    treatment=None,
                    vet_name="Dr. Kiss Péter",
                    updated_at=datetime.now()
                )
            ]
        )
        db.session.add(bodri)
        db.session.commit()


        marcsiGallery = Gallery(
            animal_id = marcsi.id,
            image_url = marcsi.image_url
        )
        db.session.add(marcsiGallery)
        db.session.commit()

        bodriGallery = Gallery(
            animal_id = bodri.id,
            image_url = bodri.image_url
        )
        db.session.add(bodriGallery)
        db.session.commit()





