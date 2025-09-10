import logging
from logging.handlers import TimedRotatingFileHandler
import os

#로그 디렉토리 생성
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 로거 생성
logger = logging.getLogger("MyCoolApp")
lo


employees = [
    {"name": "Alice", "department": "Engineering", "age": 30, "salary": 85000},      # 직원 정보
    {"name": "Bob", "department": "Marketing", "age": 25, "salary": 60000},         # 직원 정보
    {"name": "Charlie", "department": "Engineering", "age": 35, "salary": 95000},  # 직원 정보
    {"name": "David", "department": "HR", "age": 45, "salary": 70000},             # 직원 정보
    {"name": "Eve", "department": "Engineering", "age": 28, "salary": 78000},      # 직원 정보
]


# 1) 부서가 "Engineering"이고 salary >= 80000인 직원들의 이름만 리스트로 출력하세요.
employees_condition1 = []                                                        # 조건에 맞는 직원 이름 저장 리스트
for emp in employees:
    if emp["department"] == "Engineering" and emp["salary"] >= 80000:         # 조건 검사
        employees_condition1.append(emp["name"])                               # 이름 추가
print('문제 1번')
print(employees_condition1, '\n')                                                      # 결과 출력

# 2) 30세 이상인 직원의 이름과 부서를 튜플 (name, department) 형태로 리스트로 출력하세요.
employees_condition2 = []                                                        # 조건에 맞는 (이름, 부서) 저장 리스트
for emp in employees:
    if emp["age"] >= 30:                                                        # 조건 검사
        employees_condition2.append((emp['name'], emp['department']))            # 튜플 추가
print('문제 2번')
print(employees_condition2, '\n')                                                      # 결과 출력

# 3) 급여 기준으로 직원 리스트를 salary 내림차순으로 정렬하고, 상위 3명의 이름과 급여를 출력하세요.
employees_sorted = sorted(employees, key=lambda x:x['salary'], reverse=True)      # 급여 내림차순 정렬
print('문제 3번')
for i in range(3):                                                               # 상위 3명 출력
    print(employees_sorted[i]['name'], employees_sorted[i]['salary'])            # 이름과 급여 출력
print()  # 줄바꿈

# 4) 모든 부서별 평균 급여를 출력하는 코드를 작성해보세요
total_dep_salary = {}                                                            # 부서별 총 급여 및 직원 수
for emp in employees:
    dep = emp['department']
    if dep not in total_dep_salary:                                              # 부서가 처음 등장하면 기본값 설정
        total_dep_salary[dep] = {'total_salary': 0, 'count': 0}
    total_dep_salary[dep]['total_salary'] += emp['salary']                       # 부서별 총 급여 합산
    total_dep_salary[dep]['count'] += 1                                          # 부서별 직원 수 카운트
    
print('문제 4번')    
for dep, data in total_dep_salary.items():
    avg_salary = data['total_salary'] / data['count']                            # 부서별 평균 급여 계산
    print(f"부서: {dep}, 평균 급여: {avg_salary}")                              # 결과 출력
