from app.book.viewmodels import Book


class Trades:
    def __init__(self, trades, trade_count_list):
        self.trades = []
        self._trades = trades
        self._trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        trades = []
        for trade in self._trades:
            trades.append(self.__match(trade))
        return trades

    def __match(self, trade):
        count = 0
        for trade_count in self._trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        trade = {
            'id': trade.id,
            'book': Book(trade.book),
            'trade_count': count
        }
        return trade

