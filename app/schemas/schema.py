from app import ma
from marshmallow import fields

class userSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    email = fields.String()
    password = fields.String()
    perfil = fields.String()
    fecha_creacion = fields.DateTime()
    
class temaSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()

class publicacionSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    autor = fields.String()
    description = fields.String()
    perfil = fields.String()
    fecha_hora = fields.DateTime()
    tema = fields.String()
    usuario = fields.String()
    tema_id =  fields.Nested(temaSchema, exclude=('id',))
    usuario_id =  fields.Nested(userSchema, exclude=('id',))

class comentarioSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    autor = fields.String()
    perfil = fields.String()
    descripcion = fields.String()
    fecha_hora = fields.String()
    usuario = fields.String()
    usuario_id = fields.Nested(userSchema, exclude=('id',))
    id_publicacion = fields.Nested(publicacionSchema, exclude=('id',))
  