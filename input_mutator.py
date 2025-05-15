import random
import string
import json

def generate_number() -> str:
    choice = random.random()
    if choice < 0.2:
        return str(round(random.uniform(-1e-12, 1e-12), 16))  # 0에 가까운 소수
    elif choice < 0.4:
        return str(round(random.uniform(-1e18, 1e18), 6))  # 아주 큰 소수/작은 소수
    elif choice < 0.6:
        return str(random.randint(-10**9, 10**9))  # 매우 큰 정수
    elif choice < 0.8:
        return str(random.randint(-1000, 1000))  # 일반적인 정수
    else:
        return str(round(random.uniform(-1e3, 1e3), random.randint(2, 8)))  # 적당한 소수

def generate_int() -> str:
    choice = random.random()
    if choice < 0.3:
        return str(random.randint(1, 3))  # 아주 작은 정수
    elif choice < 0.6:
        return str(random.randint(4, 100))  # 일반 크기 정수
    else:
        return str(random.randint(101, 1000000))  # 아주 큰 정수

def generate_string() -> str:
    length = random.randint(3, 64)
    unsafe = '"\'(){}\\'
    safe_chars = string.ascii_letters + string.digits + ''.join(c for c in string.punctuation if c not in unsafe)
    chars = ''.join(random.choices(safe_chars, k=length))
    return '"' + chars + '"'

def generate_old_from_str(s: str) -> str:
    content = s.strip('"')
    for c in '"\'(){}\\':
        content = content.replace(c, '')
    if not content:
        return '"a"'
    start = random.randint(0, len(content) - 1)
    end = random.randint(start + 1, min(len(content), start + random.randint(2, 8)))
    return '"' + content[start:end] + '"'

def generate_list() -> str:
    choice = random.random()
    if choice < 0.2:
        size = random.randint(1, 4)
    elif choice < 0.5:
        size = random.randint(5, 10)
    else:
        size = random.randint(16, 64)
    elements = [generate_number() if random.random() < 0.5 else generate_string() for _ in range(size)]
    return "[" + ", ".join(elements) + "]"

def generate_tuple() -> str:
    size = random.randint(2, 16)
    elements = [generate_number() for _ in range(size)]
    return "(" + ", ".join(elements) + ")"

def generate_dict() -> str:
    size = random.randint(2, 10)
    d = {generate_string(): generate_number() for _ in range(size)}
    return json.dumps(d)

def generate_strlist() -> str:
    size = random.randint(2, 20)
    items = [generate_string() for _ in range(size)]
    return "[" + ", ".join(items) + "]"

def generate_numlist() -> str:
    size = random.randint(2, 20)
    items = [generate_number() for _ in range(size)]
    return "[" + ", ".join(items) + "]"

def generate_bytes() -> str:
    size = random.randint(4, 16)
    b = bytes(random.randint(0, 255) for _ in range(size))
    return repr(b)

def generate_new_string() -> str:
    return generate_string()

def generate_date_string() -> str:
    year = random.randint(2000, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'"{year:04d}-{month:02d}-{day:02d}"'

def mutate_placeholders(code: str) -> str:
    generators = {
        "__NUM__": generate_number,
        "__INT__": generate_int,
        "__STR__": generate_string,
        "__LIST__": generate_list,
        "__TUPLE__": generate_tuple,
        "__DICT__": generate_dict,
        "__STRLIST__": generate_strlist,
        "__NUMLIST__": generate_numlist,
        "__BYTES__": generate_bytes,
        "__NEW__": generate_new_string,
        "__DATE__": generate_date_string,
    }

    str_value = generators["__STR__"]() if "__STR__" in code or "__OLD__" in code else None
    if str_value:
        code = code.replace("__STR__", str_value)
    if "__OLD__" in code:
        old_value = generate_old_from_str(str_value or generate_string())
        code = code.replace("__OLD__", old_value)
    if "__NEW__" in code:
        code = code.replace("__NEW__", generators["__NEW__"]())

    for placeholder, gen_func in generators.items():
        if placeholder in ("__STR__", "__OLD__", "__NEW__"):
            continue
        if placeholder in code:
            code = code.replace(placeholder, gen_func())

    return code
