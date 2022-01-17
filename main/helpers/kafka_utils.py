from confluent_kafka import Producer
from datetime import datetime
import logging
import sys, json, os

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TOPIC = os.environ.get('TOPIC')
KAFKA_SSL_PASSWORD = os.environ.get('KAFKA_SSL_PASSWORD')
KEY_PEM_FILE = "key.pem"
CERT_PEM_FILE = "cert.pem"


def delivery_report(err, msg):
    if err:
        logging.error('Message delivery failed: {}'.format(err))
    else:
        logging.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def send_message(message):
    if not all([KAFKA_BROKER_URL, KAFKA_SSL_PASSWORD, TOPIC]):
        logging.info('The required environment variables were not set')
        raise sys.exit('The required environment variables were not set')
    else:    
        conf = {
            'bootstrap.servers': KAFKA_BROKER_URL,
            'security.protocol':'SSL',
            'ssl.ca.location':'/etc/ssl/certs/ca-certificates.crt',
            'ssl.certificate.location': f'./{CERT_PEM_FILE}',
            'ssl.key.location': f'./{KEY_PEM_FILE}',
            'ssl.key.password': KAFKA_SSL_PASSWORD
        }

        producer = Producer(conf)
        value=json.dumps({
            "infoMessage": message,
            "date": datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
            "refreshRecommend": True
        })
        producer.produce(TOPIC, value=value, callback=delivery_report)
        producer.poll(1)

if __name__ == "__main__":
    send_message({'optimization_id': '123'})
