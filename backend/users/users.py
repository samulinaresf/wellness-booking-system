from db.models import User, User_role
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from datetime import datetime
from admin.auditlog import register_metadata_in_audit_log
from pwdlib import PasswordHash
from typing import Annotated
from security import UserDB, get_current_active_user

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
    db.add(user)
    db.commit()
    db.refresh(user)
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=user.user_id,
                                   metadata_details=f"Usuario {user.user_id} ({user.email}) creado")
    
    return user

def read_users(db: Session):
    user = db.exec(select(User)).all()
    return user
    
def read_user_by_id(db: Session,
                    user_id: int):
    
    user = db.get(User, user_id)
    
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
            return None
            
    if name is not None:
        user.name = name

    if email is not None:
        user.email = email

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
    
    register_metadata_in_audit_log(db=db,
                                    booking_id=None,
                                    user_id=user.user_id,
                                    metadata_details=f"Usuario {user.user_id} ({user.email}) actualizado")
    
    return user

password_hash = PasswordHash.recommended()

def change_user_password(db:Session,
                         user_id: int,
                         current_password: str,
                         new_password: str):
    
    user = db.get(User, user_id) 
    
    if user is None:
        return None
    
    if not password_hash.verify(current_password, user.password_hash):
        raise ValueError("La contraseña actual no es correcta")
    
    if current_password == new_password:
        raise ValueError("La nueva contraseña debe ser diferente")
    
    # 3. Generar el nuevo hash para guardarlo
    new_password_hash = password_hash.hash(new_password)
    
    user.password_hash = new_password_hash
    
    user.updated_at = datetime.now()

    db.add(user)
    db.commit()
    db.refresh(user)
        
    register_metadata_in_audit_log(db=db,
                                    booking_id=None,
                                    user_id=user.user_id,
                                    metadata_details=f"Contraseña del usuario {user.user_id} ({user.email}) actualizada.")
        
    return {"message": "Contraseña actualizada exitosamente"}

def change_user_role(db: Session, 
                    user_id: int,
                    role: User_role):
    
    user = db.get(User, user_id) 
        
    if user is None:
        return None
    
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
        return None
    
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
        return None
        
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
        return None
        
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
