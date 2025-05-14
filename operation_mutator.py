import random
import re

# 함수 및 연산자 후보 정의
BUILTIN_FUNCS = ["abs", "len", "str", "float", "bool", "sorted", "repr", "hex", "bin"]
MATH_FUNCS = ["ceil", "floor", "sqrt", "log", "exp", "log1p", "fabs"]
STRING_FUNCS = ["upper", "lower", "strip", "capitalize", "title", "swapcase"]

BINOPS = ["+", "-", "*", "/", "//", "%", "**"]
UNOPS = ["-", "+", "~", "not"]
COMPS = ["==", "!=", "<", ">", "<=", ">="]

def mutate_operations(code: str) -> str:
    """
    템플릿 코드 내 __FUNC__, __BINOP__, __UNOP__, __COMP__ 등을 적절한 연산으로 대체
    """
    # 함수 처리
    if "math.__FUNC__" in code:
        code = code.replace("__FUNC__", random.choice(MATH_FUNCS))
    elif "'.__FUNC__()" in code:
        code = code.replace("__FUNC__", random.choice(STRING_FUNCS))
    elif "__FUNC__" in code:
        code = code.replace("__FUNC__", random.choice(BUILTIN_FUNCS))

    # 연산자 처리
    code = re.sub(r"__BINOP__", lambda _: random.choice(BINOPS), code)
    code = re.sub(r"__UNOP__", lambda _: random.choice(UNOPS), code)
    code = re.sub(r"__COMP__", lambda _: random.choice(COMPS), code)

    return code
