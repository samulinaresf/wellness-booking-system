from users.users import create_user, read_users, read_user_by_id, update_user_profile_by_id, change_user_password, password_hash, change_user_role, delete_user_by_id, deactivate_user_by_id, require_superadmin, activate_user_by_id, require_admin
from conftest import test_session
from datetime import datetime
from db.models import Time_slot_status, User_role, User
from decimal import Decimal, InvalidOperation
from users.security import UserDB, get_current_active_user
import pytest
from fastapi import HTTPException

def test_create_user(test_session):
    
    name = "Juan"
    email = "juan@example.com"
    password_hash = "12345"
    phone_number = "12345"
    role = User_role.USER
    profile_pic = None, 
    bio = None
    
    juan = create_user(test_session,name=name, email=email, password_hash=password_hash, phone_number=phone_number, role=role, profile_pic=profile_pic, bio=bio)

    assert juan.name == name
    assert juan.email == email
    assert juan.password_hash == password_hash
    assert juan.phone_number == phone_number
    assert juan.role == role
    assert juan.profile_pic is None
    assert juan.bio is None

def test_create_user_existing_email(test_session):
    
    name = "Juan"
    email = "juan@example.com"
    password_hash = "12345"
    phone_number = "12345"
    role = User_role.USER
    profile_pic = None, 
    bio = None
    
    
    juan = create_user(test_session,name=name, email=email, password_hash=password_hash, phone_number=phone_number, role=role, profile_pic=profile_pic, bio=bio)
    
    assert juan is not None
    
    with pytest.raises(ValueError,
                       match="El email ya existe."):
        create_user(test_session,name=name, email=email, password_hash=password_hash, phone_number=phone_number, role=role, profile_pic=profile_pic, bio=bio)


def test_read_users(test_session):
    
    juan_name = "Juan"
    juan_email = "juan2@example.com"
    juan_password_hash = "12345"
    juan_phone_number = "12345"
    juan_role = User_role.USER
    juan_profile_pic = None, 
    juan_bio = None
        
    juan = create_user(test_session,name=juan_name, email=juan_email, password_hash=juan_password_hash, phone_number=juan_phone_number, role=juan_role, profile_pic=juan_profile_pic, bio=juan_bio)
    
    maria_name = "Maria"
    maria_email = "maria2@example.com"
    maria_password_hash = "12346"
    maria_phone_number = "12346"
    maria_role = User_role.USER
    maria_profile_pic = None, 
    maria_bio = None
            
    maria = create_user(test_session,name=maria_name, email=maria_email, password_hash=maria_password_hash, phone_number=maria_phone_number, role=maria_role, profile_pic=maria_profile_pic, bio=maria_bio)
    
    results = read_users(test_session)
    
    assert any(
        users.user_id == juan.user_id
        for users in results
    )
    
    assert any(
            users.user_id == maria.user_id
            for users in results
    )

def test_read_user_by_id(test_session):
    
    juan_name = "Juan"
    juan_email = "juan@example.com"
    juan_password_hash = "12345"
    juan_phone_number = "12345"
    juan_role = User_role.USER
    juan_profile_pic = None, 
    juan_bio = None
        
    juan = create_user(test_session,name=juan_name, email=juan_email, password_hash=juan_password_hash, phone_number=juan_phone_number, role=juan_role, profile_pic=juan_profile_pic, bio=juan_bio)
    
    result = read_user_by_id(test_session,juan.user_id)
    
    assert result.user_id == juan.user_id

def test_read_fake_user(test_session):
    
    with pytest.raises(ValueError,
                       match="El usuario no existe."):
        read_user_by_id(test_session,user_id=999999999)

def test_update_user_by_id(test_session):
    
    juan_name = "Juan"
    juan_email = "juan@example.com"
    juan_password_hash = "12345"
    juan_phone_number = "12345"
    juan_role = User_role.USER
    juan_profile_pic = None, 
    juan_bio = None
    
    juan = create_user(test_session,name=juan_name, email=juan_email, password_hash=juan_password_hash, phone_number=juan_phone_number, role=juan_role, profile_pic=juan_profile_pic, bio=juan_bio)
    
    result = update_user_profile_by_id(test_session, name=juan_name, email=juan_email, phone_number=juan_phone_number,profile_pic=juan_profile_pic,user_id=juan.user_id,bio="Hola soy Juan")

    test_session.refresh(juan)
    assert result.user_id == juan.user_id
    assert juan.bio == "Hola soy Juan"
    assert result is not None
    assert juan is not None

def test_update_user_one_field(test_session):
    
    juan_name = "Juan"
    juan_email = "juan@example.com"
    juan_password_hash = "12345"
    juan_phone_number = "12345"
    juan_role = User_role.USER
    juan_profile_pic = None, 
    juan_bio = None
    
    juan = create_user(test_session,name=juan_name, email=juan_email, password_hash=juan_password_hash, phone_number=juan_phone_number, role=juan_role, profile_pic=juan_profile_pic, bio=juan_bio)
    result = update_user_profile_by_id(test_session,name=None, email=None, phone_number=None, profile_pic=None, user_id=juan.user_id, bio="Actualizando la nueva bio")

    assert result.user_id == juan.user_id
    test_session.refresh(juan)
    assert juan.bio == "Actualizando la nueva bio"
    assert juan.name == "Juan"

def test_update_user_multiple_fields(test_session):
    
    juan_name = "Juan"
    juan_email = "juan@example.com"
    juan_password_hash = "12345"
    juan_phone_number = "12345"
    juan_role = User_role.USER
    juan_profile_pic = None, 
    juan_bio = None
    
    juan = create_user(test_session,name=juan_name, email=juan_email, password_hash=juan_password_hash, phone_number=juan_phone_number, role=juan_role, profile_pic=juan_profile_pic, bio=juan_bio)
    result = update_user_profile_by_id(test_session,name=None, email=None, phone_number="1234567", profile_pic=None, user_id=juan.user_id, bio="Actualizando la nueva bio")

    assert result.user_id == juan.user_id
    test_session.refresh(juan)
    assert juan.bio == "Actualizando la nueva bio"
    assert juan.phone_number == "1234567"
    assert juan.name == "Juan"

def test_update_user_existing_email(test_session):
    
    juan_name = "Juan"
    juan_email = "juan@example.com"
    juan_password_hash = "12345"
    juan_phone_number = "12345"
    juan_role = User_role.USER
    juan_profile_pic = None, 
    juan_bio = None
    
    juan_alberto_name = "Juan Alberto"
    juan_alberto_email = "juanalberto@example.com"
    juan_alberto_password_hash = "12345"
    juan_alberto_phone_number = "12345"
    juan_alberto_role = User_role.USER
    juan_alberto_profile_pic = None, 
    juan_alberto_bio = None
    
    juan = create_user(test_session,name=juan_name, email=juan_email, password_hash=juan_password_hash, phone_number=juan_phone_number, role=juan_role, profile_pic=juan_profile_pic, bio=juan_bio)
    
    juan_alberto = create_user(test_session,name=juan_alberto_name, email=juan_alberto_email, password_hash=juan_alberto_password_hash, phone_number=juan_alberto_phone_number, role=juan_alberto_role, profile_pic=juan_alberto_profile_pic, bio=juan_alberto_bio)
    
    with pytest.raises(ValueError,match="El email ya existe."):
        update_user_profile_by_id(test_session, name=juan_alberto_name, email="juan@example.com", phone_number=juan_alberto_phone_number,profile_pic=juan_alberto_profile_pic,user_id=juan_alberto.user_id,bio=juan_alberto_bio)

def test_update_fake_user(test_session):
    
    
    with pytest.raises(ValueError,
                       match="El usuario no existe."):
        update_user_profile_by_id(test_session,name="Juan",email="juan@example.com",phone_number="12345",profile_pic=None,user_id=999999999,bio="Esta es mi biografia")

def test_change_user_password(test_session):

    current_password = "12345"
    new_password = "123456"

    current_password_hash = password_hash.hash(current_password)

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash=current_password_hash,
        phone_number="12345",
        role=User_role.USER,
        profile_pic=None,
        bio=None
    )

    old_hash = juan.password_hash

    result = change_user_password(
        test_session,
        user_id=juan.user_id,
        current_password=current_password,
        new_password=new_password
    )

    test_session.refresh(juan)

    assert juan.password_hash == old_hash

def test_change_user_fake_password(test_session):

    current_password = "12345"
    current_fake_password = "123"
    new_password = "123456"

    current_password_hash = password_hash.hash(current_password)

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash=current_password_hash,
        phone_number="12345",
        role=User_role.USER,
        profile_pic=None,
        bio=None
    )

    old_hash = juan.password_hash

    with pytest.raises(ValueError, match="La contraseña actual no es correcta"):
        change_user_password(
            test_session,
            user_id=juan.user_id,
            current_password=current_fake_password,
            new_password=new_password
        )

def test_change_fake_user_password(test_session):

    current_password = "12345"
    new_password = "123456"

    current_password_hash = password_hash.hash(current_password)

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash=current_password_hash,
        phone_number="12345",
        role=User_role.USER,
        profile_pic=None,
        bio=None
    )

    old_hash = juan.password_hash

    with pytest.raises(ValueError,
                       match="El usuario no existe."):
        change_user_password(
        test_session,
        user_id=999999,
        current_password=current_password,
        new_password=new_password
    )

def test_change_same_password(test_session):

    current_password = "12345"
    new_password = "12345"

    current_password_hash = password_hash.hash(current_password)

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash=current_password_hash,
        phone_number="12345",
        role=User_role.USER,
        profile_pic=None,
        bio=None
    )

    old_hash = juan.password_hash

    with pytest.raises(ValueError,
                       match="La nueva contraseña debe ser diferente a la anterior."):
        change_user_password(
            test_session,
            user_id=juan.user_id,
            current_password=current_password,
            new_password=new_password
        )

def test_change_user_role(test_session):
    
    juan = create_user(
            test_session,
            name="Juan",
            email="juan@example.com",
            password_hash="12345",
            phone_number="12345",
            role=User_role.USER,
            profile_pic=None,
            bio=None
        )
    
    assert juan.role == User_role.USER
    
    result = change_user_role(test_session,user_id=juan.user_id, role=User_role.ADMIN)
    test_session.refresh(juan)
    
    assert result.role == User_role.ADMIN
    assert result.role == juan.role
    assert juan.role == User_role.ADMIN

def test_change_fake_user_role(test_session):
    
    juan = create_user(
            test_session,
            name="Juan",
            email="juan@example.com",
            password_hash="12345",
            phone_number="12345",
            role=User_role.USER,
            profile_pic=None,
            bio=None
        )
    

    with pytest.raises(ValueError,
                       match="El usuario no existe."):
        change_user_role(test_session,user_id=999999, role=User_role.ADMIN)
    

def test_delete_user_by_id(test_session):
    
    juan = create_user(
                test_session,
                name="Juan",
                email="juan@example.com",
                password_hash="12345",
                phone_number="12345",
                role=User_role.USER,
                profile_pic=None,
                bio=None
            )
    
    result = delete_user_by_id(test_session, user_id=juan.user_id)
    
    assert result.user_id == juan.user_id
    
    deleted_user = test_session.get(User, juan.user_id)

    assert deleted_user is None

def test_delete_fake_user_by_id(test_session):
    
    juan = create_user(
                test_session,
                name="Juan",
                email="juan@example.com",
                password_hash="12345",
                phone_number="12345",
                role=User_role.USER,
                profile_pic=None,
                bio=None
            )
    
    with pytest.raises(ValueError,
                       match="El usuario no existe."):
        delete_user_by_id(test_session, user_id=999999)

def test_deactivate_user_by_id(test_session):
    
    juan = create_user(
                test_session,
                name="Juan",
                email="juan@example.com",
                password_hash="12345",
                phone_number="12345",
                role=User_role.USER,
                profile_pic=None,
                bio=None
            )
    assert juan.is_active == True
    
    result = deactivate_user_by_id(test_session, user_id=juan.user_id)
    
    assert result.is_active == False

def test_deactivate_or_activate_fake_user(test_session):
        
    with pytest.raises(ValueError,
            match="El usuario no es válido."
            ):
        deactivate_user_by_id(test_session,user_id=999999999)
    
    with pytest.raises(ValueError,
            match="El usuario no es válido."
            ):
        activate_user_by_id(test_session,user_id=999999999)

def test_deactivate_user_by_id(test_session):
    
    juan = create_user(
                test_session,
                name="Juan",
                email="juan@example.com",
                password_hash="12345",
                phone_number="12345",
                role=User_role.USER,
                profile_pic=None,
                bio=None
            )
    assert juan.is_active == True
    
    result = deactivate_user_by_id(test_session, user_id=juan.user_id)
    test_session.refresh(juan)
    assert result.is_active == False

def test_activate_user_by_id(test_session):
    
    juan = create_user(
                test_session,
                name="Juan",
                email="juan@example.com",
                password_hash="12345",
                phone_number="12345",
                role=User_role.USER,
                profile_pic=None,
                bio=None
            )
    assert juan.is_active == True
    
    deactivate_user = deactivate_user_by_id(test_session, user_id=juan.user_id)
    test_session.refresh(juan)
    assert deactivate_user.is_active == False
    assert juan.is_active == False
    
    activate_user = activate_user_by_id(test_session, user_id=juan.user_id)
    test_session.refresh(juan)
    assert activate_user.is_active == True
    assert juan.is_active == True

def test_require_admin_rejects_user(test_session):

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash="12345",
        phone_number="12345",
        role=User_role.USER,
        profile_pic=None,
        bio=None
    )

    with pytest.raises(HTTPException) as exc:
        require_admin(juan)

    assert exc.value.status_code == 403

def test_require_superadmin_rejects_user(test_session):

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash="12345",
        phone_number="12345",
        role=User_role.USER,
        profile_pic=None,
        bio=None
    )

    with pytest.raises(HTTPException) as exc:
        require_superadmin(juan)

    assert exc.value.status_code == 403

def test_require_superadmin_rejects_admin(test_session):

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash="12345",
        phone_number="12345",
        role=User_role.ADMIN,
        profile_pic=None,
        bio=None
    )

    with pytest.raises(HTTPException) as exc:
        require_superadmin(juan)

    assert exc.value.status_code == 403

def test_require_admin_accepts(test_session):

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash="12345",
        phone_number="12345",
        role=User_role.ADMIN,
        profile_pic=None,
        bio=None
    )

    result = require_admin(juan)

    assert result.role == User_role.ADMIN
    
def test_require_admin_accepts_superadmin(test_session):

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash="12345",
        phone_number="12345",
        role=User_role.SUPERADMIN,
        profile_pic=None,
        bio=None
    )

    result = require_admin(juan)

    assert result.role == User_role.SUPERADMIN

def test_require_superadmin_accepts(test_session):

    juan = create_user(
        test_session,
        name="Juan",
        email="juan@example.com",
        password_hash="12345",
        phone_number="12345",
        role=User_role.SUPERADMIN,
        profile_pic=None,
        bio=None
    )

    result = require_superadmin(juan)

    assert result.role == User_role.SUPERADMIN



"""
Contraseña olvidada                 ❌
Email formato                       ❌
Contraseña formato                  ❌
email_confirmation_to_change_password
confirm_password_change"""
        


    
