import PythonSrc.master_dictionary as md 
import pytest
import os
import json

@pytest.fixture
def normal_master():
    master_dictionary = md.MasterDict()
    return master_dictionary

@pytest.fixture()
def blank_master(tmp_path):
    master_dictionary = md.MasterDict()
    #os.makedirs(tmp_path)
    master_dictionary.dictionary_location = tmp_path
    master_dictionary.read_from_file()
    master_dictionary.load_file_to_json()
    return master_dictionary
    
def test_dictionary_location_exists(normal_master):
    
    assert normal_master.dictionary_location is not None

@pytest.mark.parametrize("key,value",[("Pink Lady Apples","Apples"),("Pepper Red Loose 0011902","Red Pepper")])
def test_update_inserts_into_master(blank_master,key,value):
    
    blank_master.update(key,value)

    assert blank_master.mast_dict_json[key] == value
    
#@pytest.mark.skip(reason="Not written yet")
@pytest.mark.parametrize("key,value",[("Pink Lady Apples","Apples"),("Pepper Red Loose 0011902","Red Pepper")])
def test_remove_from_master_works(blank_master,key,value):
    
    blank_master.update(key,value)
    
    blank_master.remove_from_master(key)
    
    assert key not in blank_master.mast_dict_json.keys()
    
@pytest.mark.skip(reason="Not written yet")
def test_can_read_master_from_file(master):
    assert 1 == 0
    
@pytest.mark.skip(reason="Not written yet")
def test_can_write_master_to_file(master):
    assert 1 == 0