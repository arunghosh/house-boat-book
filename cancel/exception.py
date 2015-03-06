from exceptions import Exception


class InvalidPolicyException(Exception):

    def __str__(self):
        return "The policy values is invalid"


class AlreadyExistException(Exception):

    def __str__(self):
        return "Cancellation policy for the given days already exist"

class AlreadyCancelledException(Exception):

    def __str__(self):
        return "The order has been cancelled"


class InvalidOrderReqException(Exception):

    def __str__(self):
        return "Invalid Order ID or Email address"

# class ValidCancelationPolicy