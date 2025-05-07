import ctypes
import builtins

# C 스타일 구조체 정의: struct Point { int x; int y; };
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]

def print_type_hash(obj, label):
    if hasattr(builtins, "probe_state"):
        hash_value = probe_state(obj)
        print(f"[{label}] probe_state() = {hash_value}")
        return hash_value
    else:
        print(f"[{label}] probe_state not available")
        return None

def main():
    # Point 구조체 인스턴스 생성
    p1 = Point(10, 20)
    print(f"p1 = ({p1.x}, {p1.y})")

    # probe_state 해시 확인
    h1 = print_type_hash(p1, "Initial")

    # 두 번째 구조체 인스턴스
    p2 = Point(30, 40)
    print(f"p2 = ({p2.x}, {p2.y})")
    h2 = print_type_hash(p2, "Second")

    # 동일 타입이므로 해시는 같을 것
    if h1 == h2:
        print("✅ 해시값이 동일합니다. (같은 구조체 타입)")
    else:
        print("❗ 해시값이 다릅니다. (타입 변화 가능성)")

    # 클래스 자체에 접근해서 type 해시 확인
    print_type_hash(type(p1), "Type of Point")

if __name__ == "__main__":
    main()