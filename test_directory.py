import ctypes
import time

import pytest
from test_parent import Code
from test_parent import HelperClass


@pytest.fixture(scope='module')
def dylib():
    print("\n------------------------setup------------------------")
    lib_path = 'resources/bin/mac/libhash.dylib'
    dylib = ctypes.CDLL(lib_path)
    yield dylib
    print("\n------------------------teardown------------------------")
    HelperClass().terminate(dylib, Code.HASH_ERROR_OK)


oper_id = ctypes.c_size_t(0)


def test_init(dylib):
    HelperClass().init(dylib, Code.HASH_ERROR_OK)


def test_directory_tree(dylib): ##oper_id is 1
    HelperClass().directory(dylib, b"./resources/files/tree", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    HelperClass().nextLogLineLooping(dylib, expected_count_of_hashes=1)
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)


def test_directory_identical(dylib): ##oper_id is 2
    HelperClass().directory(dylib,b"resources/files/identical_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    HelperClass().nextLogLineLooping(dylib, expected_count_of_hashes=2)
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)


def test_next_line_overflow(dylib): ##oper_id is 3
    HelperClass().directory(dylib, b"resources/files/identical_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    char_ptr = ctypes.c_char_p()
    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        print("\n", char_ptr.value.decode('utf-8'))
        dylib.HashFree(char_ptr)
        time.sleep(0.1)
    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        print("\n", char_ptr.value.decode('utf-8'))
        dylib.HashFree(char_ptr)
        time.sleep(0.1)
    assert dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_LOG_EMPTY.value ##FAIL HASH_ERROR_GENERAL cekal bych lepsi


def test_stop(dylib):
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)
