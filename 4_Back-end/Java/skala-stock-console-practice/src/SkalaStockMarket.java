import java.util.List; // 이 import 문 추가

/**
 * 프로그램의 시작점이자 전체 흐름을 제어하는 메인 컨트롤러입니다.
 * 
 * 핵심 개념:
 * - 의존성 주입: 생성자에서 모든 컴포넌트 조립
 * - 제어의 역전: 각 계층의 역할을 명확히 분리
 * - 프로그램 생명주기 관리: 시작부터 종료까지 전체 흐름 제어
 */
public class SkalaStockMarket {
    // 의존 객체들: 각 계층의 책임을 명확히 분리
    private final PlayerRepository playerRepository;
    private final StockRepository stockRepository;
    private final StockService stockService;
    private final StockView stockView;
    private Player player; // 현재 플레이어

    /**
     * 생성자에서 모든 의존 객체를 생성하고 조립합니다.
     * 의존성 주입 패턴을 통해 각 컴포넌트 간의 결합도를 낮춥니다.
     */
    public SkalaStockMarket() {
        // Repository 계층: 데이터 접근 담당
        playerRepository = new PlayerRepository();
        stockRepository = new StockRepository();
        
        // Service 계층: 비즈니스 로직 담당 (Repository에 의존)
        stockService = new StockService(stockRepository);
        
        // View 계층: 사용자 인터페이스 담당
        stockView = new StockView();
    }

    /**
     * 프로그램의 전체 생명주기를 관리합니다.
     * 초기화 → 메인 루프 → 종료 처리 순서로 실행됩니다.
     */
    public void start() {
        // 1. 데이터 로드
        stockRepository.loadStockList();     // 주식 시세 데이터 로드
        playerRepository.loadPlayerList();   // 플레이어 데이터 로드

        // 2. 플레이어 초기화 (기존 플레이어 로드 또는 신규 생성)
        initializePlayer();
        stockView.displayPlayerInfo(player); // 초기 플레이어 정보 표시

        // 3. 메인 게임 루프 실행
        mainLoop();

        // 4. 종료 처리
        playerRepository.savePlayerList();   // 플레이어 데이터 저장
        stockView.showMessage("프로그램을 종료합니다...Bye");
        stockView.close(); // Scanner 리소스 해제
    }

    /**
     * 플레이어를 초기화합니다.
     * 기존 플레이어면 로드하고, 새 플레이어면 생성합니다.
     */
    private void initializePlayer() {
        String playerId = stockView.promptForPlayerId();
        player = playerRepository.findPlayer(playerId);
        
        if (player == null) {
            // 새로운 플레이어 생성
            int money = stockView.promptForInitialMoney();
            player = new Player(playerId, money);
            playerRepository.addPlayer(player);
            stockView.showMessage("새로운 플레이어 '" + playerId + "'가 생성되었습니다!");
        } else {
            // 기존 플레이어 로드
            stockView.showMessage("기존 플레이어 '" + playerId + "'로 로그인했습니다!");
        }
    }

    /**
     * 메인 게임 루프입니다.
     * 사용자가 종료를 선택할 때까지 메뉴를 반복 표시합니다.
     */
    private void mainLoop() {
        boolean running = true;
        while (running) {
            int code = stockView.showMenuAndGetSelection();
            switch (code) {
                case 1: // 나의 자산 확인
                    stockView.displayPlayerInfo(player);
                    break;
                case 2: // 주식 구매
                    buyStock();
                    break;
                case 3: // 주식 판매
                    sellStock();
                    break;
                case 0: // 프로그램 종료
                    running = false;
                    break;
                default:
                    stockView.showMessage("올바른 번호를 선택하세요.");
            }
        }
    }

    /**
     * 주식 구매 프로세스를 제어합니다.
     * View → Service → Repository 순서로 호출하여 관심사를 분리합니다.
     */
    private void buyStock() {
        // 1. 현재 주식 시세 표시
        List<Stock> availableStocks = stockRepository.getAllStocks();
        if (availableStocks.isEmpty()) {
            stockView.showMessage("거래 가능한 주식이 없습니다.");
            return;
        }
        
        stockView.displayStockList(availableStocks);
        
        // 2. 사용자 입력 받기
        int stockIndex = stockView.getStockIndexFromUser();
        
        // 3. 선택한 주식이 유효한지 확인
        if (stockIndex < 0 || stockIndex >= availableStocks.size()) {
            stockView.showMessage("잘못된 주식 번호입니다.");
            return;
        }
        
        Stock selectedStock = availableStocks.get(stockIndex);
        int quantity = stockView.getQuantityFromUser();
        
        // 4. 비즈니스 로직 실행 (StockService에 위임)
        String result = stockService.buyStock(player, selectedStock, quantity);
        
        // 5. 결과 표시
        stockView.showMessage(result);
        
        // 6. 거래 후 플레이어 정보 업데이트 표시
        if (result.startsWith("구매 성공")) {
            stockView.showMessage("\n=== 거래 후 자산 현황 ===");
            stockView.displayPlayerInfo(player);
        }
    }

    /**
     * 주식 판매 프로세스를 제어합니다.
     * 보유 주식이 있을 때만 판매가 가능합니다.
     */
    private void sellStock() {
        // 1. 보유 주식 확인
        List<Stock> ownedStocks = player.getPortfolio().getStocksAsList();
        if (ownedStocks.isEmpty()) {
            stockView.showMessage("보유한 주식이 없습니다.");
            return;
        }
        
        // 2. 보유 주식 목록 표시
        stockView.showMessage("\n=== 보유 주식 목록 ===");
        stockView.displayPlayerInfo(player); // 포트폴리오 정보 표시
        
        // 3. 사용자 입력 받기
        int stockIndex = stockView.getStockIndexFromUser();
        
        // 4. 선택한 주식이 유효한지 확인
        if (stockIndex < 0 || stockIndex >= ownedStocks.size()) {
            stockView.showMessage("잘못된 주식 번호입니다.");
            return;
        }
        
        Stock selectedStock = ownedStocks.get(stockIndex);
        stockView.showMessage("선택한 주식: " + selectedStock.getName() + 
                             " (보유수량: " + selectedStock.getQuantity() + "주)");
        
        int quantity = stockView.getQuantityFromUser();
        
        // 5. 비즈니스 로직 실행 (StockService에 위임)
        String result = stockService.sellStock(player, selectedStock, quantity);
        
        // 6. 결과 표시
        stockView.showMessage(result);
        
        // 7. 거래 후 플레이어 정보 업데이트 표시
        if (result.startsWith("판매 성공")) {
            stockView.showMessage("\n=== 거래 후 자산 현황 ===");
            stockView.displayPlayerInfo(player);
        }
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. 의존성 주입 (Dependency Injection):
 *    - 생성자에서 모든 의존 객체를 생성하여 조립
 *    - 각 클래스의 책임을 명확히 분리
 *    - 테스트 용이성과 유지보수성 향상
 * 
 * 2. 계층별 역할 분리:
 *    - Repository: 데이터 접근 및 영속성 관리
 *    - Service: 비즈니스 로직 처리
 *    - View: 사용자 인터페이스 담당
 *    - Controller(이 클래스): 전체 흐름 제어
 * 
 * 3. 프로그램 생명주기 관리:
 *    - 초기화: 데이터 로드, 플레이어 설정
 *    - 실행: 메인 루프에서 사용자 상호작용
 *    - 종료: 데이터 저장, 리소스 해제
 * 
 * 4. 에러 처리:
 *    - 유효성 검사로 잘못된 입력 방지
 *    - 명확한 오류 메시지 제공
 * 
 * 5. 사용자 경험:
 *    - 거래 후 자산 현황 자동 표시
 *    - 단계별 안내 메시지 제공
 */