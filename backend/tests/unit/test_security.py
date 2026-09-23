from users.security import verify_password, get_password_hash, get_user, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user, get_current_active_user, create_email_verification_token, verify_email_token, create_password_change_token, verify_password_change_token, get_current_verified_user
from users.users import create_user, deactivate_user_by_id
from db.models import User_role
import jwt
import pytest
from fastapi import HTTPException
from datetime import datetime, timedelta

def test_verify_password():
    
    plain_password = "123456"
    hashed_password = get_password_hash(plain_password)
    
    result = verify_password(plain_password=plain_password, hashed_password=hashed_password)
    
    assert result is True

def test_get_password_hash():
    
    plain_password = "123456"

    hashed_password = get_password_hash(plain_password)

    assert isinstance(hashed_password, str)
    assert hashed_password != plain_password
    assert verify_password(plain_password, hashed_password)

def test_get_user(test_session):
    
    juan = create_user(test_session,name="Juan", email="juan6@example.com", password_hash="1234", phone_number="123456", role=User_role.USER, profile_pic=None, bio=None)

    result = get_user(test_session, "juan6@example.com")
    
    assert result.email == juan.email


def test_authenticate_user(test_session):
    
    plain_password = "123456"
    
    hashed_password = get_password_hash(plain_password)
    
    juan = create_user(test_session,name="Juan", email="juan6@example.com", password_hash=hashed_password, phone_number="123456", role=User_role.USER, profile_pic=None, bio=None)

    user = get_user(test_session, juan.email)
    
    result = authenticate_user(test_session, juan.email, plain_password)
    
    assert result.email == "juan6@example.com"
    assert result.password_hash == juan.password_hash

def test_create_access_token():
    
    data = {"sub": "juan@example.com"}

    token = create_access_token(data)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert isinstance(token, str)
    assert payload["sub"] == "juan@example.com"
    assert payload["purpose"] == "access"
    assert "exp" in payload

@pytest.mark.anyio    
async def test_get_current_user(test_session):
    
    juan = create_user(test_session,name="Juan", email="juan6@example.com", password_hash="12345", phone_number="123456", role=User_role.USER, profile_pic=None, bio=None)

    data = {"sub": juan.email}
    
    token = create_access_token(data)
    
    result = await get_current_user(token,test_session)
    
    assert result.user_id == juan.user_id
    assert result.email == "juan6@example.com"

@pytest.mark.anyio    
async def test_get_current_fake_user(test_session):
    
    juan = create_user(test_session,name="Juan", email="juan6@example.com", password_hash="12345", phone_number="123456", role=User_role.USER, profile_pic=None, bio=None)

    data = {"sub": "maria@example.com"}
    
    token = create_access_token(data)
    
    with pytest.raises(HTTPException,
                    match="No podemos validar las credenciales"
                    ):
            await get_current_user(token,test_session)
    
    

@pytest.mark.anyio    
async def test_get_current_active_user(test_session):
    
    juan = create_user(test_session,name="Juan", email="juan6@example.com", password_hash="12345", phone_number="123456", role=User_role.USER, profile_pic=None, bio=None)
    
    result = await get_current_active_user(juan)
    
    assert result.user_id == juan.user_id

@pytest.mark.anyio    
async def test_get_current_active_user_with_inactive_user(test_session):
    
    juan = create_user(test_session,name="Juan", email="juan6@example.com", password_hash="12345", phone_number="123456", role=User_role.USER, profile_pic=None, bio=None)
    
    juan_deactivated = deactivate_user_by_id(test_session, user_id=juan.user_id)
    
    with pytest.raises(HTTPException,
                match="Usuario inactivo"
                ):
        await get_current_active_user(juan_deactivated)

def test_verify_email_token():
    
    email="juan6@example.com"
    
    create_email_verification_token(email)
        
    token = create_email_verification_token(email)

    result = verify_email_token(token)

    assert result == email

def test_create_email_verification_token():

    email = "juan6@example.com"

    token = create_email_verification_token(email)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert payload["sub"] == email
    assert payload["purpose"] == "email_verification"
    assert "exp" in payload
    
def test_create_password_change_token():

    email = "juan@example.com"
    password_change_id = 1

    token = create_password_change_token(
        email,
        password_change_id
    )

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert payload["sub"] == email
    assert payload["password_change_id"] == 1
    assert payload["purpose"] == "password_change"
    assert "exp" in payload

def test_verify_password_change_token():
    
    email = "juan@example.com"
    password_change_id = 1
    
    token = create_password_change_token(email, password_change_id)
    
    result = verify_password_change_token(token)
    
    assert result == (email, password_change_id)

def test_verify_password_change_invalid_token():
    
    email = "juan@example.com"
    password_change_id = None
    
    token = create_password_change_token(email, password_change_id)
    
    with pytest.raises(ValueError,
                       match="Token de cambio de contraseña inválido."):
        verify_password_change_token(token)
        
@pytest.mark.anyio
async def test_get_current_verified_user(test_session):

    juan = create_user(
        test_session,
        name="Juan",
        email="juan6@example.com",
        password_hash=get_password_hash("123456"),
        phone_number="123456",
        role=User_role.USER,
        profile_pic=None,
        bio=None
    )

    juan.email_verified = True
    test_session.add(juan)
    test_session.commit()
    test_session.refresh(juan)

    result = await get_current_verified_user(juan)
    
    assert result.user_id == juan.user_id
    assert result.email_verified is True


@pytest.mark.anyio
async def test_get_current_unverified_user(test_session):

    juan = create_user(
        test_session,
        name="Juan",
        email="juan6@example.com",
        password_hash=get_password_hash("123456"),
        phone_number="123456",
        role=User_role.USER,
        profile_pic=None,
        bio=None
    )

    juan.email_verified = False
    test_session.add(juan)
    test_session.commit()
    test_session.refresh(juan)

    with pytest.raises(HTTPException, match="Debes verificar tu email."):
        await get_current_verified_user(juan)
    
    
    
    
    
    
    

