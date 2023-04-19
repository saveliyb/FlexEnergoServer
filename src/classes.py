class Bet:
    """general lata class for easier access from DataFrame"""
    def __init__(self, id: int, user_id: int, bet: float, time: float, lot: float):
        self.id = id
        self.user_id = user_id
        self.bet = bet
        self.time = time
        self.lot = lot

    def __str__(self):
        s = str({
            "id": self.id,
            "user_id": self.user_id,
            "bet": self.bet,
            "time": self.time,
            "lot": self.lot
        })
        return s

    def dict(self):
        s = {
            "id": self.id,
            "user_id": self.user_id,
            "bet": self.bet,
            "time": self.time,
            "lot": self.lot
        }
        return s


