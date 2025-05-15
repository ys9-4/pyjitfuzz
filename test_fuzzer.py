import os
import sys
import subprocess
import atheris

from code_mutator import generate_code_template
from input_mutator import mutate_placeholders
from operation_mutator import mutate_operations

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
        if fname.startswith(prefix)
    ]
    existing_nums = [
        int(fname[len(prefix):])
        for fname in existing if fname[len(prefix):-len(extension)].isdigit()
    ]
    next_num = max(existing_nums + [0]) + 1
    return os.path.join(base_dir, f"{prefix}{next_num:04d}")

def save_case(code: str, output_jit: str, output_interp: str):
    filename = get_next_sample_filename("./check_sample")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("차이 발생! 입력 코드:\n")
        f.write(code + "\n\n")
        f.write("--- JIT ---\n")
        f.write(output_jit + "\n\n")
        f.write("--- INTERP ---\n")
        f.write(output_interp + "\n")

def TestOneInput(data: bytes):
    """
    fuzz function - generate, mutate, run, and compare JIT vs interpreter
    """
    try:
        code = generate_code_template()
        code = mutate_placeholders(code)
        code = mutate_operations(code)

        output_jit = run_python(code, jit_enabled=True)
        output_interp = run_python(code, jit_enabled=False)

        if "Error" in output_jit or "Warning" in output_jit:
            print("\n에러 발생")
            print(code)
            print(output_jit)

        if "값 변화 발생:" in output_jit or output_jit != output_interp:
            print("\n차이 발생! 입력 코드:")
            print(code)
            print("--- JIT ---")
            print(output_jit)
            print("--- INTERP ---")
            print(output_interp)
            save_case(code, output_jit, output_interp)

    except Exception:
        pass

atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
atheris.Fuzz()
