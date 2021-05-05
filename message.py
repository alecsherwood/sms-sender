class Message:
    def __init__(self, recipient, message_body):
        self.recipient = recipient
        self.message_body = message_body

    def get_message(self):
        return self.message_body

    def get_recipient(self):
        return self.recipient
