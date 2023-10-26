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
)
from random import *
from datetime import datetime, timedelta
from flask.views import MethodView

class UsuarioAPI(MethodView):
    # Trae usuarios    
    def get(self, user_id=None):
        if user_id is None:
            usuarios = Usuario.query.all()
            resultado = userSchema().dump(usuarios, many=True)
        else:
            user = Usuario.query.get(user_id)
            resultado = userSchema().dump(user)
        return jsonify(resultado)
    
    # Crea usuarios
    def post(self):
        print('entro al post')
        # try:
        user_json = userSchema().load(request.json) 
        nombre = user_json.get('nombre')
        email = user_json.get('email')
        password = user_json.get('password')

        # le asigna una foto random al perfil
        numero_random = randint(1,40)
        perfil = f'gato{numero_random}.png'

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=password,
            perfil=perfil
        ) 

        db.session.add(nuevo_usuario)
        db.session.commit()
        # except:
        #     return jsonify(ERROR = "Ya existe una cuenta con este email.")

        return jsonify(AGREGADO=userSchema().dump(user_json)) 
    
    # Actualiza nombres de usuario
    def put(self, user_id):
        user = Usuario.query.get(user_id)
        user_json = userSchema().load(request.json) 
        nombre = user_json.get('nombre')
        user.nombre = nombre
        db.session.commit()
        return jsonify(MODIFICADO=userSchema().dump(user))  
    
    # Borra usuarios
    def delete(self, user_id):
        user = Usuario.query.get(user_id)

        if user:
            publicaciones_relacionadas = (Publicacion.query.
                                        filter_by(usuario_id=user_id)
                                        .all()
                                    )
            comentarios_relacionados = (Comentario.query.
                                        filter_by(usuario_id=user_id)
                                        .all()
                                    )
            
            for comentario in comentarios_relacionados:
                db.session.delete(comentario)

            for publicacion in publicaciones_relacionadas:
                tema = publicacion.tema
                comentarios_asociados = (Comentario.query
                            .filter_by(id_publicacion=publicacion.id)
                            .all()
                        )
                for comentario_asociado in comentarios_asociados:
                    db.session.delete(comentario_asociado)
                
                db.session.delete(publicacion)
                
                if (
                    db.session.query(Publicacion)
                    .filter_by(tema_id=tema.id)
                    .count() == 0
                ):
                    db.session.delete(tema)

        db.session.delete(user)
        db.session.commit()
        return jsonify(ELIMINADO={userSchema().dump(user)}) 
app.add_url_rule('/user', view_func=UsuarioAPI.as_view('usuario'))
app.add_url_rule('/user/<user_id>', view_func=UsuarioAPI.as_view('usuario_por_id'))


class PublicacionAPI(MethodView):
    # Trae publicaciones    
    def get(self, publicacion_id=None):
        if publicacion_id is None:
            usuarios = Publicacion.query.all()
            resultado = publicacionSchema().dump(usuarios, many=True)
        else:
            user = Publicacion.query.get(publicacion_id)
            resultado = publicacionSchema().dump(user)
        return jsonify(resultado)
    
    # Crea publicaciones
    def post(self):
        # try:
        publicacion_json = publicacionSchema().load(request.json) 
        autor = publicacion_json.get('autor')
        descripcion = publicacion_json.get('descripcion')
        perfil = publicacion_json.get('perfil')
        tema = publicacion_json.get('tema')
        usuario = publicacion_json.get('usuario')
        tema_id = publicacion_json.get('tema_id')
        usuario_id = publicacion_json.get('usuario_id')

        # le asigna una foto random al perfil
        numero_random = randint(1,40)
        perfil = f'gato{numero_random}.png'

        fecha_hora = datetime.now().strftime("%H:%m")

        nuevo_comentario = Publicacion (
            autor=autor,
            descripcion=descripcion,
            perfil=perfil,
            fecha_hora=fecha_hora,
            tema=tema,
            usuario=usuario,
            tema_id=tema_id,
            usuario_id=usuario_id,
        ) 

        db.session.add(nuevo_comentario)
        db.session.commit()

        return jsonify(AGREGADO=publicacionSchema().dump(publicacion_json)) 
    
    # Borra publicaciones
    def delete(self, publicacion_id):
        user = Usuario.query.get(publicacion_id)

        if user:
            publicaciones_relacionadas = (Publicacion.query.
                                        filter_by(usuario_id=publicacion_id)
                                        .all()
                                    )
            comentarios_relacionados = (Comentario.query.
                                        filter_by(usuario_id=publicacion_id)
                                        .all()
                                    )
            
            for comentario in comentarios_relacionados:
                db.session.delete(comentario)

            for publicacion in publicaciones_relacionadas:
                tema = publicacion.tema
                comentarios_asociados = (Comentario.query
                            .filter_by(id_publicacion=publicacion.id)
                            .all()
                        )
                for comentario_asociado in comentarios_asociados:
                    db.session.delete(comentario_asociado)
                
                db.session.delete(publicacion)
                
                if (
                    db.session.query(Publicacion)
                    .filter_by(tema_id=tema.id)
                    .count() == 0
                ):
                    db.session.delete(tema)

        db.session.delete(user)
        db.session.commit()
        return jsonify(ELIMINADO={userSchema().dump(user)}) 
app.add_url_rule('/publicaciones', view_func=PublicacionAPI.as_view('publicaciones'))
app.add_url_rule('/publicacion/<user_id>', view_func=PublicacionAPI.as_view('publicacion_por_id'))

@app.route('/')
def index():
    return '<h1>Index</h1>'
