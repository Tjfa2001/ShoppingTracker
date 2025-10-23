import pytest
import receipt_reader as rr
import my_logger as l
import file_handler as fh
import datetime

@pytest.fixture
def receipt_reader():
    return rr.ReceiptReader(l.Logger(fh.FileHandler()))

def test_receipt_reader_init(receipt_reader):
    assert receipt_reader.logger is not None
    assert receipt_reader.first_name_check is True
    assert receipt_reader.next_number == 0
    assert receipt_reader.receipt_dir is not None
    assert receipt_reader.accepted_dir is not None
    assert receipt_reader.excluded_dir is not None

@pytest.mark.parametrize("message",["Test message","Another test message",""])
def test_log(receipt_reader,message):
    receipt_reader.logger.log_message(message)
    current_time = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M -> ")
    assert current_time + message in receipt_reader.logger.log