/**
 * 주식 거래 관련 비즈니스 로직을 처리합니다.
 */
public class StockService {
    private final StockRepository stockRepository;

    public StockService(StockRepository stockRepository) {
        this.stockRepository = stockRepository;
    }

    public String buyStock(Player player, Stock stockToBuy, int quantity) {
        if (quantity <= 0) {
            return "ERROR: 구매 수량은 1 이상이어야 합니다.";
        }
        int totalCost = stockToBuy.getPrice() * quantity;
        if (player.getMoney() < totalCost) {
            return "ERROR: 금액이 부족합니다.";
        }
        player.setMoney(player.getMoney() - totalCost);
        Stock purchasedStock = new Stock(stockToBuy.getName(), stockToBuy.getPrice(), quantity);
        player.getPortfolio().addOrUpdateStock(purchasedStock);
        return quantity + "주를 성공적으로 구매했습니다! (남은 금액: " + player.getMoney() + ")";
    }

    public String sellStock(Player player, Stock stockToSell, int quantity) {
        if (quantity <= 0) {
            return "ERROR: 판매 수량은 1 이상이어야 합니다.";
        }
        if (quantity > stockToSell.getQuantity()) {
            return "ERROR: 보유 수량이 부족합니다.";
        }
        Stock marketStock = stockRepository.findStock(stockToSell.getName());
        if (marketStock == null) {
            return "ERROR: 판매하려는 주식이 시장에 존재하지 않습니다.";
        }
        int earnings = marketStock.getPrice() * quantity;
        player.setMoney(player.getMoney() + earnings);
        Stock stockUpdate = new Stock(
                stockToSell.getName(),
                marketStock.getPrice(),
                stockToSell.getQuantity() - quantity);
        player.getPortfolio().updateStock(stockUpdate);
        return quantity + "주를 성공적으로 판매했습니다! (현재 금액: " + player.getMoney() + ")";
    }
}