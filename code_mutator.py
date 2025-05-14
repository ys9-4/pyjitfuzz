import random
from typing import List, Tuple, Dict

def generate_templates() -> List[Dict]:
    return [
        # 내장 함수
        {"template": "__FUNC__(__NUM__)", "imports": [], "category": "builtin-func", "weight": 1},
        {"template": "math.__FUNC__(__NUM__)", "imports": ["math"], "category": "math", "weight": 1},

        # 문자열 메서드
        {"template": "__STR__.__FUNC__()", "imports": [], "category": "string", "weight": 1},
        {"template": "__STR__.replace(__OLD__, __NEW__)", "imports": [], "category": "string", "weight": 1},

        # 연산자
        {"template": "__NUM__ __BINOP__ __NUM__", "imports": [], "category": "binary-op", "weight": 1},
        {"template": "__UNOP__ __NUM__", "imports": [], "category": "unary-op", "weight": 1},
        {"template": "__NUM__ __COMP__ __NUM__", "imports": [], "category": "compare", "weight": 1},

        # 조건문
        {"template": "x = __NUM__\ny = __NUM__\nresult = x if x > y else y", "imports": [], "category": "control", "weight": 1},

        # 반복문
        {"template": "acc = 0\nfor i in range(10):\n    acc += __NUM__\nresult = acc", "imports": [], "category": "loop", "weight": 1},

        # JSON
        {"template": "json.loads(__STR__)", "imports": ["json"], "category": "json", "weight": 1},
        {"template": "json.dumps(__DICT__)", "imports": ["json"], "category": "json", "weight": 1},
        {"template": "json.dumps(__LIST__, indent=4)", "imports": ["json"], "category": "json", "weight": 1},

        # struct
        {"template": "struct.unpack('<I', __BYTES__)[0]", "imports": ["struct"], "category": "binary", "weight": 1},

        # ctypes
        {"template": "ctypes.c_int(__NUM__).value", "imports": ["ctypes"], "category": "ctypes", "weight": 1},
        {"template": "ctypes.c_double(__NUM__).value", "imports": ["ctypes"], "category": "ctypes", "weight": 1},
        {"template": "ctypes.pointer(ctypes.c_int(__NUM__))", "imports": ["ctypes"], "category": "ctypes", "weight": 1},
        {"template": "(ctypes.c_int * 3)(*__NUMLIST__)[1]", "imports": ["ctypes"], "category": "ctypes", "weight": 1},

        # 수학/통계
        {"template": "statistics.mean(__NUMLIST__)", "imports": ["statistics"], "category": "statistics", "weight": 1},
        {"template": "decimal.Decimal(__STR__)", "imports": ["decimal"], "category": "numeric", "weight": 1},
        {"template": "fractions.Fraction(__STR__)", "imports": ["fractions"], "category": "numeric", "weight": 1},
        {"template": "datetime.datetime.strptime(__DATE__, '%Y-%m-%d')", "imports": ["datetime"], "category": "datetime", "weight": 1},
        {"template": "functools.reduce(lambda x, y: x + y, __NUMLIST__)", "imports": ["functools"], "category": "functional", "weight": 1},

        # 조합 관련
        {"template": "list(itertools.combinations(__STRLIST__, __INT__))", "imports": ["itertools"], "category": "combinatorics", "weight": 1},

        # 시스템
        {"template": "platform.machine()", "imports": ["platform"], "category": "system", "weight": 1},
        {"template": "sys.getsizeof(__DICT__)", "imports": ["sys"], "category": "system", "weight": 1},

        # 컬렉션
        {"template": "list(set(__LIST__))", "imports": [], "category": "collection", "weight": 1},
        {"template": "dict(__LIST__)", "imports": [], "category": "collection", "weight": 1},
        {"template": "sorted(set(__LIST__))", "imports": [], "category": "collection", "weight": 1},
        {"template": "len(set(__LIST__))", "imports": [], "category": "collection", "weight": 1},

        # 리스트 내포
        {"template": "[i * __NUM__ for i in range(10)]", "imports": [], "category": "loop", "weight": 1}
    ]


def generate_code_template() -> str:
    """
    템플릿과 관련된 import 목록을 기반으로 코드 생성
    category 및 placeholder 구조 유지, try-catch 포함
    """
    templates = generate_templates()
    weights = [entry["weight"] for entry in templates]
    entry = random.choices(templates, weights=weights, k=1)[0]

    code_body = entry["template"]
    imports = entry["imports"]
    result_var = f"res{random.randint(1000, 9999)}"
    import_lines = "\n".join(f"import {imp}" for imp in sorted(set(imports)))

    if "\n" in code_body or "result =" in code_body:
        body_code = code_body
        return_stmt = "\n        return result" if "result =" in code_body else ""
        code_block = f"{body_code}{return_stmt}"
    else:
        code_block = f"{result_var} = {code_body}\n        return {result_var}"

    full_template = f"""
# === setup ===
{import_lines}

def target():
    try:
        {code_block}
    except Exception as e:
        return f"error: {{type(e).__name__}}"

for _ in range(100):
    probe_state(target())
"""
    return full_template.strip()

