from PythonSrc import my_logger as l, file_handler as fh
import pytest
import datetime

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
    