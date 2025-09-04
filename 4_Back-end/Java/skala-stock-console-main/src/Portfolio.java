import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * 플레이어의 주식 포트폴리오를 관리합니다.
 */
public class Portfolio {
    private final Map<String, Stock> stocks = new LinkedHashMap<>();

    public void addOrUpdateStock(Stock stockToAdd) {
        stocks.compute(stockToAdd.getName(), (name, existingStock) -> {
            if (existingStock != null) {
                existingStock.setPrice(stockToAdd.getPrice());
                existingStock.setQuantity(existingStock.getQuantity() + stockToAdd.getQuantity());
                return existingStock;
            } else {
                return stockToAdd;
            }
        });
    }

    public void updateStock(Stock stockToUpdate) {
        Stock existingStock = stocks.get(stockToUpdate.getName());
        if (existingStock != null) {
            existingStock.setPrice(stockToUpdate.getPrice());
            existingStock.setQuantity(stockToUpdate.getQuantity());
            if (existingStock.getQuantity() <= 0) {
                stocks.remove(existingStock.getName());
            }
        }
    }

    public Optional<Stock> findStockByName(String name) {
        return Optional.ofNullable(stocks.get(name));
    }

    public Collection<Stock> getAllStocks() {
        return Collections.unmodifiableCollection(stocks.values());
    }

    public List<Stock> getStocksAsList() {
        return new ArrayList<>(stocks.values());
    }
}