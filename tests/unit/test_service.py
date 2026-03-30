import pytest
from sqlmodel import SQLModel, Session, create_engine
from models import CreateRule
from service import RuleService, RuleAlreadyExistsError, RuleNotFoundError   

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s

@pytest.fixture
def service():
    return RuleService()

def test_create_rule(session, service):
    data = CreateRule(name="test", source_ip="192.168.1.1", port=80)
    rule = service.create_rule(session, data)
    assert rule.id is not None
    assert rule.source_ip == "192.168.1.1"
    assert rule.port == 80  
    
def test_create_duplicate_rule(session, service):                                                                    
    data = CreateRule(name="test", source_ip="192.168.1.1", port=80)                                                 
    service.create_rule(session, data)                                                                               
    with pytest.raises(RuleAlreadyExistsError):
        service.create_rule(session, data)  

def test_get_rule_by_id(session, service):
      data = CreateRule(name="test", source_ip="192.168.1.1", port=80)                                                 
      created = service.create_rule(session, data)                                                                     
      found = service.get_rule_by_id(session, created.id)
      assert found.id == created.id     

def test_get_rule_not_found(session, service):                                                                       
    with pytest.raises(RuleNotFoundError):                                                                           
        service.get_rule_by_id(session, "inexistant-id") 

def test_delete_rule(session, service):                                                                              
    data = CreateRule(name="test", source_ip="192.168.1.1", port=80)                                                 
    created = service.create_rule(session, data)                                                                     
    service.delete_rule(session, created.id)                                                                         
    with pytest.raises(RuleNotFoundError):                                                                           
        service.get_rule_by_id(session, created.id)   

def test_get_all_rules(session, service):                                                                            
    service.create_rule(session, CreateRule(name="r1", source_ip="10.0.0.1", port=80))                               
    service.create_rule(session, CreateRule(name="r2", source_ip="10.0.0.2", port=443))                              
    rules = service.get_all_rules(session)                                                                           
    assert len(rules) == 2 