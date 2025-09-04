import java.util.stream.Collectors;

/**
 * 포트폴리오를 파일 저장 형식(CSV)의 문자열로 변환합니다.
 */
public class FilePortfolioFormatter implements PortfolioFormatter {
    @Override
    public String format(Portfolio portfolio) {
        return portfolio.getAllStocks().stream()
                .map(stock -> stock.getName() + "," + stock.getPrice() + "," + stock.getQuantity())
                .collect(Collectors.joining("|"));
    }
}