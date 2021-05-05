from message import Message
import random
import string
import queue
# import threading
from threading import Thread
# import concurrent.futures
from time import sleep
import time
import argparse


# TODO: Improve data locking and flow across threads. Improve 3 way locking
# TODO: Improve thread management.
# TODO: Better error handling. If this were real we would want to fail gracefully.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("number_of_messages", nargs="?", type=int, default=1000, help='The number of messages you would like to generate and send.')
    parser.add_argument("message_length", nargs="?", type=int, default=100, help='The length of each message body you wish to generate')
    parser.add_argument("monitor_interval", nargs="?", type=int,  default=2, help='Frequency in seconds to monitor status. This must be whole integers.')
    parser.add_argument("failure_rate", nargs="?", type=int, default=0, help='Not Yet Implemented')
    parser.add_argument("average_time_to_send", nargs='?', type=int, default=0, help="The desired average send time for message sending.")
    parser.add_argument("number_of_senders", nargs="?", type=int, default=1, help='Number of threads you would like to use to send messages with')
    args = parser.parse_args()

    number_of_messages = args.number_of_messages
    message_length = args.message_length
    number_of_senders = args.number_of_senders
    monitor_interval = args.monitor_interval
    failure_rate = args.failure_rate
    average_time_to_send = args.average_time_to_send
    messages = queue.Queue()
    times = []
    stats = {
        "messages_sent": 0,
        "messages_failed": 0,
        "avg_message_send_time": 0,
    }

    # Start monitoring...
    monitoring = Thread(target=monitor, args=[stats, times, monitor_interval, number_of_messages], daemon=True)
    monitoring.start()

    # TODO convert threads to executors for better visibility and scaling.
    # # Start producing messages...
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future = executor.submit(push_messages, [messages, number_of_messages, message_length])
    #     message_production_done = future.result()

    producer = Thread(target=build_messages, args=[messages, number_of_messages, message_length], daemon=True)
    producer.start()
    sleep(2)

    # Start consuming messages once their production has started...
    sender_threads = []
    for _ in range(0, number_of_senders):
        sleep(1)
        consumer = Thread(target=send_messages, args=[messages, stats, times, failure_rate, average_time_to_send], daemon=True)
        consumer.start()
        sender_threads.append(consumer)

    # Once production of messages has completed, close thread.
    producer.join()

    # # Stop consumer thread once all messages have been sent.
    for thread in sender_threads:
        thread.join()

    # Close monitoring thread when Producer and Consumer threads have completed work.
    monitoring.join()

    print(f"Done - Successfully Sent: {number_of_messages - stats['messages_failed']} messages {number_of_messages} Total")


def build_message(message_length):
    # Iterate through a range of characters to generate random message
    characters = string.ascii_lowercase
    message_text = ''.join(random.choice(characters) for _ in range(message_length))
    # get a random 10 digit number generated
    message_number = random.randint(1000000000, 9999999999)
    generated_message = Message(message_number, message_text)
    return generated_message


def build_messages(messages, number_of_messages, message_length):
    for _ in range(0, number_of_messages):
        generated = build_message(message_length)
        messages.put(generated)


def send_message(message, failure_rate, average_send_time):
    sleep(abs(random.normalvariate(average_send_time, 1)))
    send_result = random.randint(0, 100)
    if send_result >= failure_rate:
        return True
    else:
        return False


def send_messages(messages, stats, times, failure_rate, average_send_time):
    while not messages.empty():
        start = time.time()
        result = send_message(messages.get(), failure_rate, average_send_time)
        end = time.time()
        result_time = end - start
        times.append(result_time)
        if result:
            stats["messages_sent"] = stats["messages_sent"] + 1
        else:
            stats["messages_failed"] = stats["messages_failed"] + 1


def calculate_average_send_time(times):
    if len(times) != 0:
        return round(sum(times) / len(times) + 1, 4)
    else:
        return 0


def monitor(stats,times, monitor_interval, number_of_messages):
    while (stats['messages_sent'] + stats['messages_failed']) < number_of_messages:
        sleep(monitor_interval)
        stats['avg_message_send_time'] = calculate_average_send_time(times)
        print("Status:")
        print("=========================")
        print(f"Messages Sent:     {stats['messages_sent']}")
        print(f"Messages Failed:   {stats['messages_failed']}")
        print(f"Average Send Time: {stats['avg_message_send_time']}\n")


if __name__ == "__main__":
    main()