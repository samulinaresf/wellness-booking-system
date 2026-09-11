from bookings.bookings import create_time_slot, update_time_slot, read_time_slots, delete_time_slot, create_booking, read_bookings, get_booking_by_id, read_bookings_by_professional, update_booking, delete_booking
from users.users import create_user
from conftest import test_session
from datetime import datetime
from db.models import Time_slot_status, User_role
from decimal import Decimal
from users.security import UserDB, get_current_active_user
import pytest

def test_create_time_slot(test_session):
    
    start_at = datetime(2026, 9, 1, 10, 0)
    end_at = datetime(2026, 9, 1, 11, 0)
    capacity = 3
    time_slot_status = Time_slot_status.AVAILABLE
    price = Decimal("19.65")
    
    result = create_time_slot(test_session,1,start_at=start_at,end_at=end_at,capacity=capacity,status=time_slot_status,price=price)
    
    assert result.prof_user_id == 1
    assert result.start_at == datetime(2026, 9, 1, 10, 0)
    assert result.end_at == datetime(2026, 9, 1, 11, 0)
    assert result.capacity == 3
    assert result.status == Time_slot_status.AVAILABLE
    assert result.price == Decimal("19.65")

def test_update_time_slot(test_session):
    
    start_at = datetime(2026, 9, 1, 10, 0)
    end_at = datetime(2026, 9, 1, 11, 0)
    capacity = 3
    time_slot_status = Time_slot_status.AVAILABLE
    price = Decimal("19.65")
    
    result = create_time_slot(test_session,1,start_at=start_at,end_at=end_at,capacity=capacity,status=time_slot_status,price=price)
    
    new_time_start_at = datetime(2026, 10, 1, 11, 0)
    new_time_end_at = datetime(2026, 10, 1, 12, 0)
    new_capacity = 4
    new_price = Decimal("19.72")
    
    updated_result = update_time_slot(test_session,result.time_slot_id,start_at=new_time_start_at,end_at=new_time_end_at,capacity=new_capacity,status=time_slot_status,price=new_price)
    
    assert updated_result.start_at == datetime(2026, 10, 1, 11, 0)
    assert updated_result.end_at == datetime(2026, 10, 1, 12, 0)
    assert updated_result.capacity == 4
    assert updated_result.status == Time_slot_status.AVAILABLE
    assert updated_result.price == Decimal("19.72")

def test_read_time_slots(test_session):
        
    time_slot_1_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_1_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_1_capacity = 3
    time_slot_1_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_1_price = Decimal("19.65")
    
    time_slot_2_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_2_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_2_capacity = 3
    time_slot_2_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_2_price = Decimal("19.65")
    
    result_1 = create_time_slot(test_session,1,start_at=time_slot_1_start_at,end_at=time_slot_1_end_at,capacity=time_slot_1_capacity,status=time_slot_1_time_slot_status,price=time_slot_1_price)
    result_2 = create_time_slot(test_session,1,start_at=time_slot_2_start_at,end_at=time_slot_2_end_at,capacity=time_slot_2_capacity,status=time_slot_2_time_slot_status,price=time_slot_2_price)

    results = read_time_slots(test_session)
    
    assert any(
        time_slot.time_slot_id == result_1.time_slot_id
        for time_slot in results
    )

    assert any(
        time_slot.time_slot_id == result_2.time_slot_id
        for time_slot in results
    )

def test_delete_time_slots(test_session):
        
    time_slot_1_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_1_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_1_capacity = 3
    time_slot_1_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_1_price = Decimal("19.65")
    
    time_slot_2_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_2_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_2_capacity = 3
    time_slot_2_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_2_price = Decimal("19.65")
    
    result_1 = create_time_slot(test_session,1,start_at=time_slot_1_start_at,end_at=time_slot_1_end_at,capacity=time_slot_1_capacity,status=time_slot_1_time_slot_status,price=time_slot_1_price)
    result_2 = create_time_slot(test_session,1,start_at=time_slot_2_start_at,end_at=time_slot_2_end_at,capacity=time_slot_2_capacity,status=time_slot_2_time_slot_status,price=time_slot_2_price)

    deleted_result = delete_time_slot(
    test_session,
    result_2.time_slot_id,
    1
)

    results = read_time_slots(test_session)

    assert any(
        time_slot.time_slot_id == result_1.time_slot_id
        for time_slot in results
    )

    assert not any(
        time_slot.time_slot_id == result_2.time_slot_id
        for time_slot in results
    )

def test_create_booking(test_session):
    
    start_at = datetime(2026, 9, 1, 10, 0)
    end_at = datetime(2026, 9, 1, 11, 0)
    capacity = 3
    time_slot_status = Time_slot_status.AVAILABLE
    price = Decimal("19.65")
        
    time_slot_result = create_time_slot(test_session,1,start_at=start_at,end_at=end_at,capacity=capacity,status=time_slot_status,price=price)
    
    result = create_booking(test_session,time_slot_id=time_slot_result.time_slot_id,user_id=time_slot_result.prof_user_id)
    
    assert result is not None
    assert result.time_slot_id == time_slot_result.time_slot_id
    assert result.prof_user_id == time_slot_result.prof_user_id
    assert result.user_id == 1

def test_read_bookings(test_session):
    
    time_slot_1_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_1_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_1_capacity = 3
    time_slot_1_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_1_price = Decimal("19.65")
    
    time_slot_2_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_2_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_2_capacity = 3
    time_slot_2_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_2_price = Decimal("19.65")
    
    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_1_start_at,end_at=time_slot_1_end_at,capacity=time_slot_1_capacity,status=time_slot_1_time_slot_status,price=time_slot_1_price)
    time_slot_2 = create_time_slot(test_session,1,start_at=time_slot_2_start_at,end_at=time_slot_2_end_at,capacity=time_slot_2_capacity,status=time_slot_2_time_slot_status,price=time_slot_2_price)
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=time_slot_1.prof_user_id)
    booking_2 = create_booking(test_session,time_slot_id=time_slot_2.time_slot_id,user_id=time_slot_2.prof_user_id)
    
    results = read_bookings(test_session)
    
    assert any(
        booking.booking_id == booking_1.booking_id
        for booking in results
    )
    
    assert any(
        booking.booking_id == booking_2.booking_id
        for booking in results
    )

def test_get_booking_by_id(test_session):
    
    time_slot_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_capacity = 3
    time_slot_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_price = Decimal("19.65")

    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_start_at,end_at=time_slot_end_at,capacity=time_slot_capacity,status=time_slot_time_slot_status,price=time_slot_price)        
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=time_slot_1.prof_user_id)
    
    result = get_booking_by_id(test_session, booking_1.booking_id)
    
    assert result is not None
    assert result.booking_id == booking_1.booking_id 

def test_read_bookings_by_professional(test_session):
    
    time_slot_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_capacity = 3
    time_slot_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_price = Decimal("19.65")

    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_start_at,end_at=time_slot_end_at,capacity=time_slot_capacity,status=time_slot_time_slot_status,price=time_slot_price)        
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=time_slot_1.prof_user_id)
    
    results = read_bookings_by_professional(test_session, booking_1.prof_user_id)
    
    assert any(
        booking.booking_id == booking_1.booking_id
        for booking in results
    )

def test_update_booking(test_session):
    
    time_slot_1_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_1_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_1_capacity = 3
    time_slot_1_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_1_price = Decimal("19.65")

    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_1_start_at,end_at=time_slot_1_end_at,capacity=time_slot_1_capacity,status=time_slot_1_time_slot_status,price=time_slot_1_price)        
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=time_slot_1.prof_user_id)
    
    time_slot_2_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_2_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_2_capacity = 3
    time_slot_2_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_2_price = Decimal("19.65")

    time_slot_2 = create_time_slot(test_session,1,start_at=time_slot_2_start_at,end_at=time_slot_2_end_at,capacity=time_slot_2_capacity,status=time_slot_2_time_slot_status,price=time_slot_2_price)        
        
    old_time_slot_id = booking_1.time_slot_id

    result = update_booking(
        test_session,
        booking_1.booking_id,
        time_slot_2.time_slot_id
    )

    assert result is not None
    assert result.time_slot_id == time_slot_2.time_slot_id
    assert result.time_slot_id != old_time_slot_id

def test_delete_booking(test_session):
    
    time_slot_1_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_1_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_1_capacity = 3
    time_slot_1_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_1_price = Decimal("19.65")
    
    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_1_start_at,end_at=time_slot_1_end_at,capacity=time_slot_1_capacity,status=time_slot_1_time_slot_status,price=time_slot_1_price)        
    
    time_slot_2_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_2_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_2_capacity = 3
    time_slot_2_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_2_price = Decimal("19.65")
    
    time_slot_2 = create_time_slot(test_session,1,start_at=time_slot_2_start_at,end_at=time_slot_2_end_at,capacity=time_slot_2_capacity,status=time_slot_2_time_slot_status,price=time_slot_2_price)        
            
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=time_slot_1.prof_user_id)
    booking_2 = create_booking(test_session,time_slot_id=time_slot_2.time_slot_id,user_id=time_slot_2.prof_user_id)

    
    deleted_result = delete_booking(test_session, booking_1.booking_id, booking_1.user_id)
    
    result = read_bookings(test_session)
    
    assert deleted_result.booking_id == booking_1.booking_id
    assert not any(booking.booking_id == booking_1.booking_id
                   for booking in result)
    assert any(booking.booking_id == booking_2.booking_id
               for booking in result)

def test_create_booking_duplicated_user(test_session):
    
    start_at = datetime(2026, 9, 1, 10, 0)
    end_at = datetime(2026, 9, 1, 11, 0)
    capacity = 3
    time_slot_status = Time_slot_status.AVAILABLE
    price = Decimal("19.65")
        
    time_slot_result = create_time_slot(test_session,1,start_at=start_at,end_at=end_at,capacity=capacity,status=time_slot_status,price=price)
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_result.time_slot_id,user_id=time_slot_result.prof_user_id)
    booking_2 = create_booking(test_session,time_slot_id=time_slot_result.time_slot_id,user_id=time_slot_result.prof_user_id)

    
    assert booking_1 != booking_2
    assert booking_1 is not None
    assert booking_2 is None 

def test_exceed_booking_capacity(test_session):
    
    start_at = datetime(2026, 9, 1, 10, 0)
    end_at = datetime(2026, 9, 1, 11, 0)
    capacity = 3
    time_slot_status = Time_slot_status.AVAILABLE
    price = Decimal("19.65")
        
    time_slot_result = create_time_slot(test_session,1,start_at=start_at,end_at=end_at,capacity=capacity,status=time_slot_status,price=price)
        
    juan = create_user(test_session,name="Juan",email="juan@example.com",password_hash="ejemplo",phone_number="12345",role=User_role.USER, profile_pic=None, bio=None)
    maria = create_user(test_session,name="Maria",email="maria@example.com",password_hash="ejemplo",phone_number="12346",role=User_role.USER, profile_pic=None, bio=None)
    pepe = create_user(test_session,name="Pepe",email="pepe@example.com",password_hash="ejemplo",phone_number="12347",role=User_role.USER, profile_pic=None, bio=None)
    laura = create_user(test_session,name="Laura",email="laura@example.com",password_hash="ejemplo",phone_number="12348",role=User_role.USER, profile_pic=None, bio=None)
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_result.time_slot_id,user_id=juan.user_id)
    booking_2 = create_booking(test_session,time_slot_id=time_slot_result.time_slot_id,user_id=maria.user_id)
    booking_3 = create_booking(test_session,time_slot_id=time_slot_result.time_slot_id,user_id=pepe.user_id)
    
    assert booking_1 is not None
    assert booking_2 is not None
    assert booking_3 is not None
    with pytest.raises(
        ValueError,
        match="Este horario no está disponible."
    ):
        create_booking(
            test_session,
            time_slot_id=time_slot_result.time_slot_id,
            user_id=laura.user_id
        )

def test_book_unavailable_booking(test_session):
    
    time_slot_1_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_1_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_1_capacity = 1
    time_slot_1_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_1_price = Decimal("19.65")
    
    time_slot_2_start_at = datetime(2026, 8, 1, 10, 0)
    time_slot_2_end_at = datetime(2026, 8, 1, 11, 0)
    time_slot_2_capacity = 2
    time_slot_2_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_2_price = Decimal("18.65")

    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_1_start_at,end_at=time_slot_1_end_at,capacity=time_slot_1_capacity,status=time_slot_1_time_slot_status,price=time_slot_1_price)        
    time_slot_2 = create_time_slot(test_session,1,start_at=time_slot_2_start_at,end_at=time_slot_2_end_at,capacity=time_slot_2_capacity,status=time_slot_2_time_slot_status,price=time_slot_2_price)        

    juan = create_user(test_session,name="Juan",email="juan@example.com",password_hash="ejemplo",phone_number="12345",role=User_role.USER, profile_pic=None, bio=None)
    maria = create_user(test_session,name="Maria",email="maria@example.com",password_hash="ejemplo",phone_number="12346",role=User_role.USER, profile_pic=None, bio=None)
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=juan.user_id)
    booking_2 = create_booking(test_session,time_slot_id=time_slot_2.time_slot_id,user_id=maria.user_id)
    
    with pytest.raises(
        ValueError,
        match="Este horario no está disponible."
    ):
        create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=maria.user_id)
        
    test_session.refresh(time_slot_1)

    assert time_slot_1.status == Time_slot_status.UNAVAILABLE

    assert booking_1 is not None
    assert booking_2 is not None
    


def test_reduce_capacity_under_number_bookings(test_session):
    
    time_slot_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_capacity = 3
    time_slot_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_price = Decimal("19.65")

    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_start_at,end_at=time_slot_end_at,capacity=time_slot_capacity,status=time_slot_time_slot_status,price=time_slot_price)        
    
    juan = create_user(test_session,name="Juan",email="juan@example.com",password_hash="ejemplo",phone_number="12345",role=User_role.USER, profile_pic=None, bio=None)
    maria = create_user(test_session,name="Maria",email="maria@example.com",password_hash="ejemplo",phone_number="12346",role=User_role.USER, profile_pic=None, bio=None)
    pepe = create_user(test_session,name="Pepe",email="pepe@example.com",password_hash="ejemplo",phone_number="12347",role=User_role.USER, profile_pic=None, bio=None)

    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=juan.user_id)
    booking_2 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=maria.user_id)
    booking_3 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=pepe.user_id)


    
    with pytest.raises(
        ValueError,
        match="No se puede modificar capacidad por debajo del número de reservas."
    ):
        update_time_slot(
            test_session,
            time_slot_1.time_slot_id,
            time_slot_1.start_at,
            time_slot_1.end_at,
            2,
            time_slot_1.status,
            time_slot_1.price
        )
    test_session.refresh(time_slot_1)

    assert time_slot_1.capacity == 3

def test_update_taken_booking(test_session):
    
    time_slot_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_capacity = 2
    time_slot_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_price = Decimal("19.65")

    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_start_at,end_at=time_slot_end_at,capacity=time_slot_capacity,status=time_slot_time_slot_status,price=time_slot_price)        
    
    juan = create_user(test_session,name="Juan",email="juan@example.com",password_hash="ejemplo",phone_number="12345",role=User_role.USER, profile_pic=None, bio=None)
    maria = create_user(test_session,name="Maria",email="maria@example.com",password_hash="ejemplo",phone_number="12346",role=User_role.USER, profile_pic=None, bio=None)
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=juan.user_id)
    booking_2 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=maria.user_id)
    
    result = update_time_slot(
            test_session,
            time_slot_1.time_slot_id,
            time_slot_1.start_at,
            time_slot_1.end_at,
            3,
            time_slot_1.status,
            time_slot_1.price
        )
    
    test_session.refresh(time_slot_1)
    
    assert result.capacity == 3
    assert result.status == Time_slot_status.AVAILABLE

def test_change_fake_status(test_session):
    time_slot_start_at = datetime(2026, 9, 1, 10, 0)
    time_slot_end_at = datetime(2026, 9, 1, 11, 0)
    time_slot_capacity = 2
    time_slot_time_slot_status = Time_slot_status.AVAILABLE
    time_slot_price = Decimal("19.65")

    time_slot_1 = create_time_slot(test_session,1,start_at=time_slot_start_at,end_at=time_slot_end_at,capacity=time_slot_capacity,status=time_slot_time_slot_status,price=time_slot_price)        
    
    juan = create_user(test_session,name="Juan",email="juan@example.com",password_hash="ejemplo",phone_number="12345",role=User_role.USER, profile_pic=None, bio=None)
    maria = create_user(test_session,name="Maria",email="maria@example.com",password_hash="ejemplo",phone_number="12346",role=User_role.USER, profile_pic=None, bio=None)
    
    booking_1 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=juan.user_id)
    booking_2 = create_booking(test_session,time_slot_id=time_slot_1.time_slot_id,user_id=maria.user_id)
    
    with pytest.raises(
            ValueError,
            match="No se puede cambiar manualmente el status."
        ):
        
        update_time_slot(
            test_session,
            time_slot_1.time_slot_id,
            time_slot_1.start_at,
            time_slot_1.end_at,
            time_slot_1.capacity,
            Time_slot_status.AVAILABLE,
            time_slot_1.price
        )
    
    test_session.refresh(time_slot_1)

    """
    Yo cubriría estas comprobaciones:
    
- Marcar manualmente como AVAILABLE un slot lleno
    --Debe rechazarse.
- Mover una reserva al mismo slot
    --update_booking() debería dejarla como está.
    --No crear duplicados ni tocar estados innecesariamente.
- Mover una reserva a un slot inexistente
    --Debe rechazarse.
    --La reserva original debe seguir apuntando al slot antiguo.
- Mover una reserva a un slot UNAVAILABLE
    --Debe rechazarse.
La reserva debe conservar su time_slot_id original.
Mover una reserva a un slot lleno
Aunque el estado estuviera mal marcado como AVAILABLE, la comprobación de capacidad debería impedirlo.
Mover una reserva y llenar el slot destino
Si el slot destino tenía una plaza libre, después del movimiento debe pasar a UNAVAILABLE.
Mover una reserva y liberar el slot origen
Si el origen estaba lleno, al sacar una reserva debería volver a AVAILABLE.
Eliminar una reserva y reabrir el slot
Este ya te conviene reforzarlo: no solo comprobar que desaparece la reserva, sino también: assert time_slot.status == Time_slot_status.AVAILABLE
Eliminar una reserva inexistente
Debe devolver None.
Y no debe modificar otras reservas.
Eliminar una reserva de un slot con más de una reserva
Si capacidad = 3 y había 2 reservas, al borrar una sigue AVAILABLE.
Aquí compruebas que no haces algo raro con el status.
Profesional inexistente en create_booking
Si el time_slot.prof_user_id apunta a algo inválido, la reserva debe rechazarse.
No debería ocurrir normalmente con una FK bien montada, pero protege la función.
Fechas inválidas del slot
end_at <= start_at.
Esto puede estar mejor en Pydantic/schema, pero en algún nivel tienes que testearlo.
Capacidad inválida
capacity = 0
capacity = -1
Debe rechazarse.
Precio inválido
Precio negativo.
Esto también puede ir mejor en schema/Pydantic, pero debe existir una prueba en alguna capa.

    """