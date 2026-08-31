from admin.auditlog import register_metadata_in_audit_log, get_audit_log
from conftest import test_session

def test_register_metadata_in_audit_log(test_session):
   
    result = register_metadata_in_audit_log(test_session,2,1,"Metadata de prueba del auditlog con éxito")
    
    assert result.booking_id == 2
    assert result.user_id == 1
    assert result.metadata_details == "Metadata de prueba del auditlog con éxito"
    
def test_get_audit_log(test_session):
    
    register_metadata_in_audit_log(
        test_session,
        2,
        1,
        "Metadata de prueba del auditlog con éxito"
    )
    
    result = get_audit_log(test_session)
    
    assert len(result) > 0
    assert any(element.booking_id == 2 and element.user_id == 1 and element.metadata_details == "Metadata de prueba del auditlog con éxito" for element in result)
