
### 2024-6923 시도 전략
\n 활용해서 이메일 헤더 파싱 취약점 활용하는 거

1. 기존 취약점 트리거인 \n 문자 이용해서 뭔가 삽입해보자
2. Value 이용한 exploit이니까 겁나 긴 스트링을 넣어서 타입 컨퓨전이나 메모리에 변화 시도해 보자...

Seed 파일들 보면 내 의도가 좀 보일거야 <br>
근데 Atheris mutate 좀 똑똑하지 못한 듯? ㅋㅋ 나보단 나을지도
 
---

### 2023-24329 시도 전략

1. 동일하게 긴 문자열 넣어보자...

---

probe_state는 타입 검증하는 좋은 함수니까 남겨두고 <br>
메모리 배치 같은 거 확인 할 수 있는 함수가 필요하다 <br>
    -> 이게 곧 JIT 컴파일링으로 발생한 다른 점을 알 수 있는거니까.... <br><br>

아마 그럼 frame을 찾아봐야하지 않을까? <br>

🔍 JIT 퍼징에서 살펴볼 주요 요소

항목	설명	이유
1. Frame 내부 필드 변화	stacktop, instr_ptr, f_executable, localsplus[]	JIT 최적화 중 레지스터/스택 배치가 달라져 예상치 못한 실행 흐름 발생 가능
2. PyCodeObject 필드	co_flags, co_varnames, co_code, co_consts, co_qualname 등	JIT 시점에 바이트코드 분석·변형이 이뤄지므로 구조가 바뀌는지 감시
3. PyTypeObject의 vectorcall 관련 필드	tp_vectorcall, tp_vectorcall_offset	JIT이 최적화된 호출 경로를 사용하도록 바꾸는 부분, 해시 추적 가능
4. JIT IR(Intermediate Representation) 캐시나 메모리 구조	JIT 내부 캐시 정보, 예: 코드가 몇 번 실행되어 JIT됐는지	히트 카운터, 트리거 조건이 제대로 작동하는지
5. locals()나 globals() 동작	특정 최적화에 의해 생략되거나 lazy 처리됨	JIT 적용 시점 이후 이 값이 누락되거나 예상과 다를 수 있음
6. trace function과 디버깅 훅	디버거, 트레이서가 예상대로 호출되지 않을 수 있음	JIT된 경로는 일반 프레임과 다르게 동작 가능



⸻

🧪 퍼징으로 포착하고 싶은 이상 현상
	•	🔥 JIT 전과 후의 probe_state() 결과가 다름
	•	🌀 같은 입력인데 결과가 다르게 나옴
	•	❌ Illegal instruction / segfault / memory corruption
	•	🧊 데이터 변형 없이 최적화된 결과가 틀림 (semantic bug)

⸻

✅ 추천 관찰 포인트
	•	f_executable → JIT 최적화 시 다른 코드 오브젝트로 대체되었는가?
	•	PyCodeObject.co_code → JIT 컴파일 전후 바이트코드 변화?
	•	type(obj).__name__ → JIT 이후 객체의 동적 속성 변경 여부
	•	localsplus[] → 스택에 저장되는 값이 다르게 보이는지?

GPT의 의견...

---

<br>

> _typeobject 코드

```c
typedef struct _typeobject {
    PyObject_VAR_HEAD  // Python 객체 헤더 (ref count, 타입 정보 등 포함)

    const char *tp_name;            // ✅ 타입 이름 (ex. "builtins.str"처럼 출력용)
    Py_ssize_t tp_basicsize;        // ✅ 기본 객체 크기 (바이트 단위)
    Py_ssize_t tp_itemsize;         // ✅ 항목 크기 (가변 객체일 경우, 예: 리스트)

    /* 표준 연산을 위한 메서드 포인터들 */

    destructor tp_dealloc;         // ✅ 객체 소멸 시 호출되는 함수
    Py_ssize_t tp_vectorcall_offset; // ✅ vectorcall 슬롯 오프셋 (빠른 함수 호출용)
    getattrfunc tp_getattr;        // ❌ 속성 접근 함수 (Py2 호환용)
    setattrfunc tp_setattr;        // ❌ 속성 설정 함수
    PyAsyncMethods *tp_as_async;   // ✅ 비동기 메서드 집합 (ex. await, async for 등)
    reprfunc tp_repr;              // ❌ 객체 표현 문자열 반환 함수 (repr())

    /* 숫자/시퀀스/매핑과 관련된 메서드 집합 (슬롯 테이블) */

    PyNumberMethods *tp_as_number;   // ✅ 숫자 연산용 함수 포인터들
    PySequenceMethods *tp_as_sequence; // ✅ 시퀀스 관련 함수 포인터들
    PyMappingMethods *tp_as_mapping; // ✅ 딕셔너리 등 매핑 관련 함수 포인터들

    /* 호환성 유지를 위한 추가 연산 슬롯들 */

    hashfunc tp_hash;              // ❌ 해시 함수
    ternaryfunc tp_call;           // ❌ 함수처럼 호출될 때 실행되는 함수 (__call__)
    reprfunc tp_str;               // ❌ str() 호출 시 사용
    getattrofunc tp_getattro;      // ❌ 일반 속성 접근 함수 (__getattr__)
    setattrofunc tp_setattro;      // ❌ 일반 속성 설정 함수 (__setattr__)

    /* 버퍼 프로토콜 관련 */

    PyBufferProcs *tp_as_buffer;   // ✅ 버퍼 인터페이스 지원용 함수들

    /* 기능 플래그 (타입의 확장/옵션 지원 여부) */

    unsigned long tp_flags;        // ✅ 다양한 플래그들 (Py_TPFLAGS_ 시리즈)

    const char *tp_doc;            // ❌ 타입의 설명 문자열 (__doc__)

    /* 순회(traverse) 및 참조 제거 관련 함수들 (GC 관련) */

    traverseproc tp_traverse;      // ✅ 가비지 컬렉션을 위한 순회 함수
    inquiry tp_clear;              // ✅ 내부 참조 해제 함수 (GC 전용)

    /* 리치 비교 연산 지원 (__eq__, __lt__ 등) */

    richcmpfunc tp_richcompare;    // ❌ 6가지 비교 연산자 처리

    /* 약한 참조 지원 여부 */

    Py_ssize_t tp_weaklistoffset;  // ✅ 약한 참조 리스트 위치 (weakref용)

    /* 이터레이터 지원 */

    getiterfunc tp_iter;           // ❌ __iter__ 지원
    iternextfunc tp_iternext;      // ❌ __next__ 지원

    /* 속성/메서드/멤버 디스크립터 등 */

    struct PyMethodDef *tp_methods;  // ❌ 메서드 목록
    struct PyMemberDef *tp_members;  // ❌ 멤버 목록 (C 구조체 필드)
    struct PyGetSetDef *tp_getset;   // ❌ getter/setter 구조체

    struct _typeobject *tp_base;   // ✅ 부모 클래스 타입
    PyObject *tp_dict;             // ✅ 클래스 딕셔너리 (__dict__)
    descrgetfunc tp_descr_get;     // ❌ 디스크립터 getter
    descrsetfunc tp_descr_set;     // ❌ 디스크립터 setter

    Py_ssize_t tp_dictoffset;      // ✅ 인스턴스에서 __dict__ 위치 오프셋
    initproc tp_init;              // ❌ __init__ 함수
    allocfunc tp_alloc;            // ✅ 메모리 할당 함수
    newfunc tp_new;                // ✅ __new__ 생성자
    freefunc tp_free;              // ✅ 메모리 해제 함수
    inquiry tp_is_gc;              // ✅ 가비지 컬렉션 대상인지 여부

    PyObject *tp_bases;            // ✅ 모든 부모 클래스 목록 (튜플)
    PyObject *tp_mro;              // ✅ MRO(Method Resolution Order) 리스트
    PyObject *tp_cache;            // ❌ 내부 캐시용 (주로 내부 구현용)
    PyObject *tp_subclasses;       // ❌ 서브클래스 참조 리스트
    PyObject *tp_weaklist;         // ❌ 약한 참조 리스트 객체
    destructor tp_del;             // ✅ __del__ 소멸자 메서드

    unsigned int tp_version_tag;   // ✅ 타입 속성 캐시 버전 태그 (속도 최적화용)

    destructor tp_finalize;        // ✅ __del__ 대체 소멸자 (__finalize__)

    vectorcallfunc tp_vectorcall;  // ✅ vectorcall 호출 슬롯 (빠른 호출 최적화)

    unsigned char tp_watched;      // ✅ 타입 감시 기능을 사용하는 감시자 비트마스크
} PyTypeObject;
```

<br> <br>

```c
typedef struct _PyInterpreterFrame {
    PyObject *f_executable;         // 이 frame이 실행 중인 코드 객체(code object) 또는 None
                                    // → 함수나 모듈 블록의 코드 정보를 포함 (실행 대상)
                                    // → strong reference (명시적으로 참조 증가)

    struct _PyInterpreterFrame *previous; 
                                    // 직전 프레임을 가리키는 포인터 (이전 호출 스택 프레임)
                                    // → 스택 프레임 체인 구성

    PyObject *f_funcobj;            // 현재 실행 중인 함수 객체
                                    // → C 스택 위가 아닌 경우에만 유효 (Python 함수)

    PyObject *f_globals;            // 글로벌 변수 딕셔너리 (__globals__)
                                    // → C 스택 위가 아닌 경우에만 유효 (borrowed reference)

    PyObject *f_builtins;           // __builtins__ 참조
                                    // → C 스택 위가 아닌 경우에만 유효 (borrowed reference)

    PyObject *f_locals;             // 로컬 변수 딕셔너리 (__locals__)
                                    // → 가비지 컬렉션을 위해 strong reference 유지 (nullable)
                                    // → C 스택 위가 아닌 경우에만 유효

    PyFrameObject *frame_obj;       // PyFrameObject로 감싼 프레임 (디버깅 등에서 사용)
                                    // → NULL일 수 있음 (lazy 생성)

    _Py_CODEUNIT *instr_ptr;        // 현재 실행 중인 바이트코드 명령어의 위치 (IP)
                                    // → CPython 인터프리터가 실제로 가리키는 바이트코드 주소
                                    // → 오프셋 계산 가능 (코드 객체의 co_code 기준)

    int stacktop;                   // TOS (Top Of Stack)의 위치 (localsplus로부터의 오프셋)
                                    // → 현재 스택의 깊이를 의미함
                                    // → localsplus 배열의 어디까지 스택으로 쓰고 있는지를 나타냄

    uint16_t return_offset;         // 호출에서 되돌아갈 바이트코드 오프셋 (CALL 시 유효)
                                    // → JUMPBACK을 위한 값

    char owner;                     // 이 프레임의 소유자 (예: 실행 중인 스레드)
                                    // → 내부 관리용 (enum으로 구분됨)

    // 이 아래는 스택 및 로컬 변수를 포함한 "실제 실행 데이터"입니다
    PyObject *localsplus[1];        // 로컬 변수 + 평가 스택 (일체형 배열)
                                    // → localsplus[0 ~ varcount-1]는 로컬 변수
                                    // → localsplus[varcount ~ stacktop]는 평가 스택
                                    // → 구조체 끝에 가변 길이 배열로 할당됨 (stack grows upward)

} _PyInterpreterFrame;
```