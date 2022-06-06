import logging
import os

from kafka import KafkaProducer
from pyftpdlib.handlers import FTPHandler


class Handler(FTPHandler):
    kafka_topic = None
    kafka_server = None
    s3_requester = None

    def ftp_RETR(self, file):
        if not file:
            self.respond("500 sorry!")
        else:
            super(Handler, self).ftp_RETR(file)

    def on_incomplete_file_received(self, file):
        os.remove(file)
        self.respond("500 please retry to send")

    def on_file_received(self, file):
        self.upload_to_kafka(file)
        os.remove(file)

    def upload_to_kafka(self, file):
        kafka_producer = KafkaProducer(bootstrap_servers=self.kafka_server)
        kafka_producer.send(topic=self.kafka_topic, value=os.path.basename(file).encode('utf-8'))
        logging.info(f'Sending message to kafka')
        kafka_producer.flush()

