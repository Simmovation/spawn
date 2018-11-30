from os import path

import pytest

from multiwindcalc.util.hash import file_hash

def create_file(tmpdir, contents, name):
    filename = path.join(tmpdir, name)
    with open(filename, 'w') as fp:
        fp.write(contents)
    return filename

@pytest.fixture
def file_a(tmpdir):
    return create_file(tmpdir, 'This is file a', 'file_a.txt')

@pytest.fixture
def file_b(tmpdir):
    return create_file(tmpdir, 'This is file b', 'file_b.txt')

@pytest.fixture
def file_a_copy(tmpdir):
    return create_file(tmpdir, 'This is file a', 'file_a_copy.txt')

def test_file_returns_hash(file_a):
    assert file_hash(file_a)

def test_different_contents_return_different_hashes(file_a, file_b):
    assert file_hash(file_a) != file_hash(file_b)

def test_same_content_different_files_returns_same_hash(file_a, file_a_copy):
    assert file_hash(file_a) == file_hash(file_a_copy)

def test_same_file_returns_same_hash(file_a):
    assert file_hash(file_a) == file_hash(file_a)
