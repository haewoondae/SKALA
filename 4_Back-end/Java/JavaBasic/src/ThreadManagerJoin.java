public class ThreadManagerJoin {
    public static void main(String[] args) {
        // 새로운 Thread 생성
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
        
        try {
            // join() 호출 - 메인 스레드가 newThread의 완료를 대기
            newThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // 스레드 완료 후 메인 함수 종료 메시지 출력
        System.out.println("메인 함수를 종료합니다");
        
        // 프로그램 종료
        System.exit(0);
    }
}