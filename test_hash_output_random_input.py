#test_hash_library.py
import ctypes
import time

import pytest
from test_parent import \
    Code, \
    HelperClass
import hashlib
import random
import string


@pytest.fixture(scope='module')
def dylib():
    dylib = HelperClass.init_lib()
    yield dylib
    print("\n------------------------teardown------------------------")
    HelperClass.terminate(dylib, Code.HASH_ERROR_OK)


def test_init(dylib):
    HelperClass.init(dylib, Code.HASH_ERROR_OK)
    open("resources/files/random_input_files/first.txt", "w").write(generate_random_string())
    HelperClass.directory(dylib, b"./resources/files/random_input_files", ctypes.pointer(oper_id), Code.HASH_ERROR_OK)


oper_id = ctypes.c_size_t(0)


def test_random_input_md5_validation(dylib):
    HelperClass.hashStatusWaiting(dylib, oper_id, Code.HASH_ERROR_OK)

    char_ptr = ctypes.c_char_p()

    if dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
        first_hash = char_ptr.value.decode('utf-8')
        dylib.HashFree(char_ptr)
        time.sleep(0.1)

    text_of_first_file = open("resources/files/random_input_files/first.txt", "r").read()
    print("\ndylib MD5 hash:", first_hash.split()[-1])
    print("valid MD5 hash:", get_md5_hash(text_of_first_file).upper())
    assert first_hash.split()[-1] == get_md5_hash(text_of_first_file).upper(), "MD5 hash is not valid"

def test_stop(dylib):
    HelperClass.stop(dylib, oper_id.value, Code.HASH_ERROR_OK)


def get_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()

def generate_random_string(length=12):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))
