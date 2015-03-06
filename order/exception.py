from exceptions import Exception


class NotAvailableException(Exception):

    def __str__(self):
        return "The boat is already book for the date"


class PastDateException(Exception):

    def __str__(self):
        return "Cannot create order for Past Date"


class CustomerCountException(Exception):

    def __str__(self):
        return "Number of passengers is more than the boat capacity"


class InvalidPriceException(Exception):

    def __str__(self):
        return "The price is invalid"
