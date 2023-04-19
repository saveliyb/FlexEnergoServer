from copy import deepcopy
from pprint import pprint
import logging
# from datetime import datetime
# import os


class Auction:
    def __init__(self, log_file: str = "var/log/auction_logs.txt"):
        self.lots_for_sale = []
        self.lots_wanted = []
        self.deals = []
        self.dump_lots_for_sale = []
        # log_file = '/'.join(os.path.abspath(__file__).split('\\')[:-2]) \
        #            + f'/var/log/auction_logs_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.txt'
        # log_file = f'var/log/auction_logs_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.txt'
        # with open(log_file, "w+") as file:
        #     file.close()
        # log_file = f'.\\var\\log\\auction_logs_{datetime.now().strftime("%d:%m:%Y_%H:%M:%S")}.txt'
        logging.basicConfig(filename=log_file, level=logging.INFO)

    def add_bet_sell(self, quantity: float, price, seller: str = None):
        # Убираем float для более точных расчетов
        quantity = int(quantity * 1_000)
        price = int(price * 100)
        if seller:
            lot = {'seller': seller, 'quantity': quantity, 'price': price}
        else:
            indexes = set([i["seller"] for i in self.lots_for_sale if type(i["seller"]) == int])
            if len(indexes) > 0:
                lot = {'seller': str(max(indexes) + 1), 'quantity': quantity, 'price': price}
            else:
                lot = {'seller': "1", 'quantity': quantity, 'price': price}

        self.lots_for_sale.append(lot)
        logging.info(f"Added lot for sale: {lot}\t\t| * 1_000; * 100")

    def add_bet_buy(self, quantity: float, price, buyer: str = None):
        # Убираем float для более точных расчетов
        quantity = int(quantity * 1_000)
        price = int(price * 100)
        if buyer:
            lot = {'buyer': buyer, 'quantity': quantity, 'price': price}
        else:
            indexes = set([i["buyer"] for i in self.lots_wanted if type(i["buyer"]) == int])
            if len(indexes) > 0:
                lot = {'buyer': str(max(indexes) + 1), 'quantity': quantity, 'price': price}
            else:
                lot = {'buyer': "1", 'quantity': quantity, 'price': price}

        self.lots_wanted.append(lot)
        logging.info(f"Added lot wanted: {lot}\t\t| * 1_000; * 100")

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

        logging.info(f"Remain sellers: {len(self.lots_for_sale)}\n\t{self.lots_for_sale}")
        logging.info(f"Remain buyers: {len(self.lots_wanted)}\n\t{self.lots_wanted}")
        self.close_auction()
        # Возвращаем float
        lst = []
        for elem in deals:
            elem["quantity"] /= 1000
            elem["price"] /= 100
            lst.append(elem)
        deals = deepcopy(lst)
        # Обновляем результат
        self.deals = deepcopy(deals)
        logging.info(f"Deals: {self.deals}")
        # Возвращаем список сделок
        return self.deals

    def vcg(self):
        return self.run_auction()

    def result(self):
        return self.deals

    def not_purchased_lots(self):
        return self.dump_lots_for_sale

    def close_auction(self):
        lst = []
        for elem in self.lots_for_sale:
            elem["quantity"] /= 1000
            lst.append(elem)
        self.dump_lots_for_sale = deepcopy(lst)
        self.lots_for_sale.clear()
        self.lots_wanted.clear()


if __name__ == "__main__":
    """
    Пример аукциона VCG
    """
    # import pandas as pd
    import random

    a = Auction()
    for _ in range(5):
        for i in "01 02 03 04 05 06 07 08 09 10".split():
            a.add_bet_sell(random.randint(1, 1_000), random.randint(1, 10_000), seller=i)
        for i in "one two three four five six seven eight nine ten".split():
            a.add_bet_buy(random.randint(1, 100), random.randint(1, 1_000), buyer=i)
        a.vcg()
    # print(a.log)
    pprint(a.deals)
