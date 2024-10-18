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
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    HelperClass().directory(dylib, b"resources/files/tree", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)
    HelperClass().directory(dylib, b"resources/files/different_two", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)
    HelperClass().hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)


def test_hashes_match_and_validated(dylib):
    hashh = ctypes.c_char_p()
    while dylib.HashReadNextLogLine(ctypes.pointer(hashh)) == Code.HASH_ERROR_OK.value:
        check_hash_free(dylib, hashh)


def check_hash_free(dylib, hashh):
    line = hashh.value.decode('utf-8')
    print("\nBEFORE HASHFREE", line)
    time.sleep(0.1)
    dylib.HashFree(hashh)
    line2 = hashh.value.decode('utf-8')
    print("\nAFTER HASHFREE", line2)
    assert line != line2, "hashes are different"


def test_stop(dylib):
    HelperClass().stop(dylib, oper_id.value, Code.HASH_ERROR_OK)
