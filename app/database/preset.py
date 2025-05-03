from sqlmodel import Session, select
from ..models.complaint import Complaint

# Todo: change the way the preset evaluates if it is present or not

common_complaints = [
    "Acumulación de basura en calles y aceras",
    "Contenedores de basura insuficientes",
    "Contenedores de basura mal ubicados",
    "Recolección de basura irregular",
    "Recolección de basura infrecuente",
    "Falta de separación de residuos para reciclaje",
    "Incumplimiento de horarios para sacar la basura",
    "Desechos voluminosos abandonados",
    "Quema de basura",
    "Contenedores de basura sucios",
    "Animales callejeros esparciendo basura",
    "Ruidos excesivos por la noche",
    "Ruidos excesivos temprano por la mañana",
    "Música alta constante",
    "Fiestas ruidosas frecuentes",
    "Trabajos de construcción ruidosos fuera de horario",
    "Ladridos de perros persistentes",
    "Vehículos estacionados en aceras",
    "Vehículos estacionados bloqueando entradas",
    "Vehículos estacionados en zonas prohibidas",
    "Obstrucción de la vía pública con objetos",
    "Falta de mantenimiento de jardines comunes",
    "Iluminación deficiente en áreas comunes",
    "Mobiliario urbano en mal estado",
    "Actividades comerciales ruidosas en zona residencial",
    "Mascotas sin correa",
    "Mascotas que ensucian sin limpiar",
    "Discusiones frecuentes entre vecinos",
    "Comportamientos irrespetuosos",
    "Presencia excesiva de mosquitos",
    "Presencia excesiva de cucarachas",
    "Presencia excesiva de ratas",
    "Malos olores persistentes",
    "Sensación de inseguridad",
    "Robos frecuentes"
]


def in_database(session: Session, text: str):
    statement = select(Complaint).where(Complaint.text == text)
    if session.exec(statement).first():
        return True

    return False


def insertPresets(session: Session):
    for t in common_complaints:
        if in_database(session, t):
            return

        new_complaint = Complaint(text=t)
        session.add(new_complaint)

    session.commit()

    return
