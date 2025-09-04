import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * 주식 데이터를 파일에 저장하고 메모리에 로드합니다.
 * 
 * 핵심 개념:
 * - Repository 패턴: 데이터 접근 로직을 캡슐화
 * - 파일 I/O: BufferedReader/Writer로 효율적인 파일 읽기/쓰기
 * - 예외 처리: 파일이 없을 때 기본 데이터로 초기화
 */
public class StockRepository {
    private static final String STOCK_FILE = "stocks.txt";
    private final List<Stock> stockList = new ArrayList<>();
    // StockMapper는 static 메서드만 있으므로 인스턴스 생성 불필요
    // private final StockMapper mapper = new StockMapper(); // 제거

    /**
     * 파일에서 주식 데이터를 로드합니다. 파일이 없으면 기본 주식 목록을 생성합니다.
     */
    public void loadStockList() {
        try (BufferedReader reader = new BufferedReader(new FileReader(STOCK_FILE))) {
            // 기존 데이터 클리어
            stockList.clear();
            
            String line;
            // 파일의 각 라인을 읽어서 Stock 객체로 변환
            while ((line = reader.readLine()) != null) {
                try {
                    // StockMapper를 사용하여 문자열을 Stock 객체로 변환
                    Stock stock = StockMapper.fromLine(line);
                    stockList.add(stock);
                } catch (IllegalArgumentException e) {
                    // 잘못된 형식의 라인은 건너뛰고 로그 출력
                    System.err.println("잘못된 주식 데이터를 건너뜁니다: " + line + " (" + e.getMessage() + ")");
                }
            }
            
            System.out.println("주식 데이터 " + stockList.size() + "개를 파일에서 로드했습니다.");
            
        } catch (IOException e) {
            // 파일이 없거나 읽기 실패 시 기본 주식 목록 생성
            System.out.println("주식 파일을 찾을 수 없습니다. 기본 주식 목록을 생성합니다.");
            initializeDefaultStocks();
            // 기본 데이터를 파일에 저장
            saveStockList();
        }
    }

    /**
     * 현재 주식 목록을 파일에 저장합니다.
     */
    public void saveStockList() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(STOCK_FILE))) {
            for (Stock stock : stockList) {
                // StockMapper를 사용하여 Stock 객체를 문자열로 변환 후 저장
                String line = StockMapper.toLine(stock);
                writer.write(line);
                writer.newLine(); // 줄바꿈 추가
            }
            System.out.println("주식 데이터 " + stockList.size() + "개를 파일에 저장했습니다.");
            
        } catch (IOException e) {
            System.err.println("주식 데이터 저장 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 기본 주식 목록을 생성합니다. (파일이 없을 때 사용)
     */
    private void initializeDefaultStocks() {
        stockList.clear(); // 기존 데이터 클리어
        
        // 기본 주식 데이터 추가 (수량은 0으로 - 시장 데이터이므로)
        stockList.add(new Stock("TechCorp", 152, 0));
        stockList.add(new Stock("GreenEnergy", 88, 0));
        stockList.add(new Stock("HealthPlus", 210, 0));
        stockList.add(new Stock("BioGen", 75, 0));
        
        System.out.println("기본 주식 목록 " + stockList.size() + "개를 생성했습니다.");
    }

    /**
     * 전체 주식 목록을 반환합니다.
     * @return 주식 목록의 복사본 (원본 보호)
     */
    public List<Stock> getAllStocks() {
        // 원본 리스트의 복사본을 반환하여 외부에서 수정하지 못하게 보호
        return new ArrayList<>(stockList);
    }

    /**
     * 인덱스로 주식을 검색합니다.
     * @param index 검색할 주식의 인덱스 (0부터 시작)
     * @return 해당 인덱스의 주식, 인덱스가 유효하지 않으면 null
     */
    public Stock findStock(int index) {
        // 인덱스 유효성 검사
        if (index < 0 || index >= stockList.size()) {
            return null; // 유효하지 않은 인덱스
        }
        
        // 해당 인덱스의 주식 반환
        return stockList.get(index);
    }

    /**
     * 주식 이름으로 주식을 검색합니다.
     * @param name 검색할 주식의 이름
     * @return 해당 이름의 주식, 찾지 못하면 null
     */
    public Stock findStock(String name) {
        // null이나 빈 문자열 체크
        if (name == null || name.trim().isEmpty()) {
            return null;
        }
        
        // 이름으로 주식 검색 (대소문자 구분 없이)
        for (Stock stock : stockList) {
            if (stock.getName().equalsIgnoreCase(name.trim())) {
                return stock;
            }
        }
        
        // 찾지 못했을 경우
        return null;
    }

    /**
     * 현재 로드된 주식 개수를 반환합니다.
     * @return 주식 개수
     */
    public int getStockCount() {
        return stockList.size();
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. Repository 패턴:
 *    - 데이터 접근 로직을 한 곳에 모아서 관리
 *    - 파일 I/O, 검색, 저장 등의 기능을 캡슐화
 * 
 * 2. try-with-resources:
 *    - try (BufferedReader reader = ...) 형태
 *    - 자동으로 리소스를 닫아줌 (메모리 누수 방지)
 * 
 * 3. 방어적 복사:
 *    - getAllStocks()에서 new ArrayList<>(stockList) 반환
 *    - 외부에서 원본 리스트를 수정하지 못하게 보호
 * 
 * 4. 예외 처리 전략:
 *    - IOException: 파일 관련 오류 → 기본 데이터 생성
 *    - IllegalArgumentException: 잘못된 데이터 → 건너뛰기
 * 
 * 5. 사용 예시:
 *    StockRepository repo = new StockRepository();
 *    repo.loadStockList();                    // 파일에서 로드
 *    List<Stock> stocks = repo.getAllStocks(); // 전체 목록 조회
 *    Stock stock = repo.findStock("TechCorp"); // 이름으로 검색
 *    Stock stock2 = repo.findStock(0);        // 인덱스로 검색
 */