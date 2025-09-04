import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * 주식 데이터를 파일에 저장하고 메모리에 로드합니다.
 */
public class StockRepository {
    private static final String STOCK_FILE = "stocks.txt";
    private final List<Stock> stockList = new ArrayList<>();
    private final StockMapper mapper = new StockMapper();

    public void loadStockList() {
        try (BufferedReader reader = new BufferedReader(new FileReader(STOCK_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                Stock stock = mapper.fromLine(line);
                if (stock != null) {
                    stockList.add(stock);
                }
            }
        } catch (IOException e) {
            System.out.println("주식 정보 파일이 없어 기본 데이터를 생성합니다.");
            initializeDefaultStocks();
        }
    }

    private void initializeDefaultStocks() {
        stockList.add(new Stock("TechCorp", 152, 0));
        stockList.add(new Stock("GreenEnergy", 88, 0));
        stockList.add(new Stock("HealthPlus", 210, 0));
        stockList.add(new Stock("BioGen", 75, 0));
    }

    public List<Stock> getAllStocks() {
        return new ArrayList<>(stockList);
    }

    public Stock findStock(int index) {
        if (index >= 0 && index < stockList.size()) {
            return stockList.get(index);
        }
        return null;
    }

    public Stock findStock(String name) {
        return stockList.stream()
                .filter(stock -> stock.getName().equals(name))
                .findFirst()
                .orElse(null);
    }
}