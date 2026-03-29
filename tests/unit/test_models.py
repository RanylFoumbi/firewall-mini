import pytest 
from models import CreateRule
                                                                                                                       
   
def test_valid_rule():                                                                                               
    rule = CreateRule(name="test", source_ip="192.168.1.1", port=80)                                               
    assert rule.source_ip == "192.168.1.1"                                                                           
    assert rule.port == 80
                                                                                                                       
                                                                                                                     
def test_invalid_ip():
    with pytest.raises(ValueError):
        CreateRule(name="test", source_ip="not_an_ip", port=80)
                                                                                                                       
   
def test_invalid_port_too_low():                                                                                     
    with pytest.raises(ValueError):                                                                                
        CreateRule(name="test", source_ip="192.168.1.1", port=0)
                                                                                                                       
   
def test_invalid_port_too_high():                                                                                    
    with pytest.raises(ValueError):                                                                                
        CreateRule(name="test", source_ip="192.168.1.1", port=99999)
