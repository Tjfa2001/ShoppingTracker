import pytest
from PythonSrc import receipt_reader as rr
from PythonSrc import my_logger as l
from PythonSrc import file_handler as fh
import datetime
import json
import re

@pytest.fixture
def receipt_reader():
    """A receipt reader object instantialised only"""
    return rr.ReceiptReader(l.Logger(fh.FileHandler()))

@pytest.mark.parametrize("file_name, expected",[("receipt.jpg",True),("receipt.x",False),("receipt.jpeg",True),("receipt.png",True),("receipt",False)])
def test_file_extension_check_regex(receipt_reader, file_name, expected):
    
    returned = receipt_reader.file_extension_check(file_name)
    
    assert returned == expected

@pytest.mark.parametrize("receipt_name",["file1.jpg","file2.jpeg","file3.png"])
def test_files_renamed_correctly(receipt_reader,receipt_name):
    
    new_name = receipt_reader.name_check(receipt_name)
    pattern = re.compile(r"lidl_receipt[0-9]*\.(png|jpg|jpeg)")
    match = pattern.match(new_name)
    passing = True if match else False

    assert passing == True

@pytest.mark.parametrize("attribute, expected_type",[("logger",l.Logger),("next_receipt_number",int),
                                                     ("first_name_check",bool),("receipt_dir",str),("accepted_dir",str),
                                                     ("excluded_dir",str)])
def test_attributes_set_for_receipt_reader(receipt_reader,attribute,expected_type):
    
    value = getattr(receipt_reader,attribute)
    
    assert value is not None
    assert isinstance(value,expected_type)
    
@pytest.mark.parametrize("regex",["extension_check","time_search","date_search","item_search",
                                  "total_search","payment_search","discount_search","quantity_check",
                                  "weight_check","name_pattern","extension_pattern"])
def test_regex_patterns_set(receipt_reader,regex):
    
    value = getattr(receipt_reader, regex)

    assert value is not None
    assert isinstance(value, re.Pattern)
    
@pytest.mark.parametrize("message",["Test message","Another test message",""])
def test_logging_writes_to_log(receipt_reader,message):
    
    return_value = receipt_reader.log(message)
    current_time = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M -> ")
    
    assert current_time + message in receipt_reader.logger.log
    assert return_value is True
    
def test_monkey_patch(receipt_reader,monkeypatch):
    monkeypatch.setattr(receipt_reader,"receipt_dir","/abc/123")
    print(receipt_reader.receipt_dir)
    
    assert 1 > 0
    
@pytest.mark.parametrize("receipt,item_details",[(["Penne Rigate 0.41"],("Penne Rigate","0.41")),
                                                 (["Apple Soup £1.55"],("Apple Soup","1.55")),
                                                 (["Broccoli (Tenderstem) £100.35"],("Broccoli (Tenderstem)","100.35"))])   
def test_item_extracted_from_receipt(receipt_reader,receipt,item_details):
    
    string_receipt = receipt_reader.extract_items(receipt)
    json_receipt = json.loads(string_receipt)
    items = json_receipt['items']
    
    for x in items:
        assert (x['name'],x['price']) == item_details