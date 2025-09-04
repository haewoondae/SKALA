/**
 * Player 객체와 파일 데이터(문자열)를 상호 변환합니다.
 * 
 * 파일 형식: "id,money,stockName1:price1:qty1|stockName2:price2:qty2"
 * 예시: "김철수,1000000,삼성전자:70000:10|LG전자:80000:5"
 * 
 * 핵심 개념:
 * - 직렬화/역직렬화: 객체 ↔ 문자열 변환
 * - 복합 데이터 파싱: 플레이어 기본 정보 + 포트폴리오 정보
 * - 구분자 활용: 쉼표(,), 콜론(:), 파이프(|)로 계층적 구분
 */
public class PlayerMapper {
    // 구분자 상수 정의
    private static final String FIELD_DELIMITER = ",";      // 필드 구분 (id, money, stocks)
    private static final String STOCK_DELIMITER = "|";      // 주식 간 구분
    private static final String STOCK_INFO_DELIMITER = ":"; // 주식 정보 구분 (name:price:qty)

    /**
     * "id,money,stockName1:price1:qty1|stockName2:price2:qty2" 형식의 문자열을 파싱하여
     * Player 객체(포트폴리오 포함)를 생성합니다.
     * 
     * @param line 파싱할 문자열
     * @return 완전히 복원된 Player 객체
     * @throws IllegalArgumentException 잘못된 형식의 라인인 경우
     */
    public static Player fromLine(String line) {
        // null이나 빈 문자열 체크
        if (line == null || line.trim().isEmpty()) {
            throw new IllegalArgumentException("플레이어 데이터가 비어있습니다");
        }

        try {
            // 1. 기본 필드 분리: [id, money, stocksData]
            String[] mainParts = line.split(FIELD_DELIMITER, 3); // 최대 3개로 분할
            
            // 기본 필드 유효성 검사 (최소 id, money는 있어야 함)
            if (mainParts.length < 2) {
                throw new IllegalArgumentException("플레이어 데이터 형식이 올바르지 않습니다: " + line);
            }

            // 2. 기본 정보 파싱
            String id = mainParts[0].trim();
            if (id.isEmpty()) {
                throw new IllegalArgumentException("플레이어 ID가 비어있습니다");
            }

            int money;
            try {
                money = Integer.parseInt(mainParts[1].trim());
            } catch (NumberFormatException e) {
                throw new IllegalArgumentException("보유 금액이 올바른 숫자가 아닙니다: " + mainParts[1]);
            }

            // 3. Player 객체 생성 (빈 포트폴리오로 시작)
            Player player = new Player(id, money);

            // 4. 포트폴리오 데이터가 있으면 파싱하여 추가
            if (mainParts.length > 2 && !mainParts[2].trim().isEmpty()) {
                String stocksData = mainParts[2].trim();
                parseAndAddStocks(player, stocksData);
            }

            return player;

        } catch (Exception e) {
            throw new IllegalArgumentException("플레이어 데이터 파싱 중 오류 발생: " + e.getMessage(), e);
        }
    }

    /**
     * 주식 데이터 문자열을 파싱하여 플레이어의 포트폴리오에 추가합니다.
     * 
     * @param player 주식을 추가할 플레이어
     * @param stocksData "stockName1:price1:qty1|stockName2:price2:qty2" 형식의 문자열
     */
    private static void parseAndAddStocks(Player player, String stocksData) {
        // 주식들을 파이프(|)로 분리
        String[] stockEntries = stocksData.split("\\" + STOCK_DELIMITER); // 정규식 이스케이프
        
        for (String stockEntry : stockEntries) {
            if (stockEntry.trim().isEmpty()) {
                continue; // 빈 엔트리는 건너뛰기
            }

            // 각 주식 정보를 콜론(:)으로 분리: [name, price, quantity]
            String[] stockInfo = stockEntry.trim().split(STOCK_INFO_DELIMITER);
            
            if (stockInfo.length != 3) {
                throw new IllegalArgumentException("주식 정보 형식이 올바르지 않습니다: " + stockEntry);
            }

            try {
                String stockName = stockInfo[0].trim();
                int price = Integer.parseInt(stockInfo[1].trim());
                int quantity = Integer.parseInt(stockInfo[2].trim());

                // 유효성 검사
                if (stockName.isEmpty()) {
                    throw new IllegalArgumentException("주식명이 비어있습니다: " + stockEntry);
                }
                if (price < 0) {
                    throw new IllegalArgumentException("주식 가격은 0 이상이어야 합니다: " + price);
                }
                if (quantity <= 0) {
                    throw new IllegalArgumentException("주식 수량은 1 이상이어야 합니다: " + quantity);
                }

                // 포트폴리오에 주식 추가
                Stock stock = new Stock(stockName, price, quantity);
                player.getPortfolio().addOrUpdateStock(stock);

            } catch (NumberFormatException e) {
                throw new IllegalArgumentException("주식 가격 또는 수량이 올바른 숫자가 아닙니다: " + stockEntry);
            }
        }
    }

    /**
     * Player 객체를 "id,money,stockName1:price1:qty1|stockName2:price2:qty2" 형식의 
     * 문자열로 변환합니다.
     * 
     * @param player 변환할 Player 객체
     * @return 파일 저장용 문자열
     * @throws IllegalArgumentException player가 null인 경우
     */
    public static String toLine(Player player) {
        if (player == null) {
            throw new IllegalArgumentException("Player 객체가 null입니다");
        }

        StringBuilder sb = new StringBuilder();
        
        // 1. 기본 정보 추가: "id,money"
        sb.append(player.getId())
          .append(FIELD_DELIMITER)
          .append(player.getMoney());
        
        // 2. 포트폴리오 정보 추가
        java.util.Collection<Stock> stocks = player.getPortfolio().getAllStocks();
        
        if (!stocks.isEmpty()) {
            sb.append(FIELD_DELIMITER); // 주식 데이터 시작 구분자
            
            boolean isFirst = true;
            for (Stock stock : stocks) {
                if (!isFirst) {
                    sb.append(STOCK_DELIMITER); // 주식 간 구분자 (|)
                }
                
                // "stockName:price:quantity" 형식으로 추가
                sb.append(stock.getName())
                  .append(STOCK_INFO_DELIMITER)
                  .append(stock.getPrice())
                  .append(STOCK_INFO_DELIMITER)
                  .append(stock.getQuantity());
                
                isFirst = false;
            }
        }
        
        return sb.toString();
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. 복합 데이터 직렬화:
 *    - Player 기본 정보 + Portfolio 정보를 하나의 문자열로 저장
 *    - 계층적 구분자 사용: , | :
 * 
 * 2. 파싱 전략:
 *    - split() 메서드의 limit 매개변수 활용
 *    - 예외 상황별 명확한 오류 메시지 제공
 * 
 * 3. 데이터 무결성:
 *    - null 체크, 빈 문자열 체크
 *    - 숫자 범위 검증 (음수 방지)
 * 
 * 4. 성능 최적화:
 *    - StringBuilder 사용으로 문자열 연결 최적화
 *    - 정규식 이스케이프 (\|) 사용
 * 
 * 5. 파일 형식 예시:
 *    - 주식 없음: "김철수,1000000"
 *    - 주식 있음: "김철수,800000,삼성전자:70000:10|LG전자:80000:5"
 * 
 * 6. 사용 예시:
 *    // 객체 → 문자열
 *    String line = PlayerMapper.toLine(player);
 *    
 *    // 문자열 → 객체
 *    Player restored = PlayerMapper.fromLine(line);
 */