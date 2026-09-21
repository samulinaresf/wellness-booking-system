#users.py

from db.models import User, User_role, PasswordChangeRequest
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from datetime import datetime
from admin.auditlog import register_metadata_in_audit_log
from pwdlib import PasswordHash
from typing import Annotated
from users.security import UserDB, get_current_active_user, create_email_verification_token, verify_email_token, verify_password_change_token, create_password_change_token
from users.email import send_message_by_email
from datetime import datetime, timedelta

def create_user(db:Session,
                name: str,
                email: str,
                password_hash: str,
                phone_number: str | None,
                role: User_role,
                profile_pic: str | None,
                bio: str | None,
                ):
    user = User(name=name, email=email, password_hash=password_hash, phone_number=phone_number, role=role, profile_pic=profile_pic, bio=bio, created_at=datetime.now(), updated_at=datetime.now(), is_active=True, last_login_at=datetime.now())
    
    existing_user = db.exec(
                        select(User).where(User.email == email)
                    ).first()
                
    if existing_user is not None:
        raise ValueError("El email ya existe.")
    
    db.add(user)
    db.commit()
    db.refresh(user)

    
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=user.user_id,
                                   metadata_details=f"Usuario {user.user_id} ({user.email}) creado")
    
    return user

def send_email_for_new_user(db: Session,
                            email: str):
    
    user = db.exec(
            select(User).where(User.email == email)
        ).first()
    
    if user is None:
        raise ValueError("El email no existe.")
    
    token = create_email_verification_token(user.email)
        
    send_message_by_email(
        user.email,
        "Confirma tu email",
        f"Pulsa aquí para verificar tu cuenta: "
        f"http://localhost:8000/usuarios/verificar-email?token={token}"
    )

def read_users(db: Session):
    user = db.exec(select(User)).all()
    return user
    
def read_user_by_id(db: Session,
                    user_id: int):
    
    user = db.get(User, user_id)
    
    if user is None:
        raise ValueError("El usuario no existe.")
    
    return user

def update_user_profile_by_id(db: Session,
                              user_id: int,
                              name: str | None,
                              email: str | None,
                              phone_number: str | None,
                              profile_pic: str | None,
                              bio: str | None):
    
    user = db.get(User, user_id)
        
    if user is None:
            raise ValueError("El usuario no existe.")
            
    if name is not None:
        user.name = name

    email_changed = False

    if email is not None and email != user.email:
    
        existing_user = db.exec(
                    select(User).where(User.email == email)
                ).first()
            
        if existing_user is not None:
            raise ValueError("El email ya existe.")
        
        user.email = email
        user.email_verified = False
        email_changed = True

    if phone_number is not None:
        user.phone_number = phone_number

    if bio is not None:
        user.bio = bio

    if profile_pic is not None:
        user.profile_pic = profile_pic

    user.updated_at = datetime.now()
        
    db.add(user)
    db.commit()
    db.refresh(user)
    
    if email_changed:
        token = create_email_verification_token(user.email)

        send_message_by_email(
            user.email,
            "Confirma tu nuevo email",
            f"Pulsa aquí para verificar tu cuenta: "
            f"http://localhost:8000/usuarios/verificar-email?token={token}"
        )
    
    register_metadata_in_audit_log(db=db,
                                    booking_id=None,
                                    user_id=user.user_id,
                                    metadata_details=f"Usuario {user.user_id} ({user.email}) actualizado")
    
    return user

password_hash = PasswordHash.recommended()

def email_confirmation_to_change_password(
    email: str,
    password_change_id: int
):
    if password_change_id is None:
        raise ValueError("El id no es válido.")
    token = create_password_change_token(
        email,
        password_change_id
    )
    
    send_message_by_email(
        email,
        "Confirma tu cambio de contraseña",
        f"Pulsa aquí para confirmar el cambio: "
        f"http://localhost:8000/usuarios/confirmar-cambio-contrasena?token={token}"
    )

def change_user_password(db:Session,
                         user_id: int,
                         current_password: str,
                         new_password: str):
    
    user = db.get(User, user_id) 
        
    if user is None:
        raise ValueError("El usuario no existe.")
        
    if not password_hash.verify(current_password, user.password_hash):
        raise ValueError("La contraseña actual no es correcta")

    if current_password == new_password:
                    raise ValueError("La nueva contraseña debe ser diferente a la anterior.")
    
    new_password_hash = password_hash.hash(new_password)

    temporal_password = PasswordChangeRequest(user_id=user.user_id,
                                              expires_at=datetime.now() + timedelta(minutes=30))
    
    temporal_password.new_password_hash = new_password_hash
    
    db.add(temporal_password)
    db.commit()
    db.refresh(temporal_password)
    
    email_confirmation_to_change_password(
        user.email,
        temporal_password.password_change_id
    )        
    
    return {"message": "Revisa tu correo para confirmar el cambio"}

def confirm_password_change(db: Session, 
                            token: str):
    
    email, password_change_id = verify_password_change_token(token)
    
    temporal_password = db.get(PasswordChangeRequest,password_change_id)
    
    if temporal_password is None:
        raise ValueError("La solicitud de cambio de contraseña no existe.")
    
    user = db.get(
        User,
        temporal_password.user_id
    )
    
    if user is None:
        raise ValueError("El usuario no existe.")
    
    if temporal_password.expires_at < datetime.now():
        raise ValueError("La solicitud ha expirado.")
    
    user.password_hash = temporal_password.new_password_hash
    user.updated_at = datetime.now()
    
    db.add(user)
    db.delete(temporal_password)
    db.commit()
    db.refresh(user)
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=user.user_id,
                                   metadata_details= f"{user.name} ha cambiado su contraseña exitosamente")
    
    return {"message": "Contraseña cambiada con éxito."}

def change_user_role(db: Session, 
                    user_id: int,
                    role: User_role):
    
    user = db.get(User, user_id) 
        
    if user is None:
        raise ValueError("El usuario no existe.")
    
    old_role = user.role

    user.role = role
    
    user.updated_at = datetime.now()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    register_metadata_in_audit_log(db=db,
                                    booking_id=None,
                                    user_id=user.user_id,
                                    metadata_details=f"Rol del usuario {user.user_id} ({user.email}) actualizado de {old_role} a {user.role}.")
    
    return user
    
def delete_user_by_id(db: Session, 
                      user_id: int):
    
    user = db.get(User, user_id)
        
    if user is None:
        raise ValueError("El usuario no existe.")
    
    #Registrar metadata antes de eliminar el registro
    register_metadata_in_audit_log(db=db,
                                    booking_id=None,
                                    user_id=user.user_id,
                                    metadata_details=f"Usuario {user.user_id} ({user.email}) eliminado.")
        
    db.delete(user)
    db.commit()
    
    return user

def deactivate_user_by_id(db: Session,
                          user_id: int):
    user = db.get(User, user_id)
        
    if user is None:
        raise ValueError("El usuario no es válido.")
        
    user.is_active = False
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=user.user_id,
                                   metadata_details=f"Usuario {user.user_id} ({user.email}) desactivado.")
        
    
    return user

def activate_user_by_id(db: Session,
                          user_id: int):
    user = db.get(User, user_id)
        
    if user is None:
        raise ValueError("El usuario no es válido.")
        
    user.is_active = True
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=user.user_id,
                                   metadata_details=f"Usuario {user.user_id} ({user.email}) activado.")
        
    
    return user

def require_admin(current_user: Annotated[UserDB, Depends(get_current_active_user)]):
    
    if current_user.role not in [User_role.ADMIN, User_role.SUPERADMIN]:
        raise HTTPException(status_code=403)
    return current_user
    
def require_superadmin(current_user: Annotated[UserDB, Depends(get_current_active_user)]):
    
    if current_user.role != User_role.SUPERADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user
