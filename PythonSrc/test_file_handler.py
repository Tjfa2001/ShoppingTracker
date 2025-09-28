import pytest

@pytest.fixture
def file_handler():
    import file_handler as fh
    return fh.FileHandler()

def test_get_directories(file_handler):
    file_handler.get_directories()
    assert file_handler.processed_directory is not None
    assert file_handler.receipt_directory is not None
    assert file_handler.accepted_directory is not None
    assert file_handler.excluded_directory is not None
    assert file_handler.log_directory is not None

@pytest.mark.parametrize("filename,expected", [("not_a_file", None), ("testfile.txt","This is a test file.")])
def test_read_from_file(file_handler,tmp_path,filename,expected):
    test_file = tmp_path / filename
    if expected is not None:
        test_file.write_text(expected)
    
    text = file_handler.read_from_file(test_file)

    assert text == expected

def test_file_handler(tmp_path):
    new_file = tmp_path / "testfile.txt"

    assert new_file is not None