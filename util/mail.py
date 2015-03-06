from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import threading


class MailSender(threading.Thread):

    def __init__(self, user, context_json=None):
        threading.Thread.__init__(self)
        self.subject_base = "Boats of Kerala - "
        self.title = self.subject_base
        self.context_json = {} if not context_json else context_json
        self.template_url = None
        self.user = user
        self.callback = None

    def send(self):
        self.context_json['user_name'] = self.user.name
        d = Context(self.context_json)
        text_content = get_template(self.template_url + '.txt').render(d)
        html_content = get_template(self.template_url + '.html').render(d)
        msg = EmailMultiAlternatives(self.subject_base + self.title,
                                     text_content,
                                     "bok@gmail.com",
                                     [self.user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def send_async(self, callback=None):
        self.callback = callback
        self.start()

    def run(self):
        self.send()
        if self.callback:
            self.callback()