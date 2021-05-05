import unittest
from queue import Queue
import message_processor
from message import Message

# TODO better test coverage
class MessageProcessorTest(unittest.TestCase):
    def test_generate_messge_number_is_correct_length(self):
        generated = message_processor.build_message(1000)
        self.assertEqual(len(str(generated.get_recipient())), 10)

    def test_generate_message_body_is_correct_length(self):
        generated = message_processor.build_message(1000)
        self.assertEqual(len(str(generated.get_message())), 1000)

    def test_push_messages_populates_a_queue(self):
        test_queue = Queue()
        message_processor.build_messages(test_queue, 1, 1)
        self.assertEqual(test_queue.empty(), False)

    def test_message_sending(self):
        mock_stats = {
            "messages_sent": 1,
            "messages_failed": 3,
            "avg_send_time": 1.0
        }
        mock_times = [1, 1.0, 1]
        my_message = Message("6178675309", "this is a message")
        test_queue = Queue()
        test_queue.put(my_message)
        message_processor.send_messages(test_queue, mock_stats, mock_times, 0, 0)
        self.assertEqual(test_queue.empty(), True)

if "__name__" == "__main__":
    unittest.main()
