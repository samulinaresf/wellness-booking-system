from db.models import User, User_role
from sqlmodel import Session, select
from datetime import datetime

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
    return user

def change_password_hash():
    None
    
def change_user_role():
    None
    
def delete_user_by_id(db: Session, 
                      user_id: int):
    
    user = db.get(User, user_id)
        
    if user is None:
        return None
        
    db.delete(user)
    db.commit()
    return user

def deactivate_user_by_id(db: Session,
                          user_id: int):
    user = db.get(User, user_id)
        
    if user is None:
        return None
        
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user