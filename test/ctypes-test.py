import ctypes

a = ctypes.c_int(10)
b = ctypes.c_int(20)

x = a.value + b.value
y = a.value * b.value
z = a.value - b.value

print("Add:", x, "Mul:", y, "Sub:", z)

