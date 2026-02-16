import pytest
import receipt_reader as rr
import my_logger as l
import file_handler as fh
import datetime
import re

@pytest.fixture
def receipt_reader():
    return rr.ReceiptReader(l.Logger(fh.FileHandler()))

@pytest.mark.parametrize("file_name, expected",[("receipt.jpg",True),("receipt.x",False),("receipt.jpeg",True),("receipt.png",True),("receipt",False)])
def test_file_extension_check(receipt_reader, file_name, expected):
    returned = receipt_reader.file_extension_check(file_name)
    assert returned == expected

def test_name_check(receipt_reader,tmp_path):
    new_name = receipt_reader.name_check("hello1.jpg")
    pattern = re.compile(r"lidl_receipt[0-9]*\.(png|jpg|jpeg)")
    match = pattern.match(new_name)
    if match:
        passing = True
    else: 
        passing = False
        
    assert passing == True
    
def test_receipt_reader_init(receipt_reader):
    assert receipt_reader.logger is not None
    assert receipt_reader.first_name_check is True
    assert receipt_reader.next_receipt_number == 0
    assert receipt_reader.receipt_dir is not None
    assert receipt_reader.accepted_dir is not None
    assert receipt_reader.excluded_dir is not None

@pytest.mark.parametrize("message",["Test message","Another test message",""])
def test_log(receipt_reader,message):
    receipt_reader.logger.log_message(message)
    current_time = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M -> ")
    assert current_time + message in receipt_reader.logger.log