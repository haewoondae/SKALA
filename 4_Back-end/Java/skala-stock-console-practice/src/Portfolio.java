import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * 플레이어의 주식 포트폴리오를 관리합니다.
 * 
 * 핵심 개념:
 * - Map<String, Stock>: 주식 이름을 키로 사용하여 빠른 검색 가능
 * - LinkedHashMap: 입력 순서를 유지하는 Map (일반 HashMap과 달리 순서 보장)
 * - Optional: null 대신 사용하는 안전한 값 처리 방식
 */
public class Portfolio {
    // LinkedHashMap: 주식 추가 순서를 유지하면서 빠른 검색 제공
    private final Map<String, Stock> stocks = new LinkedHashMap<>();

    /**
     * 포트폴리오에 주식을 추가하거나 기존 주식의 수량을 증가시킵니다.
     * @param stockToAdd 추가할 주식 객체
     */
    public void addOrUpdateStock(Stock stockToAdd) {
        String stockName = stockToAdd.getName();
        
        // 이미 해당 주식이 포트폴리오에 있는지 확인
        if (stocks.containsKey(stockName)) {
            // 기존 주식이 있으면 수량을 더하고 가격을 업데이트
            Stock existingStock = stocks.get(stockName);
            int newQuantity = existingStock.getQuantity() + stockToAdd.getQuantity();
            
            // 기존 주식의 수량과 가격 업데이트
            existingStock.setQuantity(newQuantity);
            existingStock.setPrice(stockToAdd.getPrice()); // 최신 가격으로 업데이트
        } else {
            // 새로운 주식이면 포트폴리오에 추가
            stocks.put(stockName, stockToAdd);
        }
    }

    /**
     * 기존 주식의 정보를 갱신합니다. 수량이 0 이하가 되면 포트폴리오에서 제거합니다.
     * @param stockToUpdate 갱신할 주식 객체
     */
    public void updateStock(Stock stockToUpdate) {
        String stockName = stockToUpdate.getName();
        
        // 해당 주식이 포트폴리오에 있는지 확인
        if (stocks.containsKey(stockName)) {
            // 수량이 0 이하이면 포트폴리오에서 제거
            if (stockToUpdate.getQuantity() <= 0) {
                stocks.remove(stockName);
            } else {
                // 수량이 0보다 크면 기존 주식 정보를 새로운 정보로 교체
                stocks.put(stockName, stockToUpdate);
            }
        }
        // 포트폴리오에 없는 주식이면 아무것도 하지 않음 (갱신 전용 메서드)
    }

    /**
     * 주식 이름으로 특정 주식을 찾습니다.
     * @param name 찾을 주식의 이름
     * @return Optional<Stock> - 주식이 있으면 해당 주식, 없으면 Optional.empty()
     */
    public Optional<Stock> findStockByName(String name) {
        // Map에서 주식을 찾아서 Optional로 감싸서 반환
        // null 체크를 Optional이 자동으로 처리해줌
        Stock foundStock = stocks.get(name);
        return Optional.ofNullable(foundStock); // null이면 Optional.empty(), 아니면 Optional.of(foundStock)
    }

    /**
     * 포트폴리오에 있는 모든 주식 목록을 반환합니다.
     * @return Collection<Stock> 모든 주식들의 컬렉션
     */
    public Collection<Stock> getAllStocks() {
        // Map의 values() 메서드로 모든 Stock 객체들을 Collection으로 반환
        return stocks.values();
    }

    /**
     * 메뉴에서 번호로 선택할 수 있도록 주식들을 List 형태로 반환합니다.
     * @return List<Stock> 순서가 있는 주식 리스트 (인덱스 접근 가능)
     */
    public List<Stock> getStocksAsList() {
        // Collection을 List로 변환 (인덱스로 접근 가능하게 함)
        // LinkedHashMap이므로 추가된 순서대로 List에 담김
        return new ArrayList<>(stocks.values());
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. Map<String, Stock> 사용 이유:
 *    - 주식 이름으로 O(1) 시간에 빠른 검색 가능
 *    - LinkedHashMap으로 순서도 보장
 * 
 * 2. Optional 사용:
 *    - null 대신 사용하여 안전한 값 처리
 *    - findStockByName()에서 주식이 없을 때 null 대신 Optional.empty() 반환
 * 
 * 3. Collection vs List:
 *    - getAllStocks(): Collection 반환 (순회만 필요)
 *    - getStocksAsList(): List 반환 (인덱스 접근 필요 - 메뉴 번호용)
 * 
 * 4. 사용 예시:
 *    Portfolio portfolio = new Portfolio();
 *    portfolio.addOrUpdateStock(new Stock("삼성전자", 70000, 10));
 *    
 *    Optional<Stock> stock = portfolio.findStockByName("삼성전자");
 *    if (stock.isPresent()) {
 *        System.out.println(stock.get());
 *    }
 */