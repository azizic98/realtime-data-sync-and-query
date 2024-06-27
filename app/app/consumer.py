from threading import Thread
import time
from app import (connections, 
                utils, 
                event_handler)

stream_name_outlets = 'cdc_demo.test.tbl_outlets'
stream_name_reporters = 'cdc_demo.test.tbl_reporters'

def consume_stream(stream_name):
    """
    Consumes and deletes messages from a Redis Stream.

    Args:
        stream_name (str): Name of the Redis Stream.
    """

    last_message_id = "-"  # Start from the most recent message
    while True:
        messages = connections.redis_client.xrange(stream_name, min=last_message_id, count=100)

        if not messages:
            print("No new messages. Waiting...")
            time.sleep(1)  # Adjust wait time as needed
            continue

        for message_id, message in messages:
            payload_dict = utils.extract_payload(message)
            event_handler.handle_event(payload_dict)

            # Delete the message after processing
            connections.redis_client.xdel(stream_name, message_id)
            print(f"Message Processed: {message_id}")

        # Update last_message_id to process subsequent messages
        last_message_id = message_id

def start_consumers():
    # Start consumers in separate threads
    outlets_consumer = Thread(target=consume_stream, args=(stream_name_outlets,))
    reporters_consumer = Thread(target=consume_stream, args=(stream_name_reporters,))

    outlets_consumer.start()
    reporters_consumer.start()

    outlets_consumer.join()
    reporters_consumer.join()
