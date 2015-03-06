from exceptions import Exception


class InvalidDateException(Exception):

    def __str__(self):
        return "From date should be less than To date"


class DatePriceNotFoundException(Exception):

    def __str__(self):
        return "Price for the given date not defined"