from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Sequence


db = SQLAlchemy()
USER_ID_SEQ = Sequence('user_id_seq')

class Solicitud(db.Model):
    id = db.Column(db.Integer, USER_ID_SEQ, primary_key=True, autoincrement=True, nullable=False, server_default=USER_ID_SEQ.next_value())
    nombre = db.Column(db.String(120), unique=False, nullable=False)
    apellido = db.Column(db.String(120), unique=False, nullable=False)
    cedula = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    telefono = db.Column(db.String(120), unique=False, nullable=False)
    tipo_afiliacion = db.Column(db.String(120), unique=False, nullable=False)
    estado_afiliacion = db.Column(db.String(120), unique=False, nullable=False)
    fecha = db.Column(db.Date, unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "cedula": self.cedula,
            "email": self.email,
            "telefono": self.telefono,
            "tipo_afiliacion": self.tipo_afiliacion,
            "estado_afiliacion": self.estado_afiliacion,
            "fecha": self.fecha,

        }

class Usuarios(db.Model):
    id = db.Column(db.Integer, USER_ID_SEQ, primary_key=True, autoincrement=True, nullable=False,
                   server_default=USER_ID_SEQ.next_value())
    usuario = db.Column(db.String(120), unique=False, nullable=False)
    clave = db.Column(db.String(120), unique=False, nullable=False)
    tipo_usuario = db.Column(db.String(120), unique=False, nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "clave": self.clave,
            "tipo_usuario": self.tipo_usuario,
        }

class Planes_usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_individual = db.Column(db.Boolean, primary_key=True)
    plan_banca_asistencia = db.Column(db.Boolean, primary_key=True)
    plan_corporativo = db.Column(db.Boolean, primary_key=True)

    def serialize(self):
        return {
            "id": self.id,
            "plan_individual": self.plan_individual,
            "plan_banca_asistencia": self.plan_banca_asistencia,
            "plan_corporativo": self.plan_corporativo
        }



