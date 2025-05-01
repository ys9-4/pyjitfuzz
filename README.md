# pyjitfuzz
CPython JIT Compiler Fuzzing - Capstone Project

## Note
execute `.py` file
```
parallels@ubuntu-linux-2404:~/workspace/cpython$ python3-jit ../pyjitfuzz/test.py 
<global>: [__name__ = '__main__', __doc__ = None, __package__ = None, __loader__ = <_frozen_importlib_external.SourceFileLoader object at 0xf38681631910>, __spec__ = None, __annotations__ = {}, __builtins__ = <module 'builtins' (built-in)>, __file__ = '/home/parallels/workspace/cpython/../pyjitfuzz/test.py', __cached__ = None, test = <function test at 0xf386816c31a0>, ]
<stack: code>: [<builtin_function_or_method at 0xf38681b8eb10>, 3, 2, 1]
<stack: code>: [<function at 0xf386816c31a0>]
<stack: NoneType>: [<dict at 0xf386816d4780>]
```

execute on interpreter
```
>>> def test(a, b):
...     c = a + b
...     state()
...     return c
...     
>>> test(1, 2)
<global>: [__name__ = '__main__', __doc__ = None, __package__ = '_pyrepl', __loader__ = <_frozen_importlib_external.SourceFileLoader object at 0xefa2ce266090>, __spec__ = ModuleSpec(name='_pyrepl.__main__', loader=<_frozen_importlib_external.SourceFileLoader object at 0xefa2ce266090>, origin='/home/parallels/workspace/cpython/Lib/_pyrepl/__main__.py'), __annotations__ = {}, __builtins__ = <module 'builtins' (built-in)>, __file__ = '/home/parallels/workspace/cpython/Lib/_pyrepl/__main__.py', __cached__ = '/home/parallels/workspace/cpython/Lib/_pyrepl/__pycache__/__main__.cpython-313.pyc', test = <function test at 0xefa2cdde5800>, ]
<stack: code>: [<builtin_function_or_method at 0xefa2ce39eb10>, 3, 2, 1]
<stack: code>: [<function at 0xefa2cdde5800>]
<stack: NoneType>: [<dict at 0xefa2ce234780>]
<stack: code>: [<builtin_function_or_method at 0xefa2ce39e200>, <code at 0xefa2ce1babf0>, <InteractiveColoredConsole at 0xefa2cdd75be0>]
<stack: code>: [<list_iterator at 0xefa2cdd68e20>, <nil>, <nil>, <code at 0xefa2ce1babf0>, <Interactive at 0xefa2cddfa810>, 'single', <type at 0xaad7b1e6b050>, <Expr at 0xefa2cddfa510>, <Expr at 0xefa2cddfa510>, <list at 0xefa2cdd61fc0>, <Module at 0xefa2cddfa490>, 'single', '<python-input-2>', 'test(1, 2)', <InteractiveColoredConsole at 0xefa2cdd75be0>]
<stack: code>: [<function at 0xefa2cdd714e0>, <nil>, 'test(1, 2)', 'single', '<python-input-2>', 'test(1, 2)', <InteractiveColoredConsole at 0xefa2cdd75be0>]
<stack: code>: [<function at 0xefa2cdd67e20>, <nil>, False, '<python-input-2>', 'test(1, 2)', '... ', '>>> ', <function at 0xefa2cdde53a0>, 2, <functools.partial at 0xefa2ce0435b0>, <function at 0xefa2cdddaf20>, 0, <cell at 0xefa2cddeffa0>]
<stack: code>: [<function at 0xefa2cdddb560>, <InteractiveColoredConsole at 0xefa2cdd75be0>, <function at 0xefa2cdddb560>, <type at 0xaad7b1f05260>, <nil>, <nil>, <nil>, None, <module at 0xefa2ce202520>, <dict at 0xefa2ce234780>, <nil>, False, False, None]
<stack: code>: [<function at 0xefa2cdde5120>]
<stack: NoneType>: [<dict at 0xefa2ce234780>]
<stack: code>: [<builtin_function_or_method at 0xefa2ce39e200>, '/home/parallels/workspace/cpython/Lib/_pyrepl/__pycache__/__main__.cpython-313.pyc', '/home/parallels/workspace/cpython/Lib/_pyrepl/__main__.py', <SourceFileLoader at 0xefa2ce266090>, None, '_pyrepl', <ModuleSpec at 0xefa2cdde5090>, '__main__', None, <dict at 0xefa2ce234780>, <code at 0xefa2ce054c30>]
<stack: code>: [<function at 0xefa2cdde4900>, <dict at 0xefa2ce234780>, <nil>, <nil>, <code at 0xefa2ce054c30>, <ModuleSpec at 0xefa2cdde5090>, False, '_pyrepl.__main__']
<stack: NoneType>: [<(null) at 0xfffff1967c20>]
3
```

## Issues
| something problems.. :thinking:

- cpython 
    - state function occurs segmentation fault (wtf :sad:)

## To-do
| implementation :thinking:

- atheris
    - compiled bytecode + data = new mutate bytecode
    - mutate bytecode must be needed python bytecode structures
    - ex) PUSH ARG1, PUSH ARG2, PUSH FUNC, CALL 2 = FUNC(ARG1, ARG2)

- cpython
    - add state builtin function
    - hash(PyStackFrame + Variables)