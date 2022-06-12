from abc import ABC, abstractmethod


class Field:
    def __init__(self, mine):
        self.__mine = mine
        self.__flag = False
        self.__revealed = False
        self.__tangentMineCount = 0
        self.__tangentFlagCount = 0

    def is_mined(self):
        return self.__mine

    def is_flagged(self):
        return self.__flag

    def is_revealed(self):
        return self.__revealed

    def get_tangent_mine_count(self):
        return self.__tangentMineCount

    def get_tangent_flag_count(self):
        return self.__tangentFlagCount

    def set_mine(self, mine):
        self.__mine = mine

    def toggle_flag(self):
        self.__flag = not self.__flag

    def set_revealed(self):
        self.__revealed = True

    def set_tangent_mine_count(self, count):
        self.__tangentMineCount = count

    def inc_tangent_mine_count(self):
        self.__tangentMineCount += 1

    def dec_tangent_mine_count(self):
        self.__tangentMineCount -= 1

    def inc_tangent_flag_count(self):
        self.__tangentFlagCount += 1

    def dec_tangent_flag_count(self):
        self.__tangentFlagCount -= 1
