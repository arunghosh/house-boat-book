from util.mail import MailSender


BASE = "emails/customer/"
CONFIRM_MAIL = BASE + "order_confirm"
CANCEL_MAIL = BASE + "order_cancel"


class MailNotification():

    def __init__(self, order):
        self.order = order
        self.mail = MailSender(
            order.customer.user,
            {'order': order}
        )

    def send_order_cancel(self):
        self.mail.template_url = CANCEL_MAIL
        self.mail.title = 'Cancel Ticket'
        self.mail.send_async(self.__log_cancel_mail())

    def send_order_confirm(self):
        self.mail.template_url = CONFIRM_MAIL
        self.mail.title = 'Ticket'
        self.mail.send_async(self.__log_confirm_mail())

    def __log_confirm_mail(self):
        # TODO
        pass

    def __log_cancel_mail(self):
        # TODO
        pass
