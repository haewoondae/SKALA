import java.util.ArrayList;
import java.util.List;

public class StockSorter {
    public static void main(String[] args) {
        // 5개의 주식을 리스트에 저장
        List<String> stocks = new ArrayList<>();
        stocks.add("SKALA 에듀");
        stocks.add("SKALA AI");
        stocks.add("K-테크");
        stocks.add("SKALA 테크");
        stocks.add("N-솔루션");
        
        // 정렬 전 주식 목록을 System.out의 method reference를 사용하여 출력
        System.out.println("# 정렬 전 주식 목록:");
        stocks.forEach(System.out::println);
        
        // 주식 목록을 String의 compareTo 메서드 참조를 사용해 오름차순 정렬
        stocks.sort(String::compareTo);
        
        // 정렬 후 주식 목록 출력
        System.out.println("# 정렬 후 주식 목록 (오름차순):");
        stocks.forEach(System.out::println);
    }
}