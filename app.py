from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
from models import db

from werkzeug.security import generate_password_hash, check_password_hash

import os

#Ötlet a Kedvesemtől: Lehessen magyar és angol nyelvű is a weboldal.
#Én: AI chatbot

app = Flask(__name__)

app.config['SECRET_KEY'] = 'K1c51_NYu5Z1_67$'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'library.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import Animal, MedicalRecord, Gallery, ShelterInfo, User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def roles_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Jelentkezz be a továbbiakhoz.", "warning")
                return redirect(url_for('login'))
            if not current_user.role or current_user.role not in roles:
                flash("Nincs jogosultságod ehhez.", "warning")
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return decorated_func
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/')
def main_page():
    shelter_info = ShelterInfo.query.first()
    return render_template('main_page.html', shelter_info=shelter_info)

@app.route('/animals', methods=['GET'])
def list_animals():
    animals_list = Animal.query.all()
    shelter_info = ShelterInfo.query.first()

    animals_json = {}
    for animal in animals_list:
        animals_json[animal.id] = {
            'id': animal.id,
            'name': animal.name,
            'species': animal.species,
            'breed': animal.breed,
            'age': animal.age,
            'gender': animal.gender,
            'description': animal.description,
            'image_url': animal.image_url,

            'medical_records': [{
                'vaccine': mr.vaccine,
                'vaccine_date': mr.vaccine_date.isoformat() if mr.vaccine_date else None,
                'disease': mr.disease,
                'treatment': mr.treatment,
                'vet_name': mr.vet_name,
                'updated_at': mr.updated_at.isoformat() if mr.updated_at else None
            } for mr in animal.medical_records],
            'gallery': [{
                'image_url': g.image_url
            } for g in animal.gallery]
        }

    return render_template('animals.html',
                           animals=animals_list,
                           animals_json=animals_json,
                           shelter_info=shelter_info)



@app.route('/animals/add', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'staff')
def add_animal():
    if request.method == 'POST':
        age = int(request.form.get('age')) if request.form.get('age') else None

        new_animal = Animal(
            name=request.form['name'],
            species=request.form['species'],
            breed=request.form.get('breed'),
            age=age,
            gender=request.form['gender'],
            description=request.form.get('description'),
            image_url=request.form.get('image_url')
        )
        db.session.add(new_animal)
        db.session.flush()  # hogy meglegyen az ID a medical recordhoz

        vaccines      = request.form.getlist('vaccine[]')
        vaccine_dates = request.form.getlist('vaccine_date[]')
        diseases      = request.form.getlist('disease[]')
        treatments    = request.form.getlist('treatment[]')
        vet_names     = request.form.getlist('vet_name[]')

        for i in range(len(vaccines)):
            if any([vaccines[i], diseases[i], treatments[i], vet_names[i]]):
                record = MedicalRecord(
                    animal_id=new_animal.id,
                    vaccine=vaccines[i] or None,
                    vaccine_date=vaccine_dates[i] or None,
                    disease=diseases[i] or None,
                    treatment=treatments[i] or None,
                    vet_name=vet_names[i] or None,
                    updated_at=datetime.utcnow()
                )
                db.session.add(record)

        db.session.commit()
        flash("Kisállat sikeresen hozzáadva!", "success")
        return redirect(url_for('list_animals'))

    return render_template('add_animal.html')


@app.route('/animals/edit/<int:animal_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'staff')
def edit_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)

    if request.method == 'POST':
        age = int(request.form.get('age')) if request.form.get('age') else None

        animal.name        = request.form['name']
        animal.species     = request.form['species']
        animal.breed       = request.form.get('breed')
        animal.age         = age
        animal.gender      = request.form['gender']
        animal.description = request.form.get('description')
        animal.image_url   = request.form.get('image_url')

        # Régi rekordok törlése, újak mentése
        MedicalRecord.query.filter_by(animal_id=animal.id).delete()

        vaccines      = request.form.getlist('vaccine[]')
        vaccine_dates = request.form.getlist('vaccine_date[]')
        diseases      = request.form.getlist('disease[]')
        treatments    = request.form.getlist('treatment[]')
        vet_names     = request.form.getlist('vet_name[]')

        for i in range(len(vaccines)):
            if any([vaccines[i], diseases[i], treatments[i], vet_names[i]]):
                record = MedicalRecord(
                    animal_id=animal.id,
                    vaccine=vaccines[i] or None,
                    vaccine_date=vaccine_dates[i] or None,
                    disease=diseases[i] or None,
                    treatment=treatments[i] or None,
                    vet_name=vet_names[i] or None,
                    updated_at=datetime.utcnow()
                )
                db.session.add(record)

        db.session.commit()
        flash("Kisállat adatai sikeresen módosítva!", "success")
        return redirect(url_for('list_animals'))

    return render_template('edit_animal.html', animal=animal)

@app.context_processor
def inject_shelter_info():
    shelter_info = ShelterInfo.query.first()
    return dict(shelter_info=shelter_info)

@app.route('/about_page', methods=['GET', 'POST'])
def about_page():
    shelter_info = ShelterInfo.query.first()
    return render_template('about_page.html', shelter_info=shelter_info)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("A felhasználónév már foglalt.", "error")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Ezzel az email-el már regisztráltak.", "error")
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role="user"
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Sikeres regisztráció! Most jelentkezz be.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Hibás felhasználónév vagy jelszó.", "warning")
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('main_page'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)