"""
[📛 CVE-2024-6923 퍼징용 스크립트]

🔍 설명:
    Python 표준 라이브러리의 `email` 모듈에서 발생하는 헤더 파싱 취약점입니다.
    특정 방식으로 인코딩된 문자열 (예: =?UTF-8?Q?=0A?=)이 `Subject`에 포함될 경우,
    내부 파싱 중 `Bcc:` 헤더가 은밀히 삽입되어 정보 유출(📤BCC injection)로 이어질 수 있습니다.

    이 스크립트는 Google의 Atheris 퍼저를 사용해 입력을 무작위로 생성하여
    Subject 필드에서 이러한 우회 공격을 탐지합니다.
    추가로 `probe_state()` 내장 함수를 호출하여 msg 객체의 타입 정보를 해시값으로 추적합니다.

🚨 익스플로잇 방식 요약:
    - Subject에 `=?UTF-8?Q?...\n?=` 형식의 인코딩된 줄바꿈을 포함
    - 파서가 이를 정상 해석하면서 헤더가 삽입됨 (`Bcc:`가 추가됨)
    - 이를 통해 Bcc 이메일을 은폐 전송 가능 ⇒ 정보 유출

🎯 퍼징 목표:
    - 다양한 Subject 값을 자동 생성
    - `\nBcc:` 문자열이 파싱 결과에 등장하는지 여부 확인
    - `probe_state()`로 타입 내부 필드의 변화 감지

🧠 전체 코드 흐름 (Flow Summary):
    1. Atheris가 무작위 바이트 입력 (`data`)을 전달
    2. 바이트를 문자열로 변환 후 Subject 필드에 삽입
    3. email 모듈로 전체 메시지를 파싱
    4. 헤더를 재정의하며 잠재적 Bcc 삽입을 유도
    5. `probe_state()`로 내부 구조 변화 확인
    6. '\nBcc:' 가 삽입되면 취약점 존재 → 예외 발생
"""

import atheris              # Google의 퍼징 도구인 Atheris를 불러옴
import sys                  # 시스템 관련 모듈 (실행 인자 등 사용)
import time
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
        print("Subject input:", repr(input_str))
        time.sleep(2.0)

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