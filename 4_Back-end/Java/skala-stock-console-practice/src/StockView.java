import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Scanner;

/**
 * 콘솔 입출력과 관련된 모든 것을 처리합니다.
 * 
 * 핵심 개념:
 * - View Layer: MVC 패턴의 View 계층 담당
 * - Single Responsibility: 오직 사용자 인터페이스만 담당
 * - Scanner 관리: 입력 버퍼 관리 및 한글 지원
 */
public class StockView {
    // UTF-8 인코딩을 지원하는 Scanner (한글 입력 처리)
    private final Scanner scanner;

    /**
     * StockView 생성자
     * UTF-8 인코딩으로 Scanner를 초기화하여 한글 입력을 지원합니다.
     */
    public StockView() {
        // StandardCharsets.UTF_8: 한글 등 유니코드 문자 입력 지원
        this.scanner = new Scanner(System.in, StandardCharsets.UTF_8);
    }

    /**
     * 사용자로부터 플레이어 ID 입력을 받습니다.
     * @return 입력받은 플레이어 ID
     */
    public String promptForPlayerId() {
        System.out.print("\n플레이어 ID를 입력하세요: ");
        return scanner.nextLine(); // 문자열 전체를 읽음 (공백 포함)
    }

    /**
     * 사용자로부터 초기 투자금 입력을 받습니다.
     * @return 입력받은 초기 투자금
     */
    public int promptForInitialMoney() {
        System.out.print("초기 투자금을 입력하세요: ");
        int money = scanner.nextInt(); // 정수값 읽기
        scanner.nextLine(); // 입력 버퍼에 남은 개행문자 제거 (중요!)
        return money;
    }

    /**
     * 메인 메뉴를 출력하고 사용자 선택을 받습니다.
     * @return 선택된 메뉴 번호 (0-3)
     */
    public int showMenuAndGetSelection() {
        // 시각적으로 구분되는 메뉴 출력
        System.out.println("\n======= 스칼라 주식 시장 =======");
        System.out.println("  1. 나의 자산 확인");
        System.out.println("  2. 주식 구매");
        System.out.println("  3. 주식 판매");
        System.out.println("  0. 프로그램 종료");
        System.out.println("=============================");
        System.out.print("선택: ");
        
        int selection = scanner.nextInt(); // 메뉴 선택 번호 읽기
        scanner.nextLine(); // 버퍼 정리 (nextInt() 후 항상 필요)
        return selection;
    }

    /**
     * 플레이어의 상세 정보를 출력합니다.
     * MenuPortfolioFormatter를 사용하여 포트폴리오를 번호가 매겨진 형식으로 표시합니다.
     * @param player 출력할 플레이어 객체
     */
    public void displayPlayerInfo(Player player) {
        System.out.println("\n======= 플레이어 정보 =======");
        System.out.println("  ID: " + player.getId());
        
        // String.format("%,d", ...)는 숫자에 천단위 구분자(,) 추가
        // 예: 1000000 → 1,000,000
        System.out.println("  보유 현금: " + String.format("%,d", player.getMoney()) + "원");
        System.out.println("-----------------------------");
        System.out.println("  보유 주식 목록:");
        
        // Strategy 패턴: MenuPortfolioFormatter를 사용하여 포트폴리오 포맷팅
        PortfolioFormatter formatter = new MenuPortfolioFormatter();
        String formattedStocks = formatter.format(player.getPortfolio());
        
        // 보유 주식이 없는 경우 적절한 메시지 표시
        if (formattedStocks.isEmpty()) {
            System.out.println("    (보유 주식이 없습니다)");
        } else {
            System.out.print(formattedStocks); // 이미 줄바꿈이 포함됨
        }
        System.out.println("=============================");
    }

    /**
     * 현재 주식 시세 목록을 출력합니다.
     * @param stockList 출력할 주식 목록
     */
    public void displayStockList(List<Stock> stockList) {
        System.out.println("\n======= 현재 주식 시세 =======");
        
        // 인덱스를 사용한 반복문으로 번호 매기기 (1부터 시작)
        for (int i = 0; i < stockList.size(); i++) {
            Stock stock = stockList.get(i);
            // (i + 1): 0-based 인덱스를 1-based 번호로 변환
            // String.format("%,d", ...): 가격에 천단위 구분자 추가
            System.out.println(
                    "  " + (i + 1) + ". " + stock.getName() + " - " + 
                    String.format("%,d", stock.getPrice()) + "원");
        }
        System.out.println("=============================");
    }

    /**
     * 사용자로부터 주식 번호 선택을 받습니다.
     * @return 선택된 주식의 배열 인덱스 (0-based)
     */
    public int getStockIndexFromUser() {
        System.out.print("주식 번호를 선택하세요: ");
        int index = scanner.nextInt() - 1; // 1-based 입력을 0-based 인덱스로 변환
        scanner.nextLine(); // 버퍼 정리
        return index;
    }

    /**
     * 사용자로부터 거래할 주식 수량을 입력받습니다.
     * @return 입력받은 수량
     */
    public int getQuantityFromUser() {
        System.out.print("수량을 입력하세요: ");
        int quantity = scanner.nextInt(); // 정수 수량 읽기
        scanner.nextLine(); // 버퍼 정리 (nextInt() 후 필수)
        return quantity;
    }

    /**
     * 일반 메시지를 화면에 출력합니다.
     * @param message 출력할 메시지
     */
    public void showMessage(String message) {
        System.out.println(message);
    }

    /**
     * Scanner 리소스를 해제합니다.
     * 프로그램 종료 시 반드시 호출해야 합니다.
     */
    public void close() {
        scanner.close(); // 메모리 누수 방지를 위한 리소스 해제
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. MVC 패턴의 View 계층:
 *    - Model(데이터)이나 Controller(비즈니스 로직)과 분리
 *    - 오직 사용자 인터페이스(입출력)만 담당
 * 
 * 2. Scanner 버퍼 관리:
 *    - nextInt() 후 nextLine() 호출 이유:
 *      nextInt()는 숫자만 읽고 개행문자(\n)를 버퍼에 남김
 *      다음 nextLine() 호출 시 빈 문자열을 읽는 문제 발생
 *      scanner.nextLine()으로 버퍼의 개행문자 제거 필요
 * 
 * 3. UTF-8 인코딩:
 *    - StandardCharsets.UTF_8로 한글 입력 지원
 *    - 기본 Scanner는 시스템 기본 인코딩 사용 (한글 깨짐 가능)
 * 
 * 4. 숫자 포맷팅:
 *    - String.format("%,d", number): 천단위 구분자 추가
 *    - 1000000 → "1,000,000" (가독성 향상)
 * 
 * 5. 인덱스 변환:
 *    - 사용자는 1, 2, 3... 으로 인식
 *    - 배열/리스트는 0, 1, 2... 인덱스 사용
 *    - input - 1 또는 index + 1로 변환
 * 
 * 6. 리소스 관리:
 *    - Scanner는 시스템 리소스 사용
 *    - close() 메서드로 반드시 해제 필요
 * 
 * 7. 사용 예시:
 *    StockView view = new StockView();
 *    String id = view.promptForPlayerId();
 *    int choice = view.showMenuAndGetSelection();
 *    view.displayPlayerInfo(player);
 *    view.close(); // 프로그램 종료 시
 */