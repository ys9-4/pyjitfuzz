import random
from typing import List, Dict

def generate_templates() -> List[Dict]:
    return [
        # 내장 함수
        {"template": "__FUNC__(__NUM__)", "imports": [], "category": "builtin-func", "weight": 1},
        {"template": "math.__FUNC__(__NUM__)", "imports": ["math"], "category": "math", "weight": 1},

        # 문자열 메서드
        {"template": "__STR__.__FUNC__()", "imports": [], "category": "string", "weight": 1},
        {"template": "__STR__.replace(__OLD__, __NEW__)", "imports": [], "category": "string", "weight": 1},

        # 연산자
        {"template": "(__NUM__) __BINOP__ (__NUM__)", "imports": [], "category": "binary-op", "weight": 1},
        {"template": "__UNOP__ (__NUM__)", "imports": [], "category": "unary-op", "weight": 1},
        {"template": "(__NUM__) __COMP__ (__NUM__)", "imports": [], "category": "compare", "weight": 1},

        # 조건문
        {"template": "x = __NUM__\ny = __NUM__\nresult = x if x > y else y", "imports": [], "category": "control", "weight": 1},
        {"template": "x = __NUM__\nif x > 0:\n    result = x * 2\nelse:\n    result = -x", "imports": [], "category": "branching", "weight": 2},
        {"template": "s = __STR__\nif isinstance(s, str):\n    result = len(s)\nelse:\n    result = -1", "imports": [], "category": "type-check", "weight": 2},
        {"template": "try:\n    x = int(__STR__)\n    result = x * 2\nexcept ValueError:\n    result = -1\nelse:\n    result += 1", "imports": [], "category": "exception-branch", "weight": 2},
        {"template": "x = __INT__\nmatch x:\n    case 1:\n        result = 'one'\n    case 2:\n        result = 'two'\n    case _:\n        result = 'other'", "imports": [], "category": "pattern-match", "weight": 1},
        {"template": "x = __NUM__\nif x > __INT__:\n    if x % 2 == 0:\n        result = x // 2\n    else:\n        result = x * 3\nelse:\n    result = -x", "imports": [], "category": "nested-if", "weight": 2},

        # 반복문
        {"template": "acc = 0\nfor i in range(__UINT_SMALL__):\n    acc += __NUM__\nresult = acc", "imports": [], "category": "loop", "weight": 1},
        {"template": "[i * __NUM__ for i in range(__UINT_SMALL__)]", "imports": [], "category": "loop", "weight": 1},

        # JSON
        {"template": "json.loads(__STR__)", "imports": ["json"], "category": "json", "weight": 1},
        {"template": "json.dumps(__DICT__)", "imports": ["json"], "category": "json", "weight": 1},
        {"template": "json.dumps(__LIST__, indent=4)", "imports": ["json"], "category": "json", "weight": 1},

        # struct
        {"template": "struct.unpack('<I', __BYTES__)[0]", "imports": ["struct"], "category": "binary", "weight": 1},

        # ctypes
        {"template": "ctypes.c_int(__INT__).value", "imports": ["ctypes"], "category": "ctypes", "weight": 1},
        {"template": "ctypes.c_double(__NUM__).value", "imports": ["ctypes"], "category": "ctypes", "weight": 1},
        {"template": "ctypes.pointer(ctypes.c_int(__UINT__))", "imports": ["ctypes"], "category": "ctypes", "weight": 1},
        {"template": "nums = __NUMLIST__\nArrayType = ctypes.c_double * len(eval(nums))\narr = ArrayType(*eval(nums))\nresult = arr[1]", "imports": ["ctypes"], "category": "ctypes", "weight": 1},

        # 수학/통계
        {"template": "statistics.mean(__NUMLIST__)", "imports": ["statistics"], "category": "statistics", "weight": 1},
        {"template": "decimal.Decimal(__STR__)", "imports": ["decimal"], "category": "numeric", "weight": 1},
        {"template": "decimal.Decimal(str(__NUM__))", "imports": ["decimal"], "category": "numeric", "weight": 1},
        {"template": "fractions.Fraction(__STR__)", "imports": ["fractions"], "category": "numeric", "weight": 1},
        {"template": "fractions.Fraction(str(__NUM__))", "imports": ["fractions"], "category": "numeric", "weight": 1},
        {"template": "datetime.datetime.strptime(__DATE__, '%Y-%m-%d')", "imports": ["datetime"], "category": "datetime", "weight": 1},
        {"template": "functools.reduce(lambda x, y: x + y, __NUMLIST__)", "imports": ["functools"], "category": "functional", "weight": 1},

        # 조합 관련
        {"template": "result = list(itertools.combinations(__STRLIST__, __UINT__))", "imports": ["itertools"], "category": "combinatorics", "weight": 1},
        {"template": "result = list(itertools.combinations(__NUMLIST__, __UINT__))", "imports": ["itertools"], "category": "combinatorics", "weight": 1},

        # 시스템
        {"template": "platform.machine()", "imports": ["platform"], "category": "system", "weight": 1},
        {"template": "sys.getsizeof(__DICT__)", "imports": ["sys"], "category": "system", "weight": 1},

        # 컬렉션
        {"template": "list(set(__LIST__))", "imports": [], "category": "collection", "weight": 1},
        {"template": "dict([(__STR__, __NUM__), (__STR__, __NUM__)])", "imports": [], "category": "collection", "weight": 1},
        {"template": "sorted(set(__LIST__))", "imports": [], "category": "collection", "weight": 1},
        {"template": "len(set(__LIST__))", "imports": [], "category": "collection", "weight": 1},

        # 비교 연산 확장
        {"template": "x = __NUM__\nresult = 1 < x < 100", "imports": [], "category": "compare-chain", "weight": 1},

        # 비트 연산
        {"template": "result = __UINT__ & __UINT__", "imports": [], "category": "bitwise", "weight": 1},
        {"template": "result = __UINT__ | __UINT__", "imports": [], "category": "bitwise", "weight": 1},
        {"template": "result = __UINT__ ^ __UINT__", "imports": [], "category": "bitwise", "weight": 1},
        {"template": "result = __UINT__ << __UINT__", "imports": [], "category": "bitwise", "weight": 1},
        {"template": "result = __UINT__ >> __UINT__", "imports": [], "category": "bitwise", "weight": 1},

        # 내부 접근 / 슬라이싱
        {"template": "lst = __LIST__\nresult = lst[0] if lst else None", "imports": [], "category": "list-index", "weight": 1},
        {"template": "d = {'key': __NUM__}\nresult = d.get('key', -1)", "imports": [], "category": "dict-access", "weight": 1},
        {"template": "s = __STR__\nresult = s[1:-1]", "imports": [], "category": "slice", "weight": 1},
        {"template": "nums = __NUMLIST__\nresult = nums[::-1]", "imports": [], "category": "slice", "weight": 1},

        # 사용자 정의 함수 및 클래스
        {"template": "def add(x, y):\n    return x + y\nresult = add(__NUM__, __NUM__)", "imports": [], "category": "user-func", "weight": 1},
        {"template": "class Point:\n    def __init__(self, x):\n        self.x = x\n    def double(self):\n        return self.x * 2\nresult = Point(__NUM__).double()", "imports": [], "category": "user-class", "weight": 1},

        # 메모리 버퍼 관련
        {"template": "b = bytearray(__BYTES__)\nresult = memoryview(b)[0]", "imports": [], "category": "buffer", "weight": 1},

        # 제너레이터와 반복자
        {"template": "def gen():\n    for i in range(3):\n        yield i\ng = gen()\nresult = next(g)", "imports": [], "category": "generator", "weight": 1},

        # 클로저 및 nonlocal
        {"template": "def outer():\n    x = __NUM__\n    def inner():\n        return x + 1\n    return inner()\nresult = outer()", "imports": [], "category": "closure", "weight": 1},
        {"template": "def make_counter():\n    count = 0\n    def inc():\n        nonlocal count\n        count += 1\n        return count\n    return inc()\nresult = make_counter()", "imports": [], "category": "nonlocal", "weight": 1},
        {"template": "result = (lambda x: x + 5)(__NUM__)", "imports": [], "category": "lambda", "weight": 1}
    ]


def generate_code_template() -> str:
    templates = generate_templates()
    weights = [entry["weight"] for entry in templates]
    entry = random.choices(templates, weights=weights, k=1)[0]

    code_body = entry["template"]
    imports = entry["imports"]
    result_var = f"res{random.randint(1000, 9999)}"
    import_lines = "\n".join(f"import {imp}" for imp in sorted(set(imports)))

    if "\n" in code_body or "result =" in code_body:
        body_code = code_body.strip()
        return_stmt = "\n        return result" if "result =" in code_body else ""
        if not body_code:
            body_code = "pass"
        indented_code = "\n".join("        " + line for line in body_code.splitlines())
        code_block = f"{indented_code}{return_stmt}"
    else:
        code_block = f"        {result_var} = {code_body}\n        return {result_var}"

    full_template = f"""
# === setup ===
{import_lines}

def target():
    try:
{code_block}
    except Exception as e:
        return ""

tmp = target()
prev = probe_state(tmp)
print(prev)
for _ in range(100):
    tmp = target()
    curr = probe_state(tmp)
    print(curr)
    if curr != prev:
        print("값 변화 발생:", prev, "→", curr)
    prev = curr
"""
    return full_template.strip()
