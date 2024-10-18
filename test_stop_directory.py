import ctypes
import pytest
from test_parent import Code
from test_parent import HelperClass


@pytest.fixture(scope='module')
def dylib():
    dylib = HelperClass.init_lib()
    yield dylib
    print("\n------------------------teardown------------------------")
    HelperClass.terminate(dylib, Code.HASH_ERROR_OK)


oper_id = ctypes.c_size_t(0)


def test_init(dylib):
    HelperClass.init(dylib, Code.HASH_ERROR_OK)


def test_stop_before_directory(dylib):
    HelperClass.stop(dylib, oper_id.value, Code.HASH_ERROR_GENERAL) ##FAIL HASH_ERROR_ARGUMENT_INVALID, cekal bych jinou hlasku


def test_directory_ok(dylib):
    HelperClass.directory(dylib, b"./resources/files/identical_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass.hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)


def test_stop_after_directory(dylib):
    HelperClass.stop(dylib, oper_id.value, Code.HASH_ERROR_OK)


def test_stop_once_again(dylib):
    HelperClass.stop(dylib, oper_id.value, Code.HASH_ERROR_GENERAL) ##FAIL HASH_ERROR_ARGUMENT_INVALID, cekal bych jinou hlasku
