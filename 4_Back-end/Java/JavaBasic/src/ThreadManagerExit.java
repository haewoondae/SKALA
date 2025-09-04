public class ThreadManagerExit {
    public static void main(String[] args) {
        // 새로운 Thread 생성 및 실행
        Thread newThread = new Thread(() -> {
            try {
                // 1초간 sleep
                Thread.sleep(1000);
                System.out.println("새로운 스레드 작업을 시작합니다.");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        
        // 스레드 시작
        newThread.start();
        
        // 메인 함수 종료 메시지 출력
        System.out.println("메인 함수를 종료합니다");
        
        // 프로그램 강제 종료
        System.exit(0);
    }
}