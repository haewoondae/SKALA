import java.util.Collection;
import java.util.stream.Collectors;

/**
 * Player 객체와 파일 데이터(문자열)를 상호 변환합니다.
 */
public class PlayerMapper {
    public Player fromLine(String line) {
        String[] fields = line.split(",", 3);
        if (fields.length < 2)
            return null;

        String id = fields[0];
        int money = Integer.parseInt(fields[1]);
        Player player = new Player(id, money);

        if (fields.length == 3 && !fields[2].isEmpty()) {
            String[] stockData = fields[2].split("\\|");
            for (String s : stockData) {
                String[] stockProps = s.split(":");
                if (stockProps.length == 3) {
                    String name = stockProps[0];
                    int price = Integer.parseInt(stockProps[1]);
                    int quantity = Integer.parseInt(stockProps[2]);
                    player.getPortfolio().addOrUpdateStock(new Stock(name, price, quantity));
                }
            }
        }
        return player;
    }

    public String toLine(Player player) {
        StringBuilder sb = new StringBuilder();
        sb.append(player.getId()).append(",").append(player.getMoney());

        Collection<Stock> stocks = player.getPortfolio().getAllStocks();
        if (!stocks.isEmpty()) {
            sb.append(",");
            String stockData = stocks.stream()
                    .map(stock -> String.join(":", stock.getName(), String.valueOf(stock.getPrice()),
                            String.valueOf(stock.getQuantity())))
                    .collect(Collectors.joining("|"));
            sb.append(stockData);
        }
        return sb.toString();
    }
}