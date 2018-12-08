from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'greetings'


if __name__ == '__main__':
    while True:
        msg = input('> ')

        future = producer.send(topic, msg.encode('ascii'))
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break
