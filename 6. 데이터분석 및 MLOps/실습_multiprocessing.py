import random                                                     # 랜덤 모듈
import time                                                       # 시간 측정 모듈
import math                                                       # 수학 함수 모듈
from multiprocessing import Pool                                  # 멀티프로세싱 풀
import os                                                         # OS 정보 모듈

# 소수 판별 함수
def is_prime(n):
    if n < 2:                                                     # 2 미만은 소수가 아님
        return False
    for i in range(2, int(math.sqrt(n)) + 1):                     # 제곱근까지만 체크
        if n % i == 0:                                            # 나누어 떨어지면 소수 아님
            return False
    return True                                                   # 소수 반환

# 단일 프로세스 함수
def check_nums_prime(nums):
    prime_cnt = 0                                                 # 소수 개수 초기화
    start_time = time.time()                                      # 시작 시간 기록
    for n in nums:                                                # 숫자 리스트 순회
        if is_prime(n):                                           # 소수 판별
            prime_cnt += 1                                        # 소수 개수 증가
    end_time = time.time()                                        # 종료 시간 기록
    print(f"[순차 처리] 소수의 개수: {prime_cnt}")                     # 결과 출력
    print(f"[순차 처리] 소요 시간: {end_time - start_time:.2f}초").    # 소요 시간 출력
    return prime_cnt                                              # 소수 개수 반환

# 멀티프로세싱 함수
def check_nums_prime_mp(nums):
    start_time = time.time()                                      # 시작 시간 기록
    
    with Pool(processes=os.cpu_count()) as pool:                  # CPU 코어 개수만큼 프로세스 사용
        result = pool.map(is_prime, nums)                         # 병렬로 소수 판별 실행
        
    num_cnt = sum(result)                                         # True 개수 합산 (소수 개수)
    end_time = time.time()                                        # 종료 시간 기록
    
    print(f"[멀티프로세싱] 소수의 개수: {num_cnt}")                     # 결과 출력
    print(f"[멀티프로세싱] 소요 시간: {end_time - start_time:.2f}초")   # 소요 시간 출력
    return num_cnt                                                # 소수 개수 반환

if __name__ == '__main__':
    
    # 난수 생성 
    rand_num = [random.randint(1, 10000000) for _ in range(10000000)]  # 1천만개 난수 생성
   
    # 순차 처리 테스트
    print("단일 프로세스")                                           # 단일 프로세스 제목 출력
    result1 = check_nums_prime(rand_num)                          # 순차 처리 실행
    
    print("="*50)                                                 # 구분선 출력
    
    # 멀티프로세싱 테스트  
    print("멀티 프로세스")                                           # 멀티프로세스 제목 출력
    result2 = check_nums_prime_mp(rand_num)                      # 멀티프로세싱 실행


