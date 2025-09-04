/**
 * 플레이어의 기본 정보(ID, 자금)와 포트폴리오를 관리합니다.
 * 
 * 핵심 개념:
 * - 플레이어는 고유 ID, 보유 자금, 주식 포트폴리오를 가짐
 * - portfolio는 final로 선언하여 객체 교체 방지 (불변성 보장)
 * - 포트폴리오는 생성자에서 한 번만 초기화되고 이후 교체 불가
 */
public class Player {
    private String id;
    private int money;
    private final Portfolio portfolio; // final: 한 번 초기화되면 다른 Portfolio 객체로 교체 불가

    /**
     * 플레이어 객체를 생성합니다.
     * @param id 플레이어 고유 식별자
     * @param initialMoney 초기 보유 자금
     */
    public Player(String id, int initialMoney) {
        this.id = id;
        this.money = initialMoney;
        this.portfolio = new Portfolio(); // 새로운 빈 포트폴리오 생성
    }

    // Getters: 객체의 상태를 안전하게 읽기
    
    /**
     * 플레이어 ID를 반환합니다.
     * @return 플레이어 ID
     */
    public String getId() {
        return id;
    }
    
    /**
     * 플레이어의 현재 보유 자금을 반환합니다.
     * @return 보유 자금
     */
    public int getMoney() {
        return money;
    }
    
    /**
     * 플레이어의 포트폴리오를 반환합니다.
     * @return 포트폴리오 객체 (final이므로 교체 불가, 내용 수정은 가능)
     */
    public Portfolio getPortfolio() {
        return portfolio;
    }

    // Setters: 객체의 상태를 안전하게 변경
    
    /**
     * 플레이어 ID를 변경합니다.
     * @param id 새로운 플레이어 ID
     */
    public void setId(String id) {
        this.id = id;
    }
    
    /**
     * 플레이어의 보유 자금을 변경합니다.
     * @param money 새로운 보유 자금
     */
    public void setMoney(int money) {
        this.money = money;
    }
    
    // 참고: portfolio는 final이므로 setter 없음
    // portfolio 객체 자체는 교체할 수 없지만, 
    // portfolio.addOrUpdateStock() 등으로 내용은 수정 가능
    
    /**
     * 플레이어 정보를 문자열로 반환합니다.
     * @return 플레이어 정보 (ID, 보유 자금, 포트폴리오 주식 수)
     */
    @Override
    public String toString() {
        return "플레이어 ID: " + id + ", 보유 자금: " + money + "원, " +
               "보유 주식 종목 수: " + portfolio.getAllStocks().size() + "개";
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. final 키워드의 의미:
 *    - portfolio는 final → 다른 Portfolio 객체로 교체 불가
 *    - 하지만 portfolio 내부 상태는 변경 가능 (portfolio.addOrUpdateStock() 등)
 *    - 예: portfolio = new Portfolio(); ❌ (컴파일 오류)
 *         portfolio.addOrUpdateStock(stock); ✅ (내용 변경 가능)
 * 
 * 2. 왜 portfolio에 setter가 없나?:
 *    - final로 선언했으므로 교체 불가능
 *    - 플레이어는 생성 시점부터 죽을 때까지 같은 포트폴리오 사용
 *    - 포트폴리오 내용은 portfolio.addOrUpdateStock() 등으로 변경
 * 
 * 3. 사용 예시:
 *    Player player = new Player("김철수", 1000000);
 *    player.getPortfolio().addOrUpdateStock(new Stock("삼성전자", 70000, 10));
 *    System.out.println(player); // 플레이어 정보 출력
 */