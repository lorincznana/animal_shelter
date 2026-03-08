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

        db.session.add(laszlo_user)
        db.session.commit()


        mariann = Animal(
            name="Mariann",
            species="macska",
            breed="Sziámi keverék",
            age=8,
            gender="nőstény",
            description="Hipoallergán cica, allergiásoknak ideális kisállat lehet.",
            image_url="https://images.pexels.com/photos/545560/pexels-photo-545560.jpeg?_gl=1*s2j1i1*_ga*NTA1NjY0Njg0LjE3NzE2MDg0NTU.*_ga_8JE65Q40S6*czE3NzIyODc0OTYkbzEyJGcxJHQxNzcyMjg3NTQ0JGoxMiRsMCRoMA..",
            medical_records=[
                MedicalRecord(
                    vaccine="Macska triász",
                    vaccine_date=date(2024, 3, 15),
                    disease=None,
                    treatment=None,
                    chipped = True,
                    castrated = True,
                    vet_name="Dr. Kiss Péter",
                    updated_at=datetime.now()
                )
            ]
        )
        db.session.add(mariann)
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
                    chipped=True,
                    castrated = False,
                    vet_name="Dr. Kiss Péter",
                    updated_at=datetime.now()
                )
            ]
        )
        db.session.add(bodri)
        db.session.commit()

        margareta = Animal(
            name="Margaréta",
            species="kutya",
            breed="Golden retriever mix",
            age=5,
            gender="szuka",
            description="Családbarát, kis mozgásigényű kutyus, ideális akár lakásba is.",
            image_url="https://images.pexels.com/photos/35867207/pexels-photo-35867207.jpeg?_gl=1*1h9di20*_ga*NTA1NjY0Njg0LjE3NzE2MDg0NTU.*_ga_8JE65Q40S6*czE3NzE2ODEzMzIkbzQkZzEkdDE3NzE2ODEzNDIkajUwJGwwJGgw",
            medical_records=[
                MedicalRecord(
                    vaccine="Veszettség elleni oltás",
                    vaccine_date=date(2026, 1, 3),
                    disease=None,
                    treatment=None,
                    chipped=False,
                    castrated=False,
                    vet_name="Dr. Kiss Péter",
                    updated_at=datetime.now()
                )
            ]
        )
        db.session.add(margareta)
        db.session.commit()


        marcsiGallery = Gallery(
            animal_id = mariann.id,
            image_url = mariann.image_url
        )
        db.session.add(marcsiGallery)
        db.session.commit()

        bodriGallery = Gallery(
            animal_id = bodri.id,
            image_url = bodri.image_url
        )
        db.session.add(bodriGallery)
        db.session.commit()





