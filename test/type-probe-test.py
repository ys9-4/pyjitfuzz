# type_probe_test.py

import builtins
import time

# probe_state()가 내장되어 있어야 함 (CPython에 커스텀 패치 필요)
assert hasattr(builtins, "probe_state"), "You need a patched CPython with probe_state() support."


def print_probe_state(obj, label, prev_hash=None):
    """probe_state 해시 출력 및 변화 감지 함수"""
    current_hash = probe_state(obj)
    print(f"[{label}] 해시: {current_hash}")
    if prev_hash is not None:
        if current_hash != prev_hash:
            print("⚠️  해시 변경 감지됨!\n")
            time.sleep(999999)
        else:
            # print("✅ 해시 변화 없음\n")
            pass
            
    return current_hash


def test_set_behavior():
    print("===== SET 테스트 시작 =====")
    s = set()
    h = print_probe_state(s, "빈 셋")

    for i in range(1, 100000000):
        s.add(i)
        h = print_probe_state(s, f"{i}개 요소 추가된 셋", h)

    print("===== SET 테스트 종료 =====\n")


def main():
    print("🔍 PyTypeObject 구조 해시 변화 테스트 시작\n")
    test_set_behavior()
    print("✅ 테스트 완료")


if __name__ == "__main__":
    main()