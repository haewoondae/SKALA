/**
 * 주식 거래 관련 비즈니스 로직을 처리합니다.
 * 
 * 핵심 개념:
 * - Service Layer: 비즈니스 로직을 캡슐화
 * - 의존성 주입: Repository를 생성자로 주입받아 사용
 * - 트랜잭션 처리: 거래 성공/실패에 따른 일관된 상태 유지
 */
public class StockService {
    private final StockRepository stockRepository;

    /**
     * StockService 생성자
     * @param stockRepository 주식 데이터 접근을 위한 Repository
     */
    public StockService(StockRepository stockRepository) {
        this.stockRepository = stockRepository;
    }

    /**
     * 주식을 구매합니다.
     * @param player 구매하는 플레이어
     * @param stockToBuy 구매할 주식 정보 (이름, 수량 포함)
     * @param quantity 구매할 수량
     * @return 거래 결과 메시지
     */
    public String buyStock(Player player, Stock stockToBuy, int quantity) {
        // 1. 입력값 유효성 검증
        if (player == null) {
            return "오류: 플레이어 정보가 없습니다.";
        }
        
        if (stockToBuy == null) {
            return "오류: 주식 정보가 없습니다.";
        }
        
        if (quantity <= 0) {
            return "오류: 구매 수량은 1 이상이어야 합니다.";
        }

        // 2. 시장에서 해당 주식이 존재하는지 확인
        Stock marketStock = stockRepository.findStock(stockToBuy.getName());
        if (marketStock == null) {
            return "오류: '" + stockToBuy.getName() + "' 주식을 시장에서 찾을 수 없습니다.";
        }

        // 3. 현재 시장가로 총 구매 비용 계산
        int currentPrice = marketStock.getPrice();
        int totalCost = currentPrice * quantity;

        // 4. 플레이어 자금 확인
        if (player.getMoney() < totalCost) {
            return "구매 실패: 자금이 부족합니다. (필요: " + totalCost + "원, 보유: " + player.getMoney() + "원)";
        }

        // 5. 거래 실행
        try {
            // 플레이어 자금 차감
            player.setMoney(player.getMoney() - totalCost);
            
            // 포트폴리오에 주식 추가/업데이트 (현재 시장가로)
            Stock stockToAdd = new Stock(stockToBuy.getName(), currentPrice, quantity);
            player.getPortfolio().addOrUpdateStock(stockToAdd);
            
            return "구매 성공: " + stockToBuy.getName() + " " + quantity + "주를 " + 
                   currentPrice + "원에 구매했습니다. (총 " + totalCost + "원)";
                   
        } catch (Exception e) {
            // 오류 발생 시 롤백 (자금 복구)
            player.setMoney(player.getMoney() + totalCost);
            return "구매 실패: 거래 처리 중 오류가 발생했습니다. (" + e.getMessage() + ")";
        }
    }

    /**
     * 주식을 판매합니다.
     * @param player 판매하는 플레이어
     * @param stockToSell 판매할 주식 정보
     * @param quantity 판매할 수량
     * @return 거래 결과 메시지
     */
    public String sellStock(Player player, Stock stockToSell, int quantity) {
        // 1. 입력값 유효성 검증
        if (player == null) {
            return "오류: 플레이어 정보가 없습니다.";
        }
        
        if (stockToSell == null) {
            return "오류: 주식 정보가 없습니다.";
        }
        
        if (quantity <= 0) {
            return "오류: 판매 수량은 1 이상이어야 합니다.";
        }

        // 2. 플레이어가 해당 주식을 보유하고 있는지 확인
        java.util.Optional<Stock> ownedStockOpt = player.getPortfolio().findStockByName(stockToSell.getName());
        if (!ownedStockOpt.isPresent()) {
            return "판매 실패: '" + stockToSell.getName() + "' 주식을 보유하고 있지 않습니다.";
        }

        Stock ownedStock = ownedStockOpt.get();

        // 3. 보유 수량 확인
        if (ownedStock.getQuantity() < quantity) {
            return "판매 실패: 보유 수량이 부족합니다. (요청: " + quantity + "주, 보유: " + ownedStock.getQuantity() + "주)";
        }

        // 4. 현재 시장가 확인
        Stock marketStock = stockRepository.findStock(stockToSell.getName());
        if (marketStock == null) {
            return "오류: '" + stockToSell.getName() + "' 주식이 시장에서 거래 중단되었습니다.";
        }

        // 5. 현재 시장가로 총 판매 금액 계산
        int currentPrice = marketStock.getPrice();
        int totalRevenue = currentPrice * quantity;

        // 6. 거래 실행
        try {
            // 플레이어 자금 증가
            player.setMoney(player.getMoney() + totalRevenue);
            
            // 포트폴리오에서 주식 수량 업데이트
            int remainingQuantity = ownedStock.getQuantity() - quantity;
            
            if (remainingQuantity > 0) {
                // 일부 판매: 수량만 업데이트
                Stock updatedStock = new Stock(stockToSell.getName(), currentPrice, remainingQuantity);
                player.getPortfolio().updateStock(updatedStock);
            } else {
                // 전량 판매: 포트폴리오에서 제거 (수량 0으로 업데이트하면 자동 제거)
                Stock emptyStock = new Stock(stockToSell.getName(), currentPrice, 0);
                player.getPortfolio().updateStock(emptyStock);
            }
            
            return "판매 성공: " + stockToSell.getName() + " " + quantity + "주를 " + 
                   currentPrice + "원에 판매했습니다. (총 " + totalRevenue + "원 획득)";
                   
        } catch (Exception e) {
            // 오류 발생 시 롤백 (자금 복구)
            player.setMoney(player.getMoney() - totalRevenue);
            return "판매 실패: 거래 처리 중 오류가 발생했습니다. (" + e.getMessage() + ")";
        }
    }

    /**
     * 플레이어의 특정 주식 보유 수량을 조회합니다.
     * @param player 조회할 플레이어
     * @param stockName 주식 이름
     * @return 보유 수량, 보유하지 않으면 0
     */
    public int getOwnedQuantity(Player player, String stockName) {
        if (player == null || stockName == null) {
            return 0;
        }
        
        java.util.Optional<Stock> ownedStock = player.getPortfolio().findStockByName(stockName);
        return ownedStock.map(Stock::getQuantity).orElse(0);
    }

    /**
     * 특정 주식의 현재 시장가를 조회합니다.
     * @param stockName 주식 이름
     * @return 현재 시장가, 존재하지 않으면 -1
     */
    public int getCurrentPrice(String stockName) {
        if (stockName == null) {
            return -1;
        }
        
        Stock marketStock = stockRepository.findStock(stockName);
        return marketStock != null ? marketStock.getPrice() : -1;
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. 비즈니스 로직 처리:
 *    - 자금 확인 → 거래 실행 → 결과 반환의 단계적 처리
 *    - 예외 상황에 대한 명확한 오류 메시지 제공
 * 
 * 2. 트랜잭션 안전성:
 *    - 거래 실패 시 상태 롤백 (자금 복구)
 *    - try-catch로 예외 상황 처리
 * 
 * 3. 현재 시장가 기준 거래:
 *    - 구매/판매 모두 StockRepository의 현재 시장가 사용
 *    - 과거 구매가격이 아닌 실시간 시장가로 거래
 * 
 * 4. 포트폴리오 관리:
 *    - 구매: addOrUpdateStock() (수량 누적)
 *    - 판매: updateStock() (수량 감소, 0이면 자동 제거)
 * 
 * 5. 사용 예시:
 *    StockService service = new StockService(stockRepository);
 *    String result = service.buyStock(player, stock, 10);
 *    System.out.println(result); // "구매 성공: ..." 또는 "구매 실패: ..."
 */