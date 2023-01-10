from prettytable import PrettyTable


class PIF:
    def __init__(self):
        self._pif = []

    def addToPIF(self, token, st_pos):
        pair = (token, st_pos)
        self._pif.append(pair)

    def __str__(self):
        result = PrettyTable(['TOKEN', 'ST_POS'])

        for pair in self._pif:
            result.add_row([str(pair[0]), str(pair[1])])

        return str(result)
