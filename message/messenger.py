from abc import ABC, abstractmethod

class Messenger(ABC):

    @abstractmethod
    def send(self, sender, recipient, subject, message_text, message_html):
        pass

