public class StarPrint {
  public static void main(String[] args) {
    // 왼쪽 정렬된 별 피라미드 출력
    for (int i = 1; i < 6; i++) {
      for (int j = 1; j <= i; j++) {
        System.out.print("*");
      }
      System.out.println();
    }

    System.out.println(); // 구분을 위한 빈 줄

    // 가운데 정렬된 별 피라미드 (1, 3, 5, 7, 9개)
    for (int i = 1; i <= 5; i++) {
      System.out.println(" ".repeat(5 - i) + "*".repeat(2 * i - 1));
    }
  }
}