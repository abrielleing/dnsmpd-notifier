from message.messenger import Messenger

class FakeMessenger(Messenger):
    
    def __init__(self):
        self.sender = None
        self.recipient = None
        self.subject = None
        self.message_text = None
        self.message_html = None

    def send(self, sender, recipient, subject, message_text, message_html):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.message_text = message_text
        self.message_html = message_html
