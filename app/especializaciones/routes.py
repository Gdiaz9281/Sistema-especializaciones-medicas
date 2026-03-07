from flask import Blueprint, render_template, jsonify, request
from app.models import Especializacion
from app import db

bp_especializaciones = Blueprint(
    "especializaciones",
    __name__,
    url_prefix="/especializaciones",
    template_folder="templates"
)

@bp_especializaciones.get("/")
def index():
    especializaciones = Especializacion.query.order_by(Especializacion.id.asc()).all()
    return render_template("especializaciones/index.html", especializaciones=especializaciones)


# 🔹 API LISTAR (GET)
@bp_especializaciones.get("/api")
def api_list():
    especializaciones = Especializacion.query.order_by(Especializacion.id.asc()).all()

    data = [
        {
            "id": e.id,
            "nombre": e.nombre,
            "especialista": e.especialista,
            "tipo": e.tipo,
            "horario": e.horario,
            "activo": e.activo,
        }
        for e in especializaciones
    ]

    return jsonify(data)


def _to_bool(value):
    """
    Convierte valores típicos a boolean:
    true/false, "true"/"false", 1/0, "1"/"0", "si"/"no"
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value == 1
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("true", "1", "si", "sí", "yes", "y"):
            return True
        if v in ("false", "0", "no", "n"):
            return False
    return None


# 🔹 API CAMBIAR ESTADO (PATCH)
@bp_especializaciones.patch("/api/<int:esp_id>/estado")
def cambiar_estado(esp_id):
    esp = Especializacion.query.get_or_404(esp_id)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Debe enviar JSON con el campo 'activo'"}), 400

    if "activo" not in data:
        return jsonify({"error": "Debe enviar el campo 'activo'"}), 400

    nuevo_activo = _to_bool(data["activo"])
    if nuevo_activo is None:
        return jsonify({"error": "Valor inválido para 'activo'. Use true/false o 1/0."}), 400

    esp.activo = nuevo_activo
    db.session.commit()

    return jsonify({
        "ok": True,
        "id": esp.id,
        "activo": esp.activo
    })