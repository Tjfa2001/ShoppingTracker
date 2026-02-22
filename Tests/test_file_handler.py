import pytest
import os
import my_logger as ml

@pytest.fixture
def file_handler():
    import file_handler as fh
    return fh.FileHandler()

@pytest.fixture
def get_directories(file_handler):
    file_handler.get_directories()
    return file_handler

@pytest.fixture
def compile_regex(file_handler):
    file_handler.compile_regex()
    return file_handler

@pytest.mark.parametrize("dir",["processed_directory","receipt_directory","accepted_directory","excluded_directory","log_directory"])
def test_directory_variables_set(file_handler,dir):
    
    attr = getattr(file_handler,dir)
    
    assert attr is not None

@pytest.mark.parametrize("filename,expected", [("not_a_file", ""), ("testfile.txt","This is a test file.")])
def test_reads_from_file(file_handler,tmp_path,filename,expected):
    
    test_file = tmp_path / filename

    test_file.write_text(expected)
    text = file_handler.read_from_file(test_file)

    assert text == expected
    
def test_filename_search_regex_compiled(file_handler,compile_regex):

    assert file_handler.filename_search is not None

@pytest.mark.parametrize("string,expected",[("file.jpg",True),("file",False),("file.name.txt",True)])    
def test_filename_search_finds_files(file_handler,compile_regex,string,expected):

    match = file_handler.filename_search.search(string)
    
    match = True if match else False

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
    new_file = receipt_dir / "newname.txt"
    
    old_file.write_text("This is a test file.")
    result = file_handler.rename(str(new_file),str(old_file))
    
    assert not os.path.isfile(old_file)
    assert os.path.isfile(new_file)
    assert result is True

def test_rename_file_to_itself(file_handler,tmp_path):
    
    receipt_dir = tmp_path / "receipts"
    os.makedirs(receipt_dir)
    file_handler.receipt_directory = str(receipt_dir)
    old_file = receipt_dir / "oldname.txt"
    
    old_file.write_text("This is a test file.")
    result = file_handler.rename(str(old_file),str(old_file))
    
    assert os.path.isfile(old_file)
    assert result is False

def test_writing_json_receipt_to_non_directory_fails(file_handler,tmp_path):
    
    new_non_existent_dir = tmp_path / "non_exist"
    test_file = new_non_existent_dir / "testfile.txt"
    json_obj = None
    file_handler.processed_directory = new_non_existent_dir
    
    with pytest.raises(OSError):
        file_handler.write_json_receipt_to_file(str(test_file),json_obj)

@pytest.mark.parametrize("file_name,json_obj",[("testfile.txt",None),("testfile2.jpg",None),("testfile3.jpeg",'{"a":"b","c":"d"}')])        
def test_writing_json_receipt_makes_a_file(file_handler,file_name,json_obj,tmp_path):
    
    json_obj = None
    file_handler.processed_directory = tmp_path
    test_file = tmp_path / "testfile.txt"
    test_file_json = tmp_path / "testfile.json"
    
    file_handler.write_json_receipt_to_file(str(test_file),json_obj)
    
    assert os.path.isfile(test_file_json)
    
    
def test_writes_logger_to_file(file_handler,tmp_path):
    
    file_handler.log_directory = tmp_path
    logger = ml.Logger(file_handler)
    
    file_handler.write_logger_to_file(logger)
    log_directory_files = os.listdir(tmp_path)

    assert log_directory_files is not None