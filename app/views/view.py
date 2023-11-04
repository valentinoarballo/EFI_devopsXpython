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
        if user_id is None:
            usuarios = Usuario.query.all()
            resultado = userSchema().dump(usuarios, many=True)
        else:
            user = Usuario.query.get(user_id)
            resultado = userSchema().dump(user)
        return jsonify(resultado)
    
    # Crea usuarios
    def post(self):
        # try:
        user_json = userSchema().load(request.json) 
        nombre = user_json.get('nombre')
        email = user_json.get('email')
        password = user_json.get('password')

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=password
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
            # aun no funciona YA FUNCIAAONAAA
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
                            .filter_by(publicacion_id=publicacion.id)
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
        return jsonify(USUARIO_ELIMINADO=userSchema().dump(user)) 
app.add_url_rule('/user', view_func=UsuarioAPI.as_view('usuario'))
app.add_url_rule('/user/<user_id>', view_func=UsuarioAPI.as_view('usuario_id'))

# ----------- Endpoint Publicaciones -----------

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
        publicacion_json = publicacionBasicSchema().load(request.json) 
        descripcion = publicacion_json.get('descripcion')
        tema_id = publicacion_json.get('tema_id')
        usuario_id = publicacion_json.get('usuario_id')

        # Fecha del momento en el que se crea el post
        fecha_hora = datetime.now().strftime("%H:%m")

        # Creo la nueva publicacions 
        nuevo_comentario = Publicacion (
            descripcion=descripcion,
            tema_id=tema_id,
            usuario_id=usuario_id,
        ) 

        # Subo el nuevo usuario a la base de datos
        db.session.add(nuevo_comentario)
        db.session.commit()

        return jsonify(AGREGADO=publicacionBasicSchema().dump(publicacion_json)) 
    
    # Borra publicaciones
    def delete(self, publicacion_id):
        publicacion = Publicacion.query.get(publicacion_id)

        if publicacion:
            
            comentarios_relacionados = (Comentario.query.
                                        filter_by(publicacion_id=publicacion_id)
                                        .all()
                                    )
            
            for comentario in comentarios_relacionados:
                db.session.delete(comentario)
            
        db.session.delete(publicacion)
        db.session.commit()
        return jsonify(PUBLICACION_ELIMINADA=comentarioBasicSchema().dump(publicacion))
app.add_url_rule('/publicaciones', view_func=PublicacionAPI.as_view('publicaciones'))
app.add_url_rule('/publicaciones/<publicacion_id>', view_func=PublicacionAPI.as_view('publicacion_id'))

# ----------- Endpoint Temas -----------

class TemaAPI(MethodView):
    def get(self, tema_id=None):
        if tema_id is None:
            temas = Tema.query.all()
            resultado = temaSchema().dump(temas, many=True)
        else:
            tema = Tema.query.get(tema_id)
            resultado = temaSchema().dump(tema)
        return jsonify(resultado)
    
    def post(self):
        tema_json = temaSchema().load(request.json) 
        tema = tema_json.get('nombre')

        nuevo_tema = Tema(
            nombre=tema,
        )

        db.session.add(nuevo_tema)
        db.session.commit()

        return jsonify(AGREGADO=temaSchema().dump(tema_json))
        
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
