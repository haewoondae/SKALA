import { reactive } from "vue";
const storage = reactive({
	playerId: "",
	playerMoney: 0,
});

export const storePlayer = (player) => {
	storage.playerId = player.playerId;
	storage.playerMoney = player.playerMoney;
	sessionStorage.setItem("skala-stock-ui", JSON.stringify(player));
};

export const usePlayer = () => {
	const item = sessionStorage.getItem("skala-stock-ui");
	if (item) {
		const player = JSON.parse(item);
		storage.playerId = player.playerId;
		storage.playerMoney = player.playerMoney;
	}
	return storage;
};
