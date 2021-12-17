import os

class Utils:

    @staticmethod
    def reshape_tolist(nparray, shape):
        retlist = []
        _shape = shape
        for elem in nparray:
            retlist.append(elem)
        retlist.append(_shape[0])
        retlist.append(_shape[1])
        return retlist

    @staticmethod
    def screen_clear():
        # for mac and linux(here, os.name is 'posix')
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            # for windows platfrom
            _ = os.system('cls')
        # print out some text