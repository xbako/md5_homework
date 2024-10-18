import ctypes
import pytest
from test_parent import Code
from test_parent import HelperClass

@pytest.fixture(scope='module')
def dylib():
    dylib = HelperClass.init_lib()
    yield dylib


oper_id = ctypes.c_size_t(0)


def test_directory_too_soon(dylib):
    HelperClass.directory(dylib, b"./resources/files/empty", ctypes.pointer(oper_id), Code.HASH_ERROR_NOT_INITIALIZED)


def test_hash_status_too_soon(dylib):
    HelperClass.hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_NOT_INITIALIZED)


def test_next_log_line_too_soon(dylib):
    char_ptr = ctypes.c_char_p()
    result = dylib.HashReadNextLogLine(ctypes.pointer(char_ptr))
    assert result == Code.HASH_ERROR_NOT_INITIALIZED.value, "HashReadNextLogLine failed"


def test_stop_too_soon(dylib):
    HelperClass.stop(dylib, oper_id.value, Code.HASH_ERROR_NOT_INITIALIZED) ##FAIL HASH_ERROR_ARGUMENT_INVALID


def test_terminate_too_soon(dylib):
    HelperClass.terminate(dylib, Code.HASH_ERROR_NOT_INITIALIZED)


def test_init(dylib):
    HelperClass.init(dylib, Code.HASH_ERROR_OK)


def test_init_already_initialized(dylib):
    HelperClass.init(dylib, Code.HASH_ERROR_ALREADY_INITIALIZED) ##FAIL HASH_ERROR_OK


def test_terminate_sunny(dylib):
    HelperClass.terminate(dylib, Code.HASH_ERROR_OK)


def test_terminate_once_again(dylib):
    HelperClass.terminate(dylib, Code.HASH_ERROR_NOT_INITIALIZED)
