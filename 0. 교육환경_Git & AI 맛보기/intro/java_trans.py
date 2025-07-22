class Stock:
    def __init__(self, ticker, company_name, current_price, change_percent, volume):
        self._ticker = ticker                 # 주식 종목 코드
        self._company_name = company_name     # 회사 이름
        self._current_price = current_price   # 현재 가격
        self._change_percent = change_percent # 변동률 (%)
        self._volume = volume                 # 거래량

    # ticker
    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, value):
        self._ticker = value

    # company_name
    @property
    def company_name(self):
        return self._company_name

    @company_name.setter
    def company_name(self, value):
        self._company_name = value

    # current_price
    @property
    def current_price(self):
        return self._current_price

    @current_price.setter
    def current_price(self, value):
        self._current_price = value

    # change_percent
    @property
    def change_percent(self):
        return self._change_percent

    @change_percent.setter
    def change_percent(self, value):
        self._change_percent = value

    # volume
    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
