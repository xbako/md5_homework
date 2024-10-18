import time
import ctypes
import enum

class HelperClass:

    def terminate(self, dylib, expected_result):
        result = dylib.HashTerminate()
        assert result == expected_result.value, "HashTerminate failed"

    def init(self, dylib, expected_result):
        result = dylib.HashInit()
        assert result == expected_result.value, "HashInit failed"

    def directory(self, dylib, path, id_ptr, expected_result):
        result = dylib.HashDirectory(path, id_ptr)
        assert result == expected_result.value, "HashDirectory failed"

    def hashStatusWaiting(self, dylib, oper_id, expected_result):
        running = ctypes.c_bool(True)
        result = dylib.HashStatus(oper_id, ctypes.byref(running))
        assert result == expected_result.value, "HashStatus failed"
        while dylib.HashStatus(oper_id, ctypes.byref(running)) == Code.HASH_ERROR_OK.value and running.value:
            pass  # Waiting for the operation to complete

    def nextLogLineLooping(self, dylib: object, expected_count_of_hashes: object) -> object:
        char_ptr = ctypes.c_char_p()
        iteration_count = 0
        while dylib.HashReadNextLogLine(ctypes.pointer(char_ptr)) == Code.HASH_ERROR_OK.value:
            print("\n", char_ptr.value.decode('utf-8'))  # print to stdout
            # dylib.HashFree(char_ptr)
            time.sleep(0.1)
            iteration_count += 1

        assert iteration_count == expected_count_of_hashes, "Number of lines does not match the count of directories."

    def stop(self, dylib, oper_id, expected_result):
        print("\nSTOP ->", oper_id)
        result = dylib.HashStop(oper_id)
        assert result == expected_result.value, "HashStop failed"


class Code(enum.Enum):
    HASH_ERROR_OK = 0
    HASH_ERROR_GENERAL = 1
    HASH_ERROR_EXCEPTION = 2
    HASH_ERROR_MEMORY = 3
    HASH_ERROR_LOG_EMPTY = 4
    HASH_ERROR_ARGUMENT_INVALID = 5
    HASH_ERROR_ARGUMENT_NULL = 6
    HASH_ERROR_NOT_INITIALIZED = 7
    HASH_ERROR_ALREADY_INITIALIZED = 8
