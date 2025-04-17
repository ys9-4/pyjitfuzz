# pyjitfuzz
CPython JIT Compiler Fuzzing - Capstone Project

## To-do
| implementation :thinking:

- atheris
    - compiled bytecode + data = new mutate bytecode
    - mutate bytecode must be needed python bytecode structures
    - ex) PUSH ARG1, PUSH ARG2, PUSH FUNC, CALL 2 = FUNC(ARG1, ARG2)

- cpython
    - add state builtin function
    - hash(PyStackFrame + Variables)