import os
import sys
import subprocess
import atheris

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
   

def add_state(code: bytes):     
    """
    add state function in harness code

    @param code: Harness code for fuzz
    @type code: int
    """
    pass


def TestOneInput(data: bytes):
    """
    fuzz function

    @param data: mutated bytes
    @type data: bytes
    """
    code = ""

    with open("harness/poc.py", "r") as f:
        code = f.read()

    add_state(code)

    output_jit = run_python(code, jit_enabled=True)
    output_interp = run_python(code, jit_enabled=False)

    if output_jit != output_interp:
        print("\n차이 발생! 입력 코드:")
        print(code)
        print("--- JIT ---")
        print(output_jit)
        print("--- INTERP ---")
        print(output_interp)
        raise RuntimeError("JIT/INTERP mismatch")

atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
atheris.Fuzz()