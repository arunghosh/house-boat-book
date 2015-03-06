from exceptions import Exception


class UserNotCustomerException(Exception):

    def __str__(self):
        return "The user is not of type customer"
