import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * 플레이어 데이터를 파일에 저장하고 메모리에 로드합니다.
 * 
 * 핵심 개념:
 * - Repository 패턴: 데이터 접근 로직을 캡슐화
 * - Map 기반 저장소: 플레이어 ID로 O(1) 시간에 빠른 검색
 * - PlayerMapper 활용: 객체 ↔ 문자열 변환 위임
 */
public class PlayerRepository {
    private static final String PLAYER_FILE = "players.txt";
    // LinkedHashMap: 삽입 순서를 유지하면서 빠른 검색 제공
    private final Map<String, Player> playerMap = new LinkedHashMap<>();
    // PlayerMapper는 static 메서드만 있으므로 인스턴스 불필요
    // private final PlayerMapper mapper = new PlayerMapper(); // 제거

    /**
     * 파일에서 플레이어 데이터를 로드합니다.
     * 파일이 없으면 빈 저장소로 시작합니다.
     */
    public void loadPlayerList() {
        try (BufferedReader reader = new BufferedReader(new FileReader(PLAYER_FILE))) {
            // 기존 데이터 클리어
            playerMap.clear();
            
            String line;
            int loadedCount = 0;
            
            // 파일의 각 라인을 읽어서 Player 객체로 변환
            while ((line = reader.readLine()) != null) {
                try {
                    // PlayerMapper를 사용하여 문자열을 Player 객체로 변환
                    Player player = PlayerMapper.fromLine(line);
                    // Map에 저장 (플레이어 ID를 키로 사용)
                    playerMap.put(player.getId(), player);
                    loadedCount++;
                    
                } catch (IllegalArgumentException e) {
                    // 잘못된 형식의 라인은 건너뛰고 로그 출력
                    System.err.println("잘못된 플레이어 데이터를 건너뜁니다: " + line + " (" + e.getMessage() + ")");
                }
            }
            
            System.out.println("플레이어 데이터 " + loadedCount + "개를 파일에서 로드했습니다.");
            
        } catch (IOException e) {
            // 파일이 없거나 읽기 실패 시 (신규 사용자들을 위해 빈 저장소로 시작)
            System.out.println("플레이어 파일을 찾을 수 없습니다. 새로운 저장소를 시작합니다.");
            playerMap.clear(); // 빈 상태로 초기화
        }
    }

    /**
     * 현재 메모리의 모든 플레이어 데이터를 파일에 저장합니다.
     */
    public void savePlayerList() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(PLAYER_FILE))) {
            int savedCount = 0;
            
            // Map의 모든 Player 객체를 파일에 저장
            for (Player player : playerMap.values()) {
                try {
                    // PlayerMapper를 사용하여 Player 객체를 문자열로 변환
                    String line = PlayerMapper.toLine(player);
                    writer.write(line);
                    writer.newLine(); // 줄바꿈 추가
                    savedCount++;
                    
                } catch (IllegalArgumentException e) {
                    // 변환 실패한 플레이어는 건너뛰고 로그 출력
                    System.err.println("플레이어 저장 실패: " + player.getId() + " (" + e.getMessage() + ")");
                }
            }
            
            System.out.println("플레이어 데이터 " + savedCount + "개를 파일에 저장했습니다.");
            
        } catch (IOException e) {
            System.err.println("플레이어 데이터 저장 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 플레이어 ID로 플레이어를 검색합니다.
     * 
     * @param id 검색할 플레이어 ID
     * @return 해당 ID의 플레이어, 찾지 못하면 null
     */
    public Player findPlayer(String id) {
        // null이나 빈 문자열 체크
        if (id == null || id.trim().isEmpty()) {
            return null;
        }
        
        // Map에서 O(1) 시간에 검색
        return playerMap.get(id.trim());
    }

    /**
     * 새로운 플레이어를 저장소에 추가하거나 기존 플레이어 정보를 업데이트합니다.
     * 
     * @param player 추가하거나 업데이트할 플레이어
     * @throws IllegalArgumentException player가 null이거나 ID가 유효하지 않은 경우
     */
    public void addPlayer(Player player) {
        // 유효성 검사
        if (player == null) {
            throw new IllegalArgumentException("Player 객체가 null입니다.");
        }
        
        String playerId = player.getId();
        if (playerId == null || playerId.trim().isEmpty()) {
            throw new IllegalArgumentException("플레이어 ID가 유효하지 않습니다.");
        }
        
        // Map에 저장 (기존 플레이어가 있으면 덮어쓰기)
        Player existingPlayer = playerMap.put(playerId, player);
        
        if (existingPlayer != null) {
            System.out.println("기존 플레이어 '" + playerId + "'의 정보를 업데이트했습니다.");
        } else {
            System.out.println("새로운 플레이어 '" + playerId + "'를 추가했습니다.");
        }
    }

    /**
     * 현재 저장된 플레이어 수를 반환합니다.
     * 
     * @return 플레이어 수
     */
    public int getPlayerCount() {
        return playerMap.size();
    }

    /**
     * 특정 플레이어 ID가 존재하는지 확인합니다.
     * 
     * @param id 확인할 플레이어 ID
     * @return 존재하면 true, 아니면 false
     */
    public boolean containsPlayer(String id) {
        if (id == null || id.trim().isEmpty()) {
            return false;
        }
        return playerMap.containsKey(id.trim());
    }
}

/*
 * 💡 핵심 개념 설명:
 * 
 * 1. Repository 패턴:
 *    - 데이터 접근 로직을 한 곳에 캡슐화
 *    - 파일 I/O, 검색, 저장 등의 기능을 통합 관리
 * 
 * 2. Map<String, Player> 사용 이유:
 *    - 플레이어 ID로 O(1) 시간에 빠른 검색
 *    - LinkedHashMap으로 삽입 순서도 보장
 * 
 * 3. PlayerMapper 위임:
 *    - 객체 ↔ 문자열 변환 로직을 PlayerMapper에 위임
 *    - 단일 책임 원칙 준수
 * 
 * 4. 예외 처리 전략:
 *    - IOException: 파일 관련 오류 → 빈 저장소로 시작
 *    - IllegalArgumentException: 잘못된 데이터 → 건너뛰기
 * 
 * 5. 파일 형식 예시 (players.txt):
 *    김철수,1000000,삼성전자:70000:10|LG전자:80000:5
 *    이영희,500000,TechCorp:152:3
 *    박민수,2000000
 * 
 * 6. 사용 예시:
 *    PlayerRepository repo = new PlayerRepository();
 *    repo.loadPlayerList();                    // 파일에서 로드
 *    Player player = repo.findPlayer("김철수"); // 검색
 *    repo.addPlayer(newPlayer);                // 추가
 *    repo.savePlayerList();                    // 파일에 저장
 */