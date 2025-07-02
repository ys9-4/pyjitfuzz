import os
import sys
import time
import subprocess
import atheris
import signal
import atexit
import pyfiglet
import shutil


from code_mutator import generate_code_template
from input_mutator import mutate_placeholders
from operation_mutator import mutate_operations

execution_counter = 0 

def handle_signal(signum, frame):
    print(f"\n총 실행된 테스트 횟수: {execution_counter}\n")
    os._exit(0)

def on_exit():
    print(f"\n총 실행된 테스트 횟수: {execution_counter}\n")

def run_python(code: str, jit_enabled: bool) -> str:
    env = os.environ.copy()
    env["PYTHON_JIT"] = "1" if jit_enabled else "0"

    try:
        result = subprocess.run(
            ["python3.13", "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            timeout=10
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def get_next_sample_filename(base_dir: str, prefix: str = "check_code", extension: str = "") -> str:
    os.makedirs(base_dir, exist_ok=True)
    existing = [
        fname for fname in os.listdir(base_dir)
        if fname.startswith(prefix) and fname[len(prefix):].isdigit()
    ]
    existing_nums = [int(fname[len(prefix):]) for fname in existing]
    next_num = max(existing_nums + [0]) + 1
    return os.path.join(base_dir, f"{prefix}{next_num:04d}{extension}")

def save_case(code: str, output_jit: str, output_interp: str):
    filename = get_next_sample_filename("./check_sample")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code + "\n\n")
        f.write("--- JIT ---\n")
        f.write(output_jit + "\n\n")
        f.write("--- INTERP ---\n")
        f.write(output_interp + "\n")

def TestOneInput(data: bytes):
    global execution_counter
    try:
        execution_counter += 1
        code = generate_code_template()
        code = mutate_placeholders(code)
        code = mutate_operations(code)

        output_jit = run_python(code, jit_enabled=True)
        output_interp = run_python(code, jit_enabled=False)

        # if "Error" in output_jit or "Warning" in output_jit:
        #     # print("\n에러 발생")
        #     # print(code)
        #     # print(output_jit)

        if "값 변화 발생:" in output_jit or output_jit != output_interp:
            # print("\n차이 발생! 입력 코드:")
            # print(code)
            # print("--- JIT ---")
            # print(output_jit)
            # print("--- INTERP ---")
            # print(output_interp)
            save_case(code, output_jit, output_interp)

    except Exception as e:
        pass

def slow_print(text, delay=0.05, center=True):
    """색상 코드 제외한 중앙 정렬 slow print"""
    import re
    term_width = shutil.get_terminal_size((80, 20)).columns

    # ANSI escape code 제거용 정규식
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    plain_text = ansi_escape.sub('', text)

    if center:
        padding = (term_width - len(plain_text)) // 2
        sys.stdout.write(" " * padding)

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def framed_banner_centered(text: str, font="slant", padding=1):
    """중앙 정렬된 아스키 아트 배너 + 박스 테두리"""
    rendered = pyfiglet.figlet_format(text, font=font)
    lines = rendered.splitlines()
    content_width = max(len(line) for line in lines) + padding * 2
    term_width = shutil.get_terminal_size((80, 20)).columns
    box_margin = max((term_width - content_width) // 2, 0)
    pad = " " * padding

    top = "╔" + "═" * content_width + "╗"
    bottom = "╚" + "═" * content_width + "╝"

    print(" " * box_margin + top)
    for line in lines:
        content = "║" + pad + line.ljust(content_width - padding * 2) + pad + "║"
        print(" " * box_margin + content)
    print(" " * box_margin + bottom)

def print_banner():
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    print(GREEN, end="")
    framed_banner_centered("pyjitfuzz", font="slant", padding=4)
    print(RESET, end="")

    time.sleep(0.5)
    slow_print(f"{CYAN}2024 PNU Project{RESET}")
    time.sleep(0.3)
    slow_print(f"{BOLD}Team HongBoSeok{RESET}")
    time.sleep(0.3)
    slow_print(f"{BOLD}ys9-4, seonHH, ehdrjs6831{RESET}")
    time.sleep(1)

    # 구분선 중앙 정렬
    term_width = shutil.get_terminal_size((80, 20)).columns
    print(("-" * 50).center(term_width))

def main():
    print_banner()
    atexit.register(on_exit)
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)


    atheris.Fuzz()

if __name__ == "__main__":
    main()