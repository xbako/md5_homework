# md5_homework

Seznam bugů: 

test_initialization.py
1. Volání HashStop před HashInit vrací HASH_ERROR_ARGUMENT_INVALID. Očekávál jsem HASH_ERROR_NOT_INITIALIZED
2. Volání HashInit po HashInit vrací HASH_ERROR_OK. Očekávál jsem HASH_ERROR_ALREADY_INITIALIZED

test_stop_directory.py
1. Volání HashStop před HashDirectory vrací HASH_ERROR_ARGUMENT_INVALID. Očekávál jsem něco jiného
2. Volání HashStop po HashStop vrací HASH_ERROR_ARGUMENT_INVALID. Očekávál jsem něco jiného

test_directory_next_line.py
1. Opakovaně jsem volal HashReadNextLogLine s HashFree, měl jsem překročit maximální počet řádků, a HashReadNextLogLine v návratu vracel HASH_ERROR_GENERAL. Očekával jsem HASH_ERROR_LOG_EMPTY.

test_directory_hash_status_next_line.py
1. Doptával jsem se s HashDirectory na adresář, který byl prázný. Pak jsem sledoval log přes HashReadNextLogLine a vracel HASH_ERROR_GENERAL. Očekával jsem HASH_ERROR_LOG_EMPTY.
2. Volal jsem HashStatus s operation_id None a vracel HASH_ERROR_OK. Očekával jsem HASH_ERROR_ARGUMENT_NULL.
3. Volal jsem HashStatus s invalidným druhým argumentem a vracel HASH_ERROR_OK. Očekával jsem HASH_ERROR_ARGUMENT_INVALID.
4. Volal jsem HashDirectory a místo druhého argumentu jsem posílal invalidní argument a vracel HASH_ERROR_OK. Očekával jsem HASH_ERROR_ARGUMENT_INVALID.

test_hash_output_random_input.py
1. Test generuje random inputt text, který dále použit pro MD5 hashování. Jednou se input hashoval přes knihovnu hashlib a jindy přes testovanou dylib knihovnu. Výsledky se lišily, dylib výsledkům chybí určité 0, ale ne pokaždé. 
