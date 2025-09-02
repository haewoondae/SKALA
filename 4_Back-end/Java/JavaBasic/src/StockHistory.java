import java.text.DecimalFormat;

public class StockHistory {
    public static void main(String[] args) {
        String[] stocks = {"SKALA", "EDUAI", "KQTECH"};
        int[] prices = {12300, 9850, 23000};
        int[] yesterdayPrices = {12000, 10200, 22000};

        // 가격에 천 단위 콤마를 표시하기 위한 DecimalFormat
        DecimalFormat priceFormat = new DecimalFormat("#,###");
        // 등락률을 소수점 2자리까지 표시하기 위한 DecimalFormat
        DecimalFormat rateFormat = new DecimalFormat("+#0.00%;-#0.00%");

        StringBuilder sb = new StringBuilder();
        sb.append(String.format("%-8s %10s %10s %8s\n", "종목명", "전일가", "현재가", "등락률"));

        for (int i = 0; i < stocks.length; i++) {
            double rate = (double)(prices[i] - yesterdayPrices[i]) / yesterdayPrices[i];
            sb.append(String.format("%-8s %10s %10s %8s\n",
                    stocks[i],
                    priceFormat.format(yesterdayPrices[i]),
                    priceFormat.format(prices[i]),
                    rateFormat.format(rate)
            ));
        }

        System.out.println(sb.toString());
    }
}
