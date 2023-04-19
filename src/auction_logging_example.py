import logging


class Auction:
    def __init__(self):
        self.lots_for_sale = []
        self.lots_wanted = []
        self.deals = []
        self.log_file = 'auction_logs.txt'
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def add_lot_for_sale(self, seller, quantity, price):
        lot = {'seller': seller, 'quantity': quantity, 'price': price}
        self.lots_for_sale.append(lot)
        logging.info(f"Added lot for sale: {lot}")

    def add_lot_wanted(self, buyer, quantity, price):
        lot = {'buyer': buyer, 'quantity': quantity, 'price': price}
        self.lots_wanted.append(lot)
        logging.info(f"Added lot wanted: {lot}")

    def run_auction(self):
        # Сортируем лоты на продажу по возрастанию цены
        self.lots_for_sale = sorted(self.lots_for_sale, key=lambda lot: lot['price'])
        # Сортируем лоты на покупку по убыванию цены
        self.lots_wanted = sorted(self.lots_wanted, key=lambda lot: lot['price'], reverse=True)

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
                    self.deals.append(deal)
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
        # Записываем результаты аукциона в файл логов
        logging.info(f"Deals: {self.deals}")
        # Возвращаем список сделок
        return self.deals


# Создаем экземпляр аукциона
auction = Auction()

# Добавляем лоты на продажу и на покупку
auction.add_lot_for_sale('bob', 2.5, 5)
auction.add_lot_for_sale('anna', 3.5, 10)
auction.add_lot_wanted('sava', 1, 7)
auction.add_lot_wanted('jenya', 6, 4)

# Запускаем аукцион и выводим список сделок
print(auction.run_auction())
