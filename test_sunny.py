import ctypes
import time
import pytest
from test_parent import Code
from test_parent import HelperClass


@pytest.fixture(scope='module')
def dylib():
    dylib = HelperClass.init_lib()
    yield dylib
    print("\n------------------------teardown------------------------")
    HelperClass.terminate(dylib, Code.HASH_ERROR_OK)


def test_init(dylib):
    HelperClass.init(dylib, Code.HASH_ERROR_OK)


oper_id = ctypes.c_size_t(0)


def test_directory(dylib):
    HelperClass.directory(dylib, b"./resources/files/identical_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)


def test_sunny(dylib):
    running = ctypes.c_bool(True)
    while dylib.HashStatus(oper_id, ctypes.byref(running)) == Code.HASH_ERROR_OK.value and running.value:
        pass  # Waiting for the operation to complete

    char_ptr = ctypes.c_char_p()

    while dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        print("\n", char_ptr.value.decode('utf-8'))  # print to stdout
        dylib.HashFree(char_ptr)
        time.sleep(0.1)


def test_stop(dylib):
    HelperClass.stop(dylib, oper_id.value, Code.HASH_ERROR_OK)
