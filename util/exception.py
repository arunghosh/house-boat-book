from exceptions import Exception

class CannotUpdateException(Exception):

    def __str__(self):
        return "This model cannot be updated"


class AccessDeniedException(Exception):

    def __str__(self):
        return "Access Denied"


class InvalidFomToException(Exception):

    def __str__(self):
        return "From date should be less than To date"


class PastDateException(Exception):

    def __str__(self):
        return "Date cannot be a past date"
