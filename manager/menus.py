from account.models import UserManager


class MainMenu:
    __boat = dict(name="Boats", url="", icon="list", selected=True)
    __order = dict(name="Booking", url="mtnc", icon="usd")
    __policy = dict(name="Cancel Policy", url="mtnc", icon="usd")
    __company = dict(name="Companies", url="mtnc", icon="usd")

    @classmethod
    def get(cls, user):
        if user.is_owner:
            return cls.__owner()
        if user.is_bok:
            return cls.__bok()
        return []

    @classmethod
    def __owner(cls):
        return [cls.__boat, cls.__order]

    @classmethod
    def __bok(cls):
        return [cls.__boat, cls.__order, cls.__policy, cls.__company]
