import java.util.HashMap;
import java.util.Scanner;

public class StockHash {
  public static void main(String[] args) {
    // 초기 보유 종목 등록
    HashMap<String, Integer> portfolio = new HashMap<>();
    portfolio.put("SKALA 에듀", 12);
    portfolio.put("SKALA AI", 8);
    portfolio.put("SKALA 에너지", 5);
    
    Scanner scanner = new Scanner(System.in);
    
    while (true) {
      System.out.print("조회할 주식명을 입력하세요: ");
      String stockName = scanner.nextLine();
      
      // 프로그램 종료 조건
      if (stockName.equals("exit") || stockName.equals("종료")) {
        break;
      }
      
      // getOrDefault()를 사용해 없는 종목은 0으로 처리
      int quantity = portfolio.getOrDefault(stockName, 0);
      
      if (quantity > 0) {
        System.out.println(stockName + " 주식을 " + quantity + "주 보유 중입니다.");
      } else {
        System.out.println("해당 주식을 보유하고 있지 않습니다.");
      }
    }
    
    scanner.close();
  }
}