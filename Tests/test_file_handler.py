import pytest
import os

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
    
def test_compile_regex(file_handler):
    file_handler.compile_regex()
    assert file_handler.filename_search is not None

@pytest.mark.parametrize("string,expected",[("file.jpg",True),("file",False),("file.name.txt",True)])    
def test_filename_search(file_handler,string,expected):
    file_handler.compile_regex()
    match = file_handler.filename_search.search(string)
    if match:
        match = True
    else:
        match = False
    assert match == expected

# Testing write_json_receipt_to_file function
def test_accept_new_file(file_handler,tmp_path):
    receipt_dir = tmp_path / "receipts"
    accepted_dir = tmp_path / "accepted"
    os.makedirs(receipt_dir)
    os.makedirs(accepted_dir)

    file_handler.receipt_directory = str(receipt_dir)
    file_handler.accepted_directory = str(accepted_dir)

    test_file = receipt_dir / "testfile.txt"
    test_file.write_text("This is a test file.")

    file_handler.accept("testfile.txt")

    assert not os.path.isfile(test_file)
    assert os.path.isfile(accepted_dir / "testfile.txt")
  
# Testing exclude function  
def test_exclude_new_file(file_handler,tmp_path):
    receipt_dir = tmp_path / "receipts"
    excluded_dir = tmp_path / "excluded"
    os.makedirs(receipt_dir)
    os.makedirs(excluded_dir)

    file_handler.receipt_directory = str(receipt_dir)
    file_handler.excluded_directory = str(excluded_dir)

    test_file = receipt_dir / "testfile.txt"
    test_file.write_text("This is a test file.")

    file_handler.exclude("testfile.txt")

    assert not os.path.isfile(test_file)
    assert os.path.isfile(excluded_dir / "testfile.txt")
    
def test_rename_file(file_handler,tmp_path):
    receipt_dir = tmp_path / "receipts"
    os.makedirs(receipt_dir)
    file_handler.receipt_directory = str(receipt_dir)
    old_file = receipt_dir / "oldname.txt"
    old_file.write_text("This is a test file.")
    new_file = receipt_dir / "newname.txt"
    result = file_handler.rename(str(new_file),str(old_file))
    
    assert not os.path.isfile(old_file)
    assert os.path.isfile(new_file)
    assert result is True

def test_rename_existing_file(file_handler,tmp_path):
    receipt_dir = tmp_path / "receipts"
    os.makedirs(receipt_dir)
    file_handler.receipt_directory = str(receipt_dir)
    old_file = receipt_dir / "oldname.txt"
    old_file.write_text("This is a test file.")
    result = file_handler.rename(str(old_file),str(old_file))
    
    assert os.path.isfile(old_file)
    assert result is False

def test_file_handler(tmp_path):
    new_file = tmp_path / "testfile.txt"

    assert new_file is not None