import os                                                      # OS 모듈
import logging                                                 # 로깅 모듈
from logging.handlers import TimedRotatingFileHandler          # 핸들러 모듈
from dotenv import load_dotenv                                 # .env 로드 모듈

def setup_logging():
    """로깅 시스템 설정 함수 - 경로 지정 버전"""
        
    # .env 파일 로드
    load_dotenv()                                              # .env 파일 로드
    
    # 환경변수 가져오기 (기본값도 함께 설정)
    log_level_str = os.getenv("LOG_LEVEL")                    # 로그 레벨 환경변수
    app_name = os.getenv("APP_NAME")                          # 앱 이름 환경변수
    
    # 로드 확인을 위한 출력
    print(f"로드된 LOG_LEVEL: {log_level_str}")                # 로그 레벨 출력
    print(f"로드된 APP_NAME: {app_name}")                      # 앱 이름 출력
    
    # 로그 레벨 변환
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)  # 문자열을 상수로 변환
    
    # 로그 포맷 설정
    log_format = "%(asctime)s | %(levelname)s | %(message)s"   # 로그 포맷 문자열
    formatter = logging.Formatter(log_format)                   # 포맷터 객체 생성
    
    # 로거 생성
    logger = logging.getLogger(app_name)                        # 앱 이름으로 로거 생성
    logger.setLevel(log_level)                                  # 로거 레벨 설정
    logger.handlers.clear()                                     # 기존 핸들러 제거
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()                   # 콘솔 핸들러 생성
    console_handler.setLevel(log_level)                         # 콘솔 핸들러 레벨 설정
    console_handler.setFormatter(formatter)                     # 콘솔 핸들러 포맷 설정
    logger.addHandler(console_handler)                          # 로거에 콘솔 핸들러 추가
    
    # 파일 핸들러
    file_handler = logging.FileHandler("app.log", encoding="utf-8") # 파일 핸들러 생성
    file_handler.setLevel(log_level)                            # 파일 핸들러 레벨 설정
    file_handler.setFormatter(formatter)                        # 파일 핸들러 포맷 설정
    logger.addHandler(file_handler)                             # 로거에 파일 핸들러 추가
    
    return logger                                              # 로거 반환

def main():
    """메인 함수 - 로그 출력만"""
    
    # 로깅 설정
    logger = setup_logging()                                    # 로깅 시스템 설정
    
    # INFO 레벨 메시지: "앱 실행 시작"
    logger.info("앱 실행 시작")                                 # 앱 시작 로그
    
    # DEBUG 레벨 메시지: "환경 변수 로딩 완료"
    logger.debug("환경 변수 로딩 완료")                         # 환경 변수 로딩 로그
    
    # ERROR 레벨 메시지: ZeroDivisionError 예외 발생 시 출력
    try:
        result = 10 / 0                                        # 0으로 나누기
    except ZeroDivisionError as e:
        logger.error(f"ZeroDivisionError 예외 발생: {e}")      # 예외 로그

if __name__ == "__main__":
    main()                                                     # main 함수 실행
