from exceptions import Exception


class OrderExistException(Exception):

    def __str__(self):
        return "An order exist in the given period"
