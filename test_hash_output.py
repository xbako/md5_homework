#test_hash_library.py
import ctypes
import time

import pytest
from test_parent import \
    Code, \
    HelperClass
import hashlib


@pytest.fixture(scope='module')
def dylib():
    print("\n------------------------setup------------------------")
    lib_path = 'resources/bin/mac/libhash.dylib'
    dylib = ctypes.CDLL(lib_path)
    yield dylib
    print("\n------------------------teardown------------------------")
    HelperClass().terminate(dylib, Code.HASH_ERROR_OK)

def test_init(dylib):
    HelperClass().init(dylib, Code.HASH_ERROR_OK)

oper_id = ctypes.c_size_t(0)
def test_directory_identical(dylib):
    HelperClass().directory(dylib, b"resources/files/identical_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)

def test_hashes_match_and_validated(dylib):
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)

    char_ptr = ctypes.c_char_p()

    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        first_hash = char_ptr.value.decode('utf-8')  # print to stdout
        dylib.HashFree(char_ptr)
        time.sleep(0.1)

    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        second_hash = char_ptr.value.decode('utf-8')  # print to stdout
        dylib.HashFree(char_ptr)
        time.sleep(0.1)

    assert first_hash.split()[-1] == second_hash.split()[-1], "identical files have different hash"
    assert first_hash.split()[0] == second_hash.split()[0], "operation id of siblings files are different"

    text_of_first_file = open(
        "resources/files/identical_two/first.txt", "r").read()
    print("\ndylib MD5 hash:", first_hash.split()[-1])
    print("valid MD5 hash:", get_md5_hash(text_of_first_file).upper())
    assert first_hash.split()[-1] == get_md5_hash(text_of_first_file).upper(), "MD5 hash is not valid"

def test_directory_identical_but_blank(dylib):
    HelperClass().directory(dylib, b"resources/files/identical_two_blank", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)

def test_hashes_match_and_validated_blank_files(dylib):
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)

    char_ptr = ctypes.c_char_p()

    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        first_hash = char_ptr.value.decode('utf-8')  # print to stdout
        dylib.HashFree(char_ptr)
        time.sleep(0.1)

    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        second_hash = char_ptr.value.decode('utf-8')  # print to stdout
        dylib.HashFree(char_ptr)
        time.sleep(0.1)

    assert first_hash.split()[-1] == second_hash.split()[-1], "identical files have different hash"
    assert first_hash.split()[0] == second_hash.split()[0], "operation id of siblings files are different"

    text_of_first_file = open(
        "resources/files/identical_two_blank/first.txt", "r").read()
    print("\ndylib MD5 hash", first_hash.split()[-1])
    print("valid MD5 hash", get_md5_hash(text_of_first_file).upper())
    assert first_hash.split()[-1] == get_md5_hash(text_of_first_file).upper(), "MD5 hash is not valid"

def test_directory_different(dylib):
    HelperClass().directory(dylib, b"resources/files/different_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)

def test_hashes_different(dylib):
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)

    char_ptr = ctypes.c_char_p()

    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        first_hash = char_ptr.value.decode('utf-8')  # print to stdout
        dylib.HashFree(char_ptr)
        time.sleep(0.1)

    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        second_hash = char_ptr.value.decode('utf-8')  # print to stdout
        dylib.HashFree(char_ptr)
        time.sleep(0.1)

    assert first_hash.split()[-1] != second_hash.split()[-1], "different files have identical hash"
    assert first_hash.split()[0] == second_hash.split()[0], "operation id of siblings files are different"

def test_stop(dylib):
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)

def get_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()
