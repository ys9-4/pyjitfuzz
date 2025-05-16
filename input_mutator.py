import random
import string
import json
import re

def clean_string(s: str) -> str:
    unsafe = '"\'(){}\\'
    return ''.join(c for c in s if c not in unsafe)

def generate_number() -> str:
    p = random.random()
    if p < 0.182:
        return str(round(random.uniform(-1e-12, 1e-12), random.randint(0, 10)))
    elif p < 0.182 * 2:
        return str(round(random.uniform(-1e18, 1e18), random.randint(0, 6)))
    elif p < 0.182 * 3:
        return str(random.randint(-2**31, 2**31 - 1))
    elif p < 0.182 * 4:
        return str(random.randint(-100000, 100000))
    elif p < 0.182 * 5:
        return str(round(random.uniform(-1e3, 1e3), random.randint(0, 8)))
    elif p < 0.182 * 5 + 0.03:
        return "float('nan')"
    elif p < 0.182 * 5 + 0.06:
        return "float('inf')"
    else:
        return "float('-inf')"

def generate_int() -> str:
    choice = random.randint(0, 5)
    if choice == 0:
        return str(random.randint(-100, 100))
    elif choice == 1:
        return str(random.randint(0, 100000))
    elif choice == 2:
        return str(random.randint(-100000, 0))
    elif choice == 3:
        return str(random.randint(100001, 10**18))
    elif choice == 4:
        return str(random.randint(-10**18, -100001))
    else:
        return str(random.randint(-2**63, 2**63 - 1))

def generate_string() -> str:
    length = random.randint(1, 32)
    chars = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    cleaned = clean_string(chars)
    return '"' + (cleaned if cleaned else "a") + '"'

def generate_old_from_str(s: str) -> str:
    content = clean_string(s.strip('"'))
    if len(content) < 2:
        return '"' + content + '"'
    start = random.randint(0, len(content) - 2)
    end = random.randint(start + 1, min(len(content), start + 8))
    return '"' + content[start:end] + '"'

def generate_list() -> str:
    size = random.randint(0, 10)
    elements = [generate_number() if random.random() < 0.5 else generate_string() for _ in range(size)]
    return "[" + ", ".join(elements) + "]"

def generate_tuple() -> str:
    size = random.randint(1, 8)
    elements = [generate_number() for _ in range(size)]
    return "(" + ", ".join(elements) + ")"

def generate_dict() -> str:
    size = random.randint(0, 5)
    d = {generate_string(): generate_number() for _ in range(size)}
    return json.dumps(d)

def generate_strlist() -> str:
    size = random.randint(0, 10)
    items = [generate_string() for _ in range(size)]
    return "[" + ", ".join(items) + "]"

def generate_numlist() -> str:
    size = random.randint(0, 10)
    items = [generate_number() for _ in range(size)]
    return "[" + ", ".join(items) + "]"

def generate_bytes() -> str:
    size = random.randint(0, 32)
    b = bytes(random.randint(0, 255) for _ in range(size))
    return repr(b)

def generate_date_string() -> str:
    year = random.randint(1900, 2100)
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
        "__NEW__": generate_string,
        "__DATE__": generate_date_string,
    }

    str_cache = generate_string() if "__STR__" in code or "__OLD__" in code else None

    if str_cache:
        code = re.sub(r"__STR__", lambda _: generate_string(), code)
    if "__OLD__" in code:
        code = re.sub(r"__OLD__", lambda _: generate_old_from_str(str_cache or generate_string()), code)
    if "__NEW__" in code:
        code = re.sub(r"__NEW__", lambda _: generate_string(), code)

    for key, func in generators.items():
        if key in ("__STR__", "__OLD__", "__NEW__"):
            continue
        if key in code:
            code = re.sub(re.escape(key), lambda _: func(), code)

    return code
