# fuzz_cve_2024_6923.py

import atheris              # Google의 퍼징 도구인 Atheris를 불러옴
import sys                  # 시스템 관련 모듈 (실행 인자 등 사용)
from email import message_from_string  # 문자열로 이메일을 파싱하는 함수
from email.policy import default       # 이메일 파서의 기본 설정

def TestOneInput(data: bytes):
    try:
        # 퍼저가 준 바이트 데이터를 문자열로 변환함 (utf-8로 해석, 에러는 무시)
        input_str = data.decode("utf-8", errors="ignore")

        # 이메일 형식의 문자열을 만듦 (Subject 헤더에 퍼저가 만든 입력을 삽입함)
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

        # 이메일 문자열을 실제 email 객체로 파싱함
        msg = message_from_string(email_template, policy=default)

        # 파싱된 헤더들을 다시 설정함 (여기서 문제가 발생할 수 있음)
        for header, value in list(msg.items()):
            del msg[header]
            msg[header] = value

        # 메시지를 다시 문자열로 변환함 (변경된 헤더 포함)
        email_out = str(msg)

        # 🔍 probe_state 함수가 CPython에 추가되어 있다면, msg 객체 상태를 해시로 출력
        import builtins
        if hasattr(builtins, "probe_state"):
            print(probe_state(msg))  # 해시 출력 (타입 내부 정보 추적용)

        # 📛 만약 헤더 중에 Bcc가 숨어서 삽입되었으면 취약하다고 판단하고 예외 발생
        if "\nBcc:" in email_out:
            raise RuntimeError("💥 Detected inserted Bcc header!")

    except Exception:
        pass  # 예외는 무시하고 계속 진행 (퍼징은 실패도 일종의 결과임)

def main():
    # Atheris에 퍼징 함수와 설정 전달
    atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)

    # 퍼징 시작 (무한 루프처럼 동작함)
    atheris.Fuzz()

if __name__ == "__main__":
    main()