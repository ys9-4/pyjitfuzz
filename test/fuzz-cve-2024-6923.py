# fuzz_cve_2024_6923.py
"""
CVE-2024-6923 퍼징: CPython email 모듈에서 Subject 헤더의 입력이
PyTypeObject 내부에 변화를 유도할 수 있는지 추적하는 퍼저.

이 버전은 probe_state() 해시값이 변화하면 "취약 가능성"을 탐지함.
"""

import atheris
import sys
import time
from email import message_from_string
from email.policy import default

# 🔐 이전 해시값 저장용
prev_hash = None

def TestOneInput(data: bytes):
    global prev_hash

    try:
        input_str = data.decode("utf-8", errors="ignore")

        email_template = f"""\
To: admin@vicarius.com
From: attacker@evil.com
Subject: {input_str}
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: quoted-printable
MIME-Version: 1.0

<html>
<body>
<p>This is a test.</p>
</body>
</html>
"""

        msg = message_from_string(email_template, policy=default)

        for header, value in list(msg.items()):
            del msg[header]
            msg[header] = value

        import builtins
        if hasattr(builtins, "probe_state"):
            current_hash = probe_state(msg)
            # print(current_hash)
            # print("Subject input:", repr(input_str))
            # time.sleep(1.0)

            # 🔍 해시값이 바뀌었을 때만 경고
            if prev_hash and current_hash != prev_hash:
                print("💥 TypeObject 내부 상태 변경 탐지됨 (해시 변화)")
            prev_hash = current_hash

    except Exception:
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()