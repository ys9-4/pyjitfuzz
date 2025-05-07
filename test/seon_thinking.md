
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
