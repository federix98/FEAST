from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import TopicPartition

from Connector import Connector

class KafkaConnector(Connector):
    
    '''
    Constructor of the KafkaConnector class
    Each instance of this class was thinked as a single specific publisher of a component.
    So for each instance we have to specify the "topic" and the "key" parameters to publish
    messages.  
    
    Parameters
    ----------
    HOST : str    
        address of the bootstrap server
    PORT : str    
        port of the bootstrap server
    topic : str
       topic where messages will be published (Producer) / read (Consumer)
    key : str     
        key of the message values that will be published (Producer)
    tp: "Producer" | "Consumer"      
        type of the KafkaConnector: (Producer | Consumer)
    '''
    def __init__(self, HOST, PORT, topic, key, tp="Producer"):
        super().__init__()
        self.HOST = HOST
        self.PORT = PORT
        self.tp = tp
        self.topic = topic
        self.key = key
        print("Kafka Connector", self.tp, "created")

    def connect(self):
        if self.tp == "Producer":
            try:
                self.producer = KafkaProducer(bootstrap_servers=[str(self.HOST) + ':' + str(self.PORT)], api_version=(0, 10))
                print("Producer connected to bootstrap server")
            except Exception as ex:
                print('Exception while connecting Kafka')
                print(str(ex))
        elif self.tp == "Consumer":
            self.consumer = KafkaConsumer(auto_offset_reset='latest',
                                  bootstrap_servers=[str(self.HOST) + ':' + str(self.PORT)], api_version=(0, 10), consumer_timeout_ms=1000)
            self.consumer.subscribe(topics=[self.topic])

    def send(self, message):
        try:
            key_bytes = bytearray(self.key,'utf8')
            value_bytes = bytearray(message,'utf8')
            self.producer.send(self.topic, key=key_bytes, value=value_bytes)
            self.producer.flush()
            print('Message published successfully.')
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))

    def receive(self):
        return [str(message.value, 'utf-8') for message in self.consumer if message.topic == self.topic] 
