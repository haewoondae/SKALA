/**
 * 포트폴리오를 메뉴 출력 형식의 문자열로 변환합니다.
 * 
 * 핵심 개념:
 * - Strategy 패턴: PortfolioFormatter 인터페이스의 구체적인 구현체
 * - 메뉴 형식: 번호가 매겨진 리스트로 주식 정보를 표시
 * - StringBuilder: 효율적인 문자열 연결을 위해 사용
 */
public class MenuPortfolioFormatter implements PortfolioFormatter {
    
    /**
     * 포트폴리오의 주식 목록을 번호가 매겨진 메뉴 형식으로 변환합니다.
     * 
     * @param portfolio 포맷할 포트폴리오 객체
     * @return "1. 종목: TechCorp, 현재가: 152, 보유수량: 10" 형식의 문자열
     */
    @Override
    public String format(Portfolio portfolio) {
        // StringBuilder: String 연결보다 효율적 (메모리 최적화)
        StringBuilder sb = new StringBuilder();
        
        // 메뉴 번호를 위한 인덱스 (1부터 시작)
        int index = 1;
        
        // 포트폴리오의 모든 주식을 순회하며 메뉴 형식으로 변환
        for (Stock stock : portfolio.getAllStocks()) {
            sb.append(index++)              // 1. 2. 3. ... (후위 증가 연산자)
              .append(". ")                 // 번호 뒤에 점과 공백 추가
              .append(stock.toString())     // Stock의 toString() 메서드 활용
              .append(System.lineSeparator()); // OS별 줄바꿈 문자 (\n 또는 \r\n)
        }
        
        // 완성된 메뉴 형식 문자열 반환
        return sb.toString();
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. Strategy 패턴 구현:
 *    - PortfolioFormatter 인터페이스의 구체적인 구현체
 *    - 다른 포맷터들(DetailedFormatter, SimpleFormatter 등)과 교체 가능
 * 
 * 2. StringBuilder 사용 이유:
 *    - String + String 연산은 매번 새로운 객체 생성 (비효율적)
 *    - StringBuilder는 내부 버퍼를 사용하여 효율적으로 문자열 조합
 * 
 * 3. 후위 증가 연산자 (index++):
 *    - index++ : 현재 값 사용 후 1 증가
 *    - ++index : 1 증가 후 값 사용
 *    - 여기서는 현재 값(1,2,3...)을 먼저 사용하고 증가
 * 
 * 4. System.lineSeparator():
 *    - Windows: \r\n
 *    - Unix/Mac: \n
 *    - 운영체제에 맞는 줄바꿈 문자를 자동으로 선택
 * 
 * 5. 메서드 체이닝:
 *    - sb.append().append().append() 형태로 연속 호출
 *    - 각 append() 메서드가 StringBuilder 객체를 반환하므로 가능
 * 
 * 6. 출력 예시:
 *    1. 종목: TechCorp, 현재가: 152, 보유수량: 10
 *    2. 종목: GreenEnergy, 현재가: 88, 보유수량: 5
 *    3. 종목: HealthPlus, 현재가: 210, 보유수량: 3
 * 
 * 7. 사용 예시:
 *    PortfolioFormatter formatter = new MenuPortfolioFormatter();
 *    String menuText = formatter.format(player.getPortfolio());
 *    System.out.println("=== 보유 주식 선택 ===");
 *    System.out.println(menuText);
 */