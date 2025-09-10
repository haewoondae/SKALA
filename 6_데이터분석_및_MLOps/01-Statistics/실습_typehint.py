from typing import List, Dict, Optional, Union  # 타입 힌트를 위한 모듈 임포트
import timeit                                  # 성능 측정을 위한 timeit 모듈 임포트
import random                                  # 랜덤 숫자 생성을 위한 random 모듈 임포트

def sum_squares(numbers):                      # 타입 힌트 없는 제곱 합 계산 함수 정의
    sum = 0                                    # 합계 초기화
    for n in numbers:                          # 리스트의 각 요소 반복
        sum += n**2                            # 제곱을 더함
    return sum                                 # 결과 반환

def sum_squares_hint(numbers: List[int]) -> int:  # 타입 힌트 있는 제곱 합 계산 함수 정의
    sum = 0                                    # 합계 초기화
    for n in numbers:                          # 리스트의 각 요소 반복
        sum += n**2                            # 제곱을 더함
    return sum                                 # 결과 반환 (타입 힌트: int)

test_list = [random.randint(1,100) for _ in range(10000)]  # 1~100 사이 랜덤 숫자 10,000개 리스트 생성

time_no_hint = timeit.timeit("sum_squares(test_list)", globals=globals(), number=500000)  # 힌트 없는 함수 실행 시간 측정 (50만 번)

time_hint = timeit.timeit("sum_squares_hint(test_list)", globals=globals(), number=500000)  # 힌트 있는 함수 실행 시간 측정 (50만 번)

print(f"No hint: {time_no_hint}")              # 힌트 없는 경우 시간 출력
print(f"With hint: {time_hint}")               # 힌트 있는 경우 시간 출력
