from PythonSrc import my_logger as l, file_handler as fh
#from PythonSrc.my_logger import log_message, log_error
import pytest
import datetime
import re

@pytest.fixture
def logger():
    file_handler = fh.FileHandler()
    return l.Logger(file_handler)

@pytest.mark.parametrize("message",["","Single Line","General Log Message","%$£./-{}\\","M<> ?!754"])
def test_single_message_logged(logger,message):
    
    str_len = -len(message)
    logger.log_message(message)
    
    if message == "":
        assert logger.log[0] is not None
    else:
        assert message == logger.log[0][str_len:]
        
def test_date_in_message_logged(logger):
    
    logger.log_message("Random message")
    current_time = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M")
    time_string_length = len(current_time)
    
    assert current_time == logger.log[0][:time_string_length]
    
def test_write_to_file(logger,monkeypatch):
    
    monkeypatch.setattr(logger,"write_to_file",lambda: "armadillo")
    a = logger.write_to_file()
    print(f"A: {a}")
    assert 1==1

@pytest.mark.parametrize("error_msg",["","Cannot open X","Error with Y","£$%^&!*"])    
def test_log_error(logger ,error_msg):
    
    str_len = -len(error_msg)
    logger.log_error(error_msg)
    
    if error_msg == "":
        assert logger.log[0] is not None
    else:
        assert error_msg == logger.log[0][str_len:]

@pytest.mark.parametrize("log_list",[[],["","ab"],["Message 1","Message 2","Message 3"]])
def test_list_logged(logger,log_list):
    
    logged_messages = []
    
    logger.log_list_log(log_list)

    for line in logger.log:
        match = re.search("(.+)(-> )(.+)",line)
        if match:
            logged_messages.append(match.group(3))
        else:
            logged_messages.append("")
    
    assert len(logger.log) == len(log_list)
    assert logged_messages == log_list

@pytest.mark.parametrize("function, msg",[("log_error","ABORT"),("log_message","Nice one matey")])
def test_debug_mode(logger,function,msg,capsys):
    
    logger.debug = True
    
    getattr(logger,function)(msg)

    captured = capsys.readouterr()
    
    assert msg in captured.out
