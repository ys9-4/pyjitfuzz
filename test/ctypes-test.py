import ctypes
# import builtins  # 당신이 patch한 trace_stack 함수가 이 안에 있음


import inspect

def trace_stack():
    for frame_info in inspect.stack():
        print(f"Function: {frame_info.function}, File: {frame_info.filename}, Line: {frame_info.lineno}")

def inner():
    a = ctypes.c_int(10)
    b = ctypes.c_int(20)

    x = a.value + b.value
    y = a.value * b.value
    z = a.value - b.value

    print("Add:", x, "Mul:", y, "Sub:", z)

    trace_stack()  # <== 이걸 여기에 옮겨야 inner도 추적됨
    return x, y, z

def outer():
    results = inner()
    print("Results:", results)
    # builtins.trace_stack()  # 여기에 스택 프레임 이름이 출력됨

a = ctypes.c_int(10)
b = ctypes.c_int(20)

x = a.value + b.value
y = a.value * b.value
z = a.value - b.value

print("Add:", x, "Mul:", y, "Sub:", z)

trace_stack()  # <== 이걸 여기에 옮겨야 inner도 추적됨
