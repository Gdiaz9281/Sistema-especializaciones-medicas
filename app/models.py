from app import db

class Especializacion(db.Model):
    __tablename__ = "especializaciones"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialista = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(120), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    def _repr_(self):
        return f"<Especializacion {self.nombre}>"