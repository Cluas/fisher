class Book:

    def __init__(self, book):
        self.title = book['title']
        self.isbn = book['isbn']
        self.author = '、'.join(book['author'])
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.price = book['price']
        self.summary = book['summary'] or ''
        self.image = book['image']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = (i for i in (self.author, self.publisher, self.price) if i)
        return '/'.join(intros)


class Books:

    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, book, keyword):
        self.total = book.total
        self.keyword = keyword
        self.books = [Book(b) for b in book.books]


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    @staticmethod
    def __map_to_trade(single):
        time = single.create_datetime.strftime('%y-%m-%d') if single.create_datetime else '未知'
        return dict(
            username=single.user.nickname,
            time=time,
            id=single.id
        )
