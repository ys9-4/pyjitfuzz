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

        print(output_jit)

        if output_jit != output_interp:
            print("\n차이 발생! 입력 코드:")
            print(code)
            print("--- JIT ---")
            print(output_jit)
            print("--- INTERP ---")
            print(output_interp)
            raise RuntimeError("JIT/INTERP mismatch")
    except Exception:
        pass

atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
atheris.Fuzz()
