from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from loguru import logger

class USERS(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(64), unique=False)
    password_hash = db.Column(db.String(128))
    geolocation = db.Column(db.VARCHAR(1024))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        logger.debug(self.password_hash, password)
        return check_password_hash(self.password_hash, password)

    def add_geo(self, data):
        self.geolocation = data
        db.session.commit()

    def __repr__(self):
        return f'name {self.name}\npasswd {self.password_hash}\n geo {self.geolocation}\n'

class STATUS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_result = db.Column(db.String(256))
    сontact_with_infected = db.Column(db.String(256))
    Symptoms = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'))

    def edit_test_result(self,data):
        self.test_result = data
        db.session.commit()

    def edit_сontact_with_infected(self,data):
        self.сontact_with_infected = data
        db.session.commit()

    def edit_symptoms(self,data):
        self.Symptoms = data
        db.session.commit()

    def __repr__(self):
        return f'test_result {self.test_result}\nсontact_with_infected {self.сontact_with_infected}\n geo {self.Symptoms}\n'

class BUFFER_PEOPLE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    geolocation = db.Column(db.String(256))
    type_of_public = db.Column(db.String(256))

    def edit_geolocation(self,data):
        self.geolocation = data
        db.session.commit()

    def edit_type_of_public(self,data):
        self.type_of_public = data
        db.session.commit()

    def __repr__(self):
        return f'id: {self.id}\ngeolocation: {self.geolocation}\n type_of_public: {self.type_of_public}\n'

class VISITED_PLACES(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    lat = db.Column(db.VARCHAR(256))
    lon = db.Column(db.VARCHAR(256))
    type_of_public = db.Column(db.String(256))

    def edit_lat(self, data):
        self.lat = data
        db.session.commit()

    def edit_lon(self, data):
        self.lon = data
        db.session.commit()

    def edit_type_of_public(self, data):
        self.type_of_public = data
        db.session.commit()

    def __repr__(self):
        return f'id: {self.id}\nplaces: {self.places}\n'


@login.user_loader
def load_user(id):
    return USERS.query.get(int(id))