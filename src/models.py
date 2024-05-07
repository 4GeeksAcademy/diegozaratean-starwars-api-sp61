from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "esta_vivo": self.is_active,
            "calificacion": 10,
            # do not serialize the password, its a security breach
        }

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    ciudad = db.Column(db.String(250), nullable=False)
    slogan = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Enterprise %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "slogan": self.slogan,
            # do not serialize the password, its a security breach
        }