from db.models import Audit_log
from sqlmodel import Session, select
from datetime import datetime
from db.db import engine

#Crear acciones en el auditlog para llevar el checkeo en panel de administrador 
def register_metadata_in_audit_log(db:Session,
                                   booking_id: int | None,
                                   user_id: int,
                                   metadata_details: str):
   
    auditlog = Audit_log(booking_id=booking_id,user_id=user_id,created_at=datetime.now(),metadata_details=metadata_details)
    db.add(auditlog)
    db.commit()
    db.refresh(auditlog)
    
    return auditlog

#Mostrar todos los registros de auditlog
def get_audit_log():
    with Session(engine) as session:
        auditlog = session.exec(select(Audit_log)).all()
        return auditlog
    
    