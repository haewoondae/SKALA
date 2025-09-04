/**
 * 시장에 상장된 Stock 객체와 파일 저장용 문자열을 상호 변환합니다.
 * 
 * 핵심 개념:
 * - 데이터 영속성: 프로그램 종료 후에도 데이터를 보존하기 위해 파일로 저장
 * - 직렬화/역직렬화: 객체 ↔ 문자열 변환
 * - CSV 형식: "주식명,가격" 형태로 간단하게 저장
 */
public class StockMapper {
    
    // CSV 구분자: 쉼표로 필드 구분
    private static final String DELIMITER = ",";
    
    /**
     * "주식명,가격" 형식의 문자열을 파싱하여 Stock 객체를 생성합니다.
     * 
     * @param line 파싱할 문자열 (예: "삼성전자,70000")
     * @return Stock 객체 (수량은 0으로 설정)
     * @throws IllegalArgumentException 잘못된 형식의 라인인 경우
     */
    public static Stock fromLine(String line) {
        // null이나 빈 문자열 체크
        if (line == null || line.trim().isEmpty()) {
            throw new IllegalArgumentException("라인이 null이거나 비어있습니다: " + line);
        }
        
        // 앞뒤 공백 제거
        line = line.trim();
        
        // 쉼표로 분리
        String[] parts = line.split(DELIMITER);
        
        // 정확히 2개 부분(주식명, 가격)이 있는지 확인
        if (parts.length != 2) {
            throw new IllegalArgumentException("잘못된 형식입니다. '주식명,가격' 형태여야 합니다: " + line);
        }
        
        // 각 부분에서 공백 제거
        String name = parts[0].trim();
        String priceStr = parts[1].trim();
        
        // 주식명이 비어있는지 확인
        if (name.isEmpty()) {
            throw new IllegalArgumentException("주식명이 비어있습니다: " + line);
        }
        
        // 가격을 정수로 변환
        int price;
        try {
            price = Integer.parseInt(priceStr);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("가격이 올바른 숫자가 아닙니다: " + priceStr);
        }
        
        // 가격이 음수인지 확인
        if (price < 0) {
            throw new IllegalArgumentException("가격은 0 이상이어야 합니다: " + price);
        }
        
        // Stock 객체 생성 (수량은 0으로 설정 - 시장 데이터이므로)
        return new Stock(name, price, 0);
    }
    
    /**
     * Stock 객체를 "주식명,가격" 형식의 문자열로 변환합니다.
     * 
     * @param stock 변환할 Stock 객체
     * @return "주식명,가격" 형식의 문자열 (수량은 저장하지 않음)
     * @throws IllegalArgumentException stock이 null인 경우
     */
    public static String toLine(Stock stock) {
        // null 체크
        if (stock == null) {
            throw new IllegalArgumentException("Stock 객체가 null입니다");
        }
        
        // 주식명 null 체크
        if (stock.getName() == null || stock.getName().trim().isEmpty()) {
            throw new IllegalArgumentException("주식명이 null이거나 비어있습니다");
        }
        
        // "주식명,가격" 형식으로 변환
        // 수량은 저장하지 않음 (시장 데이터는 가격 정보만 필요)
        return stock.getName() + DELIMITER + stock.getPrice();
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. 정적 메서드(static) 사용 이유:
 *    - StockMapper는 상태를 가지지 않는 유틸리티 클래스
 *    - 인스턴스 생성 없이 바로 사용 가능
 *    - StockMapper.fromLine(), StockMapper.toLine() 형태로 호출
 * 
 * 2. 데이터 영속성(Persistence):
 *    - 프로그램이 종료되어도 데이터가 사라지지 않도록 파일에 저장
 *    - 프로그램 시작 시 파일에서 데이터를 다시 읽어옴
 * 
 * 3. 예외 처리:
 *    - 잘못된 형식의 데이터에 대해 명확한 오류 메시지 제공
 *    - IllegalArgumentException으로 잘못된 입력 처리
 * 
 * 4. 수량이 0인 이유:
 *    - 시장 데이터는 "어떤 주식이 얼마에 거래되는가" 정보
 *    - 개인의 보유 수량과는 별개 (Portfolio에서 관리)
 * 
 * 5. 사용 예시:
 *    // 문자열 → Stock 객체
 *    Stock stock = StockMapper.fromLine("삼성전자,70000");
 *    System.out.println(stock); // 종목: 삼성전자, 현재가: 70000, 보유수량: 0
 *    
 *    // Stock 객체 → 문자열
 *    String line = StockMapper.toLine(stock);
 *    System.out.println(line); // "삼성전자,70000"
 */