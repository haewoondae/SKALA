import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * 플레이어 데이터를 파일에 저장하고 메모리에 로드합니다.
 */
public class PlayerRepository {
    private static final String PLAYER_FILE = "players.txt";
    private final Map<String, Player> playerMap = new LinkedHashMap<>();
    private final PlayerMapper mapper = new PlayerMapper();

    public void loadPlayerList() {
        try (BufferedReader reader = new BufferedReader(new FileReader(PLAYER_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                Player player = mapper.fromLine(line);
                if (player != null) {
                    playerMap.put(player.getId(), player);
                }
            }
        } catch (IOException e) {
            System.out.println("기존 플레이어 정보가 없습니다. 새로 시작합니다.");
        }
    }

    public void savePlayerList() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(PLAYER_FILE))) {
            for (Player player : playerMap.values()) {
                writer.write(mapper.toLine(player));
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("파일에 플레이어 정보를 저장하는 중 오류가 발생했습니다.");
        }
    }

    public Player findPlayer(String id) {
        return playerMap.get(id);
    }

    public void addPlayer(Player player) {
        playerMap.put(player.getId(), player);
    }
}