from app import db
from sqlalchemy import ForeignKey
from datetime import datetime


class Publicacion(db.Model):
    __tablename__ = 'publicacion'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    descripcion = db.Column(
        db.String(100),
        nullable=False
    )

    fecha_hora = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    tema_id = db.Column(
        db.Integer,
        db.ForeignKey('tema.id')
    )

    tema = db.relationship(
        'Tema',
        backref=db.backref('tema')
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id')
    )

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('publicacion')
    )

    def __str__(self):
        return self.name

class Tema(db.Model):
    __tablename__ = 'tema'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(50),
        unique=True
    )

    def __str__(self):
        return self.name

class Comentario(db.Model):
    __tablename__ = 'comentario'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    descripcion = db.Column(
        db.String(100),
        nullable=False
    )

    publicacion_id = db.Column(
        db.Integer,
        db.ForeignKey('publicacion.id'),
        nullable=False
    )

    publicacion = db.relationship(
        'Publicacion',
        backref=db.backref('publicacion')
    )

    fecha_hora = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id'),
        nullable=False
    )    

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('comentario')
    )

    def __str__(self):
        return self.name

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    def __str__(self):
        return self.name
