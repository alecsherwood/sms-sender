Cloud Engineer Coding Test
==============================

The objective is to simulate sending a large number of SMS alerts, like for an emergency alert service. 
The simulation consists of three parts:
   1. A producer that generates a configurable number of messages (default 1000) to random phone number. Each message contains up to 100 random characters.
   2. A sender, who picks up messages from the producer and simulates sending messages by waiting a random period time distributed around a configurable mean. The sender also has a configurable failure rate.
   3. A progress monitor that displays the following and updates it every N seconds (configurable):
        - Number of messages sent so far
        - Number of messages failed so far
        - Average time per message so far
   
One instance each for the  producer and the progress monitor will be started while a variable number of senders can be started with different mean processing time and error rate settings.
You are free in the programming language you choose, but your code should come with reasonable unit testing.
Please submit the code test at least two business days before the interview, so we have time to review it.

## Running The Code:
To run this program execute the following:

Default Settings:

`python message_processor.py`

Help

`python message_processor.py -h`


`python message_processor.py --help`

Override Settings:

`python message_processor.py <number_of_messages> <length_of_message> <monitor_interval> <failure_rate> <average_time_to_send> <number_of_senders>`
