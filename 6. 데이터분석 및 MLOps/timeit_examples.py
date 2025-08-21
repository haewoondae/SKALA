import timeit
import time
import random
from typing import List

# ============================================================================
# 1. 기본 timeit 사용법
# ============================================================================

def basic_timeit_examples():
    """기본적인 timeit 사용법 예시"""
    print("=== 1. 기본 timeit 사용법 ===")
    
    # 1-1. 간단한 표현식 측정
    result1 = timeit.timeit('sum([1, 2, 3, 4, 5])', number=100000)
    print(f"sum([1,2,3,4,5]) 100,000번 실행 시간: {result1:.6f}초")
    
    # 1-2. 문자열 연결 vs 리스트 join 비교
    string_concat = timeit.timeit('"".join([str(i) for i in range(100)])', number=10000)
    string_format = timeit.timeit('"{}".format("".join([str(i) for i in range(100)]))', number=10000)
    
    print(f"문자열 join: {string_concat:.6f}초")
    print(f"문자열 format: {string_format:.6f}초")

# ============================================================================
# 2. 함수 성능 측정
# ============================================================================

def bubble_sort(arr: List[int]) -> List[int]:
    """버블 정렬 구현"""
    n = len(arr)
    arr = arr.copy()  # 원본 배열 보호
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr: List[int]) -> List[int]:
    """퀵 정렬 구현"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def compare_sorting_algorithms():
    """정렬 알고리즘 성능 비교"""
    print("\n=== 2. 정렬 알고리즘 성능 비교 ===")
    
    # 테스트 데이터 생성
    test_data = [random.randint(1, 1000) for _ in range(100)]
    
    # setup 코드 정의 (각 테스트마다 동일한 데이터 사용)
    setup_code = f"""
import random
from __main__ import bubble_sort, quick_sort
test_data = {test_data}
"""
    
    # 버블 정렬 시간 측정
    bubble_time = timeit.timeit('bubble_sort(test_data)', setup=setup_code, number=100)
    
    # 퀵 정렬 시간 측정
    quick_time = timeit.timeit('quick_sort(test_data)', setup=setup_code, number=100)
    
    # 내장 정렬 시간 측정
    builtin_time = timeit.timeit('sorted(test_data)', setup=setup_code, number=100)
    
    print(f"버블 정렬 (100회): {bubble_time:.6f}초")
    print(f"퀵 정렬 (100회): {quick_time:.6f}초")
    print(f"내장 정렬 (100회): {builtin_time:.6f}초")
    
    # 가장 빠른 것 찾기
    fastest = min(bubble_time, quick_time, builtin_time)
    if fastest == bubble_time:
        print("가장 빠른 정렬: 버블 정렬")
    elif fastest == quick_time:
        print("가장 빠른 정렬: 퀵 정렬")
    else:
        print("가장 빠른 정렬: 내장 정렬")

# ============================================================================
# 3. Timer 객체 사용법
# ============================================================================

def timer_object_examples():
    """Timer 객체를 사용한 고급 측정"""
    print("\n=== 3. Timer 객체 사용법 ===")
    
    # Timer 객체 생성
    t1 = timeit.Timer('sum(range(100))', setup='pass')
    t2 = timeit.Timer('sum([i for i in range(100)])', setup='pass')
    
    # 여러 번 측정하여 최소값 구하기
    result1 = min(t1.repeat(repeat=5, number=10000))
    result2 = min(t2.repeat(repeat=5, number=10000))
    
    print(f"sum(range(100)) 최소 시간: {result1:.6f}초")
    print(f"sum([i for i in range(100)]) 최소 시간: {result2:.6f}초")

# ============================================================================
# 4. 명령행 인터페이스 시뮬레이션
# ============================================================================

def simulate_command_line():
    """명령행 인터페이스 시뮬레이션"""
    print("\n=== 4. 명령행 스타일 측정 ===")
    
    # python -m timeit 명령어와 유사한 결과
    import sys
    from io import StringIO
    
    # 표준 출력을 캡처
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        # timeit.main을 직접 호출 (실제로는 명령행에서 사용)
        # 대신 직접 측정
        result = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
        sys.stdout = old_stdout
        print(f"문자열 조인 테스트: {result:.6f}초")
        
    except:
        sys.stdout = old_stdout
        print("명령행 스타일 테스트 완료")

# ============================================================================
# 5. 실제 활용 예제 - 다양한 방법들의 성능 비교
# ============================================================================

def practical_examples():
    """실제 활용 예제들"""
    print("\n=== 5. 실제 활용 예제 ===")
    
    # 5-1. 리스트 컴프리헨션 vs for 루프
    setup = "data = range(1000)"
    
    list_comp = timeit.timeit('[x*2 for x in data]', setup=setup, number=1000)
    for_loop = timeit.timeit('''
result = []
for x in data:
    result.append(x*2)
''', setup=setup, number=1000)
    
    print(f"리스트 컴프리헨션: {list_comp:.6f}초")
    print(f"for 루프: {for_loop:.6f}초")
    
    # 5-2. 딕셔너리 접근 방법 비교
    setup_dict = "d = {'key': 'value'}"
    
    get_method = timeit.timeit("d.get('key', 'default')", setup=setup_dict, number=100000)
    try_except = timeit.timeit('''
try:
    result = d['key']
except KeyError:
    result = 'default'
''', setup=setup_dict, number=100000)
    
    print(f"dict.get() 방법: {get_method:.6f}초")
    print(f"try-except 방법: {try_except:.6f}초")

# ============================================================================
# 6. 데코레이터를 사용한 함수 실행 시간 측정
# ============================================================================

def timing_decorator(func):
    """함수 실행 시간을 측정하는 데코레이터"""
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        print(f"{func.__name__} 실행 시간: {end_time - start_time:.6f}초")
        return result
    return wrapper

@timing_decorator
def slow_function():
    """느린 함수 예제"""
    time.sleep(0.1)  # 0.1초 대기
    return sum(range(10000))

def decorator_example():
    """데코레이터 예제"""
    print("\n=== 6. 데코레이터를 사용한 시간 측정 ===")
    result = slow_function()
    print(f"함수 결과: {result}")

# ============================================================================
# 7. 메인 실행 함수
# ============================================================================

def main():
    """모든 예제 실행"""
    print("TIMEIT 활용법 종합 예제")
    print("=" * 50)
    
    basic_timeit_examples()
    compare_sorting_algorithms()
    timer_object_examples()
    simulate_command_line()
    practical_examples()
    decorator_example()
    
    print("\n" + "=" * 50)
    print("모든 테스트 완료!")

if __name__ == "__main__":
    main()
