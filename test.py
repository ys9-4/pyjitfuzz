def test(a, b):
    c = a + b
    state()
    return c


def test2(a, b):
    c = a[0] + b[0]
    state()
    return c

test(1, 2)
test2([1, 1, 1], [2, 2, 2])