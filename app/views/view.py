# Imports que son nativos de Python
import os
from datetime import timedelta
# Imports que son nativos del Framework y Librerias
from app import app, db, jwt
from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    flash,
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy import ForeignKey
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    )
from marshmallow.exceptions import ValidationError
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
# Imports de variables generadas por nosotros
from app.models.models import (
    Publicacion,
    Comentario,
    Tema,
    Usuario,
)
from app.schemas.schema import (
    userSchema,
    publicacionSchema,
    publicacionBasicSchema,
    temaSchema,
    comentarioSchema,
    comentarioBasicSchema,
)
from random import *
from datetime import datetime, timedelta
from flask.views import MethodView

# ----------- Endpoint Usuarios -----------

class UsuarioAPI(MethodView):
    # Trae usuarios    
    def get(self, user_id=None):
        
        # si no se proporciona ninguna id se trae todo
        if user_id is None:
            usuarios = Usuario.query.all()
            resultado = userSchema().dump(usuarios, many=True)
            return jsonify(resultado), 200
        
        # si se proporciona una id, la busca
        user = Usuario.query.get(user_id)
        
        # si no existe devuelve este error
        if user is None:
            return jsonify(USER_NOT_FOUND=f"user with id {user_id} not found"), 404
        
        # a este punto se llega solo si se proporciono un id que exista
        resultado = userSchema().dump(user)
        return jsonify(resultado), 200
    
    # Crea usuarios
    def post(self):
        # se podria separar en 2 try's, pero creo que se entiende
        try:
            # recuper los datos de la request
            user_json = userSchema().load(request.json) 
            nombre = user_json.get('nombre')
            email = user_json.get('email')
            password = user_json.get('password')

            # los intenta cargar a la base de datos
            nuevo_usuario = Usuario(
                nombre=nombre,
                email=email,
                password=password
            )

            db.session.add(nuevo_usuario)
            db.session.commit()
            # si todo salio bien los carga y devuelve lo que se cargo
            return jsonify(AGREGADO=userSchema().dump(user_json)) 
        
        # Puede haber 2 tipos de error, con la serializacion o con la base de datos
        except (ValidationError, IntegrityError) as err:
            # por si es con la serializacion
            if isinstance (err, ValidationError): 
                return jsonify(ERROR=err.messages), 400
            # por si es con la base de datos
            elif isinstance (err, IntegrityError):
                # hace un rollback, por las dudas
                db.session.rollback()
                return jsonify(ERROR=str(err)), 409
    
    # Actualiza nombres de usuario
    def put(self, user_id):
        # este try si lo separe en 2
        try:
            # busca un usuario con el id proporcionado
            user = Usuario.query.filter_by(id=user_id).one()
        except:
            # si no lo encuentra devuelve que no lo encontro
            return jsonify(ERROR=f"user with id {user_id} not found")  

        # si existe el usuario, verifica que la request sea valida tambien
        try:
            user_json = userSchema().load(request.json) 
            nombre = user_json.get('nombre')
        except ValidationError as err:
            return jsonify(ERROR=err.messages)  
        
        # si pasa todas las validaciones, cambia el nombre
        user.nombre = nombre
        db.session.commit()

        # y muestra al usuario ya modificado
        return jsonify(MODIFICADO=userSchema().dump(user))  
    
    # Borra usuarios
    def delete(self, user_id):
        # verifica que exista el usuario
        try:
            user = Usuario.query.filter_by(id=user_id).one()
        except:
            return jsonify(ERROR=f"user with id {user_id} not found")
        
       # borra todos los comentarios hechos por el usuario que se esta borrando
        Comentario.query.filter_by(usuario_id=user_id).delete()
        Publicacion.query.filter_by(usuario_id=user_id).delete()
        
        # borra el usuario
        db.session.delete(user)
        db.session.commit()
        return jsonify(USUARIO_ELIMINADO=userSchema().dump(user))

app.add_url_rule('/user', view_func=UsuarioAPI.as_view('usuario'))
app.add_url_rule('/user/<user_id>', view_func=UsuarioAPI.as_view('usuario_id'))

# ----------- Endpoint Publicaciones -----------

class PublicacionAPI(MethodView):
    # Trae publicaciones    
    def get(self, publicacion_id=None):
        # trae todo si no se proporciona id
        if publicacion_id is None:
            usuarios = Publicacion.query.all()
            resultado = publicacionSchema().dump(usuarios, many=True)
            return jsonify(resultado), 200

        
        # intenta buscar el id proporcionado 
        user = Publicacion.query.get(publicacion_id)

        # si el id que ingreso el usuario no existe entra al if
        if user is None:
            resultado = f"publication with id {publicacion_id} not found"
            return jsonify(PUBLICATION_NOT_FOUND=resultado), 404

        resultado = publicacionSchema().dump(user)
        return jsonify(resultado), 200
    
    # Crea publicaciones
    def post(self):
        # valida la serializacion
        try:
            publicacion_json = publicacionBasicSchema().load(request.json) 
            descripcion = publicacion_json.get('descripcion')
            tema_id = publicacion_json.get('tema_id')
            usuario_id = publicacion_json.get('usuario_id')
        
        except ValidationError as err:
            return jsonify(ERROR=err.messages), 400
        
        # valida la carga de datos
        try:
            nuevo_comentario = Publicacion (
                descripcion=descripcion,
                tema_id=tema_id,
                usuario_id=usuario_id,
            )
            db.session.add(nuevo_comentario)
            db.session.commit()

        except IntegrityError as err:
            db.session.rollback()
            return jsonify(ERROR=str(err)), 409

        # si todo esta OK ya se creo la publicacion y se muestra el dump
        return jsonify(AGREGADO=publicacionBasicSchema().dump(publicacion_json)), 201
    
    # Borra publicaciones
    def delete(self, publicacion_id):
        try:
            publicacion = Publicacion.query.filter_by(id=publicacion_id).one()
        except:
            return jsonify(ERROR=f"publication with id {publicacion_id} not found"), 404
        
        # si se borra la publicacion tambien se borrar sus comentarios
        Comentario.query.filter_by(publicacion_id=publicacion_id).delete()
            
        # se borra la publicacion
        db.session.delete(publicacion)
        db.session.commit()
        return jsonify(PUBLICACION_ELIMINADA=comentarioBasicSchema().dump(publicacion))

app.add_url_rule('/publicaciones', view_func=PublicacionAPI.as_view('publicaciones'))
app.add_url_rule('/publicaciones/<publicacion_id>', view_func=PublicacionAPI.as_view('publicacion_id'))

# ----------- Endpoint Temas -----------

class TemaAPI(MethodView):
    # Trae Temas
    def get(self, tema_id=None):
        # si no se proporciona tema_id
        if tema_id is None:
            temas = Tema.query.all()
            resultado = temaSchema().dump(temas, many=True)
            return jsonify(resultado)

        # busca tema_id en la tabla Tema
        tema = Tema.query.get(tema_id)

        # si no lo encuentra devuelve este error
        if tema is None:
            return jsonify(ERROR=f"theme with id {tema_id} not found"), 404

        # si se proporciono tema_id y se encontro el tema
        resultado = temaSchema().dump(tema)
        return jsonify(resultado)
    
    # Crea Temas
    def post(self):
        tema_json = temaSchema().load(request.json) 
        tema = tema_json.get('nombre')

        nuevo_tema = Tema(
            nombre=tema,
        )

        db.session.add(nuevo_tema)
        db.session.commit()

        return jsonify(AGREGADO=temaSchema().dump(tema_json))
        
    # Borra Temas
    def delete(self, tema_id):
        tema = Tema.query.get(tema_id)
        db.session.delete(tema)
        db.session.commit()
        return jsonify(TEMA_ELIMINADO=temaSchema().dump(tema))

app.add_url_rule('/temas', view_func=TemaAPI.as_view('temas'))
app.add_url_rule('/temas/<tema_id>', view_func=TemaAPI.as_view('tema_id'))

# ----------- Endpoint Comentarios -----------

class ComentarioAPI(MethodView):
    def get(self, comentario_id=None):
        if comentario_id is None:
            comentarios = Comentario.query.all()
            resultado = comentarioSchema().dump(comentarios, many=True)
        else:
            comentario = Comentario.query.get(comentario_id)
            resultado = comentarioSchema().dump(comentario)
        return jsonify(resultado)

    def post(self):
        comentario_json = comentarioBasicSchema().load(request.json)
        descripcion = comentario_json.get("descripcion")
        publicacion_id = comentario_json.get("publicacion_id")
        usuario_id = comentario_json.get("usuario_id")

        nuevo_comentario = Comentario(
            descripcion=descripcion,
            publicacion_id=publicacion_id,
            usuario_id=usuario_id,
        )

        db.session.add(nuevo_comentario)
        db.session.commit()
        return jsonify(AGREGADO=comentarioSchema().dump(comentario_json))
    
    def delete(self, comentario_id):
        comentario = Comentario.query.get(comentario_id)
        db.session.delete(comentario)
        db.session.commit()
        return jsonify(ELIMINADO=comentarioBasicSchema().dump(comentario))

app.add_url_rule('/comentarios', view_func=ComentarioAPI.as_view('comentarios'))
app.add_url_rule('/comentarios/<comentario_id>', view_func=ComentarioAPI.as_view('comentario_id'))

# ----------- Endpoint Raiz (? -----------

@app.route('/')
def index():
    return '<h1>Index</h1>'
