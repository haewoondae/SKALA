def main():
    print("문장을 입력하세요. 종료하려면 '!quit'을 입력하세요.")
    
    while True:  # 무한 반복
        sentence = input(">> ")  # 사용자 입력 받기
        
        if sentence == "!quit":  # 종료 조건 확인
            print("프로그램을 종료합니다.")
            break  # 반복문 탈출
        
        print(f"입력하신 문장: {sentence}")  # 입력받은 문장 출력

if __name__ == "__main__":
    main()
