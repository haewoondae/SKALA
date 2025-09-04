// 부모 클래스 Stock (보통주 기본 속성)
class Stock {
    private String name;    // 종목명
    private int price;      // 현재가
    private boolean votingRight; // 의결권 여부
    private boolean dividendPreference; // 배당우선권 여부

    public Stock(String name, int price, boolean votingRight, boolean dividendPreference) {
        this.name = name;
        this.price = price;
        this.votingRight = votingRight;
        this.dividendPreference = dividendPreference;
    }

    public Stock(String name2, int price2, int i) {
        //TODO Auto-generated constructor stub
    }

    // Getter & Setter
    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    public boolean hasVotingRight() {
        return votingRight;
    }

    public boolean hasDividendPreference() {
        return dividendPreference;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    // 정보 출력 (오버라이딩 목적)
    public String getInfo() {
        return String.format("[일반주] 종목: %s / 현재가: %d원 / 의결권: %s / 배당우선권: %s",
                name, price,
                votingRight ? "있음" : "없음",
                dividendPreference ? "있음" : "없음");
    }

    public int getQuantity() {
      // TODO Auto-generated method stub
      throw new UnsupportedOperationException("Unimplemented method 'getQuantity'");
    }

    public void setQuantity(int newQuantity) {
      // TODO Auto-generated method stub
      throw new UnsupportedOperationException("Unimplemented method 'setQuantity'");
    }
}

// 자식 클래스 PreferredStock (우선주)
class PreferredStock extends Stock {
    private double dividendRate; // 배당률 (%)

    public PreferredStock(String name, int price, double dividendRate, boolean votingRight, boolean dividendPreference) {
        super(name, price, votingRight, dividendPreference);
        this.dividendRate = dividendRate;
    }

    public double getDividendRate() {
        return dividendRate;
    }

    // 부모 getInfo 오버라이딩
    @Override
    public String getInfo() {
        return String.format("[우선주] 종목: %s / 현재가: %d원 / 배당률: %.1f%% / 의결권: %s / 배당우선권: %s",
                getName(), getPrice(), dividendRate,
                hasVotingRight() ? "있음" : "없음",
                hasDividendPreference() ? "있음" : "없음");
    }
}

public class StockTicker {
    public static void main(String[] args) {
        // 일반주 객체 생성
        Stock scalaEdu = new Stock("스칼라 에듀", 15000, true, false);
        // 우선주 객체 생성
        PreferredStock scalaAI = new PreferredStock("스칼라 AI", 17500, 5.0, false, true);

        // 초기 거래 내역 출력
        System.out.println(scalaEdu.getInfo());
        System.out.println(scalaAI.getInfo());

        // 가격 변경
        scalaEdu.setPrice(15800);
        scalaAI.setPrice(18000);

        System.out.println(scalaEdu.getName() + " 가격이 " + scalaEdu.getPrice() + "원으로 변경되었습니다.");
        System.out.println(scalaAI.getName() + " 가격이 " + scalaAI.getPrice() + "원으로 변경되었습니다.");

        // 가격 변경 후 정보 출력
        System.out.println("[가격 변경 후 정보]");
        System.out.println(scalaEdu.getInfo());
        System.out.println(scalaAI.getInfo());
    }
}
