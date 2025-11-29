from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from models import db

from werkzeug.security import generate_password_hash, check_password_hash

import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'K1c51_NYu5Z1_67$'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'library.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import Animal, MedicalRecord, Gallery, Adopter, Adoption, ShelterInfo, User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/')
def main_page():
    shelter_info = ShelterInfo.query.first()
    return render_template('main_page.html', shelter_info=shelter_info)
@app.route('/animals', methods=['GET', 'POST'])
def list_animals():
    animals = Animal.query.all()
    return render_template('animals.html', animals=animals)

"""
@app.route('/animals/add', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        animal_name = request.form['animal_name']
        animal_species = request.form['animal_species']
        animal_breed = request.form['animal_breed']
        animal_age = request.form['animal_age']
        animal_gender = request.form['animal_gender']
        animal_description = request.form['animal_description']
        animal_image = request.form['animal_image']
        animal_available = request.form['animal_available']

        new_animal = Animal(
            animal_name=animal.name,
            animal_species=animal.species,
            animal_breed=animal_breed,
            animal_age=animal_age,
            animal_gender=animal_gender,
            animal_description=animal_description,
            animal_image=animal_image,
            animal_available=animal_available,
            animal_cre
        )
"""



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
            return "A felhasználónév már foglalt."
        if User.query.filter_by(email=email).first():
            return "Ezzel az email-el már regisztráltak."

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role="user"
        )
        db.session.add(new_user)
        db.session.commit()
        return ("Sikeres regisztráció!")
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return "Hibás felhasználónév vagy jelszó."

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



