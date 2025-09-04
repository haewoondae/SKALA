/**
 * 포트폴리오를 메뉴 출력 형식의 문자열로 변환합니다.
 */
public class MenuPortfolioFormatter implements PortfolioFormatter {
    @Override
    public String format(Portfolio portfolio) {
        StringBuilder sb = new StringBuilder();
        int index = 1;
        for (Stock stock : portfolio.getAllStocks()) {
            sb.append(index++)
                    .append(". ")
                    .append(stock.toString())
                    .append(System.lineSeparator());
        }
        return sb.toString();
    }
}