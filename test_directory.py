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


def test_directory_argument_null(dylib):
    HelperClass.directory(dylib, None, ctypes.pointer(oper_id), Code.HASH_ERROR_ARGUMENT_NULL)
    assert oper_id.value == 0, "oper_id should be 0"
