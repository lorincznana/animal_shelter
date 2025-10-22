from flask import Flask, render_template, request, redirect, url_for
from models import db

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)

#app.config['SECRET_KEY'] = 'K1c51_NYu5Z1_67$'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'library.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import Animal, MedicalRecord, Gallery, Adopter, Adoption, ShelterInfo, User

@app.route('/')
def main_page():
    return render_template('main_page.html')
@app.route('/animals', methods=['GET', 'POST'])
def list_dogs():
    animals = Animal.query.all()
    return render_template('animals.html', animals=animals)

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