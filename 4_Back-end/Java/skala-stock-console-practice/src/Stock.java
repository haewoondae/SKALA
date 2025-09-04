/**
 * 주식의 이름, 가격, 수량을 저장하는 데이터 클래스입니다.
 * 
 * 주요 개념 설명:
 * - DTO(Data Transfer Object): 데이터를 담는 가장 기본적인 데이터 객체
 * - 캡슐화(Encapsulation): private 필드 + public getter/setter로 데이터 보호
 */
public class Stock {
    // private 키워드: 외부에서 직접 접근 불가 (캡슐화의 핵심)
    private String name;
    private int price;
    private int quantity;

    /**
     * 모든 속성을 초기화하는 생성자
     * @param name 주식 종목명
     * @param price 현재 주식 가격
     * @param quantity 보유 수량
     */
    public Stock(String name, int price, int quantity) {
        // this 키워드: "현재 객체 자기 자신"을 가리키는 참조
        // 매개변수와 필드 이름이 같을 때 구분하기 위해 필수 사용
        this.name = name;        // this.name(필드) = name(매개변수)
        this.price = price;      // this가 없으면 매개변수 = 매개변수가 됨 (필드 변경 안됨!)
        this.quantity = quantity;
    }

    // Getters: private 필드의 값을 안전하게 읽는 메서드 (읽기 전용 접근)
    // 캡슐화를 통해 필드를 직접 노출하지 않으면서도 값을 읽을 수 있게 함
    public String getName() {
        return name;
    }
    
    public int getPrice() {
        return price;
    }
    
    public int getQuantity() {
        return quantity;
    }

    // Setters: private 필드의 값을 안전하게 변경하는 메서드 (쓰기 접근)
    // 나중에 유효성 검사 로직을 추가할 수 있어서 직접 접근보다 안전함
    // 예: if(price >= 0) 같은 조건 추가 가능
    public void setName(String name) {
        this.name = name;  // this 필수: 매개변수 name과 필드 name 구분
    }
    
    public void setPrice(int price) {
        this.price = price;  // this 없으면: price = price (아무것도 안 바뀜)
    }
    
    public void setQuantity(int quantity) {
        this.quantity = quantity;  // this로 "이 객체의 필드"임을 명시
    }

    /**
     * 객체 정보를 쉽게 출력할 수 있도록 toString() 메서드 재정의
     * 출력 형식: "종목: TechCorp, 현재가: 152, 보유수량: 10"
     * @return 주식 정보를 포맷된 문자열로 반환
     */
    @Override
    public String toString() {
        return "종목: " + name + ", 현재가: " + price + ", 보유수량: " + quantity;
    }
}

/*
 * 💡 핵심 개념 요약:
 * 
 * 1. 캡슐화 = private 필드 + public getter/setter
 *    - 데이터 보호 및 안전한 접근 제어
 *    - 나중에 유효성 검사나 추가 로직 삽입 가능
 * 
 * 2. this 키워드
 *    - "현재 객체 자기 자신"을 가리킴
 *    - 매개변수와 필드 이름이 같을 때 구분 용도로 필수
 *    - this.필드명 = 매개변수명; 형태로 사용
 * 
 * 3. 사용 예시:
 *    Stock stock = new Stock("삼성전자", 70000, 10);
 *    System.out.println(stock.getName());     // getter로 읽기
 *    stock.setPrice(75000);                   // setter로 변경
 *    System.out.println(stock);               // toString() 자동 호출
 */