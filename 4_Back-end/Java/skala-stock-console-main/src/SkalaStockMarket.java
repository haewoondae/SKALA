import java.util.List;

/**
 * 프로그램의 시작점. 각 컴포넌트를 생성하고 전체 흐름을 제어합니다.
 */
public class SkalaStockMarket {
    private final PlayerRepository playerRepository;
    private final StockRepository stockRepository;
    private final StockService stockService;
    private final StockView stockView;
    private Player player;

    public SkalaStockMarket() {
        // 의존 객체 생성
        playerRepository = new PlayerRepository();
        stockRepository = new StockRepository();
        stockService = new StockService(stockRepository);
        stockView = new StockView();
    }

    public void start() {
        stockRepository.loadStockList();
        playerRepository.loadPlayerList();

        initializePlayer();
        stockView.displayPlayerInfo(player);

        mainLoop();

        stockView.showMessage("프로그램을 종료합니다...Bye");
        stockView.close();
    }

    private void initializePlayer() {
        String playerId = stockView.promptForPlayerId();
        player = playerRepository.findPlayer(playerId);
        if (player == null) {
            int money = stockView.promptForInitialMoney();
            player = new Player(playerId, money);
            playerRepository.addPlayer(player);
        }
    }

    private void mainLoop() {
        boolean running = true;
        while (running) {
            int code = stockView.showMenuAndGetSelection();
            switch (code) {
                case 1:
                    stockView.displayPlayerInfo(player);
                    break;
                case 2:
                    buyStock();
                    break;
                case 3:
                    sellStock();
                    break;
                case 0:
                    running = false;
                    break;
                default:
                    stockView.showMessage("올바른 번호를 선택하세요.");
            }
        }
    }

    // SkalaStockMarket.java의 buyStock 메서드 내부
    private void buyStock() {
        // 1. Repository에서 주식 '목록'을 먼저 가져옵니다.
        List<Stock> marketStocks = stockRepository.getAllStocks();

        // 2. 가져온 '목록'을 View에 전달하여 화면에 표시합니다.
        stockView.displayStockList(marketStocks);

        int index = stockView.getStockIndexFromUser();
        if (index >= 0 && index < marketStocks.size()) {
            Stock selectedStock = marketStocks.get(index);
            int quantity = stockView.getQuantityFromUser();
            String result = stockService.buyStock(player, selectedStock, quantity);
            stockView.showMessage(result);
        } else {
            stockView.showMessage("ERROR: 잘못된 선택입니다.");
        }
    }

    private void sellStock() {
        stockView.showMessage("\n판매할 주식 번호를 선택하세요:");
        stockView.displayPlayerInfo(player);

        List<Stock> playerStocks = player.getPortfolio().getStocksAsList();
        if (playerStocks.isEmpty()) {
            return;
        }

        int index = stockView.getStockIndexFromUser();

        if (index >= 0 && index < playerStocks.size()) {
            Stock stockToSell = playerStocks.get(index);
            int quantity = stockView.getQuantityFromUser();
            String result = stockService.sellStock(player, stockToSell, quantity);
            stockView.showMessage(result);
        } else {
            stockView.showMessage("ERROR: 잘못된 선택입니다.");
        }
    }
}