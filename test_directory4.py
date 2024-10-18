import ctypes
import \
    time

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

########################################## INIT ######################################


def test_init(dylib):
    HelperClass().init(dylib, Code.HASH_ERROR_OK)


def test_directory_empty_log_empty(dylib):
    HelperClass().directory(dylib, b"./resources/files/empty", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    char_ptr = ctypes.c_char_p()
    result = dylib.HashReadNextLogLine(ctypes.pointer(char_ptr))
    assert char_ptr.value is None, "hash should not exist"
    assert result == Code.HASH_ERROR_LOG_EMPTY.value, "HashReadNextLogLine failed" ##FAIL HASH_ERROR_GENERAL


def test_stop_1(dylib):
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)


def test_next_line_argument_null(dylib):
    HelperClass().directory(dylib, b"resources/files/identical_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    result = dylib.HashReadNextLogLine(None)
    assert result == Code.HASH_ERROR_ARGUMENT_NULL.value, "HashReadNextLogLine failed"


def test_stop_2(dylib):
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)


def test_hash_status_argument_null(dylib):
    HelperClass().directory(dylib, b"resources/files/identical_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass().hashStatusWaiting(dylib, None, Code.HASH_ERROR_ARGUMENT_NULL) ##FAIL HASH_ERROR_OK


def test_stop_3(dylib):
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)


def test_hash_status_argument_invalid(dylib):
    HelperClass().directory(dylib, b"resources/files/identical_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    result = dylib.HashStatus(oper_id, b"invalid")
    assert result == Code.HASH_ERROR_ARGUMENT_INVALID.value, "HashStatus failed" ##FAIL HASH_ERROR_OK

def test_stop_4(dylib):
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)

def test_directory_argument_invalid(dylib):
    HelperClass().directory(dylib, b"./resources/files/identical_two", b"invalid", Code.HASH_ERROR_ARGUMENT_INVALID) ##FAIL HASH_ERROR_OK


def test_stop_5(dylib):
    time.sleep(2) # because previous test currently succeeds, I cannot use hashStatusWaiting
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)
