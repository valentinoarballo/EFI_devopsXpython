from app import ma
from marshmallow import fields

class userSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    email = fields.String()
    password = fields.String()
    fecha_creacion = fields.DateTime()
    
class temaSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()


class publicacionBasicSchema(ma.Schema):
    descripcion = fields.String()
    tema_id =  fields.Integer()
    usuario_id =  fields.Integer()

class publicacionSchema(publicacionBasicSchema):
    id = fields.Integer(dump_only=True)
    fecha_hora = fields.DateTime()
    tema =  fields.Nested(temaSchema)
    usuario =  fields.Nested(userSchema)

class comentarioBasicSchema(ma.Schema):
    descripcion = fields.String()
    publicacion_id = fields.Integer()
    usuario_id = fields.Integer()
  
class comentarioSchema(comentarioBasicSchema):
    id = fields.Integer(dump_only=True)
    fecha_hora = fields.DateTime()
    publicacion =  fields.Nested(publicacionSchema)
    usuario =  fields.Nested(userSchema)