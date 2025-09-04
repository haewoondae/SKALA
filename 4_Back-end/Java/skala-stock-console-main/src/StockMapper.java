/**
 * Stock 객체와 파일 데이터(문자열)를 상호 변환합니다.
 */
public class StockMapper {
    public Stock fromLine(String line) {
        String[] fields = line.split(",");
        if (fields.length == 2) {
            String name = fields[0];
            int price = Integer.parseInt(fields[1]);
            return new Stock(name, price, 0);
        }
        return null;
    }

    public String toLine(Stock stock) {
        return stock.getName() + "," + stock.getPrice();
    }
}