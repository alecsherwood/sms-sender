import unittest
from message import Message


class MessageTest(unittest.TestCase):
    def test_get_message_recipient(self):
        my_message = Message("6178675309", "This is a test message.")
        self.assertEqual(my_message.get_recipient(), "6178675309")

    def test_get_message_body(self):
        my_message = Message("6178675309", "This is a test message.")
        self.assertEqual(my_message.get_message(), "This is a test message.")


if __name__ == "__main__":
    unittest.main()
