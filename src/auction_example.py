from copy import deepcopy
from pprint import pprint
import logging


class Auction:
    def __init__(self):
        self.lots_for_sale = []
        self.lots_wanted = []
        self.deals = []
        self.log_file = 'auction_logs.txt'
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def add_bet_sell(self, quantity: float, price, seller: str = None):
        if seller:
            lot = {'seller': seller, 'quantity': quantity, 'price': price}
        else:
            indexes = set([i["seller"] for i in self.lots_for_sale if type(i["seller"]) == int])
            if len(indexes) > 0:
                lot = {'seller': str(max(indexes) + 1), 'quantity': quantity, 'price': price}
            else:
                lot = {'seller': "1", 'quantity': quantity, 'price': price}

        self.lots_for_sale.append(lot)
        logging.info(f"Added lot for sale: {lot}")

    def add_bet_buy(self, quantity: float, price, buyer: str = None):
        # lot = {'buyer': buyer, 'quantity': quantity, 'price': price}
        if buyer:
            lot = {'buyer': buyer, 'quantity': quantity, 'price': price}
        else:
            indexes = set([i["buyer"] for i in self.lots_wanted if type(i["buyer"]) == int])
            if len(indexes) > 0:
                lot = {'buyer': str(max(indexes) + 1), 'quantity': quantity, 'price': price}
            else:
                lot = {'buyer': "1", 'quantity': quantity, 'price': price}

        self.lots_wanted.append(lot)
        logging.info(f"Added lot wanted: {lot}")

    def run_auction(self):
        # Сортируем лоты на продажу по возрастанию цены
        self.lots_for_sale = sorted(self.lots_for_sale, key=lambda lot: lot['price'])
        # Сортируем лоты на покупку по убыванию цены
        self.lots_wanted = sorted(self.lots_wanted, key=lambda lot: lot['price'], reverse=True)
        deals = []
        # Проходимся по лотам на продажу и пытаемся найти совпадения с лотами на покупку
        for lot_for_sale in self.lots_for_sale:
            for lot_wanted in self.lots_wanted:
                if lot_wanted['price'] >= lot_for_sale['price']:
                    # Вычисляем количество энергии, которую можно продать по данной цене
                    quantity = min(lot_for_sale['quantity'], lot_wanted['quantity'])
                    # Создаем сделку
                    deal = {
                        'seller': lot_for_sale['seller'],
                        'buyer': lot_wanted['buyer'],
                        'quantity': quantity,
                        'price': lot_for_sale['price']
                    }
                    # Добавляем сделку в список сделок
                    deals.append(deal)
                    # Обновляем количество энергии в лотах на продажу и на покупку
                    lot_for_sale['quantity'] -= quantity
                    lot_wanted['quantity'] -= quantity
                    # Если лот на продажу полностью продан, удаляем его из списка лотов на продажу
                    if lot_for_sale['quantity'] == 0:
                        self.lots_for_sale.remove(lot_for_sale)
                    # Если лот на покупку полностью куплен, удаляем его из списка лотов на покупку
                    if lot_wanted['quantity'] == 0:
                        self.lots_wanted.remove(lot_wanted)
                    # Прерываем цикл по лотам на покупку, чтобы перейти к следующему лоту на продажу
                    break

        # Возвращаем список сделок
        self.close_auction()
        # Обновляем результат
        self.deals = deepcopy(deals)
        logging.info(f"Deals: {self.deals}")
        return self.deals

    def vcg(self):
        return self.run_auction()

    def result(self):
        return self.deals

    def close_auction(self):
        self.lots_for_sale.clear()
        self.lots_wanted.clear()


if __name__ == "__main__":
    """
    Пример аукциона VCG
    """
    # import pandas as pd
    import numpy as np

    a = Auction()
    for _ in range(5):
        for i in "high mid low".split():
            a.add_bet_sell(np.random.randint(1, 100), np.random.randint(1, 100), seller=i)
        for i in "one two three four five six seven eight nine ten".split():
            a.add_bet_buy(np.random.randint(1, 10), np.random.randint(1, 25), buyer=i)
        a.vcg()
    # print(a.log)
    pprint(a.deals)