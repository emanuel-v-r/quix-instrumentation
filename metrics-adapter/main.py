
import os
import quixstreams as qx
from dotenv import load_dotenv
from app_factory import get_app
from quixstreams.models.serializers.quix import QuixDeserializer, QuixTimeseriesSerializer
import time


load_dotenv();

USE_LOCAL_KAFKA=os.getenv("use_local_kafka", False)

app = get_app(use_local_kafka=USE_LOCAL_KAFKA)

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(topic=input_topic)

def to_metrics(row):    
    
    timestamp = int(time.time())
    
    metrics = [{      
            "metrics":[{
                "name": "trades.volume",
                'type': "count",
                'value': row['v'],
                'timestamp': timestamp,
                "interval.ms": 1000,
                "attributes": {
                    "symbol": row['s']
                }
            },
            {
                "name": "trades.price",
                'type' : "gauge",
                'value' : row['p'],
                'timestamp' : timestamp,
                "attributes": {
                    "symbol": row['s'],
                    'source.timestamp' : row['t'],
                }
            } ]        
            }]
    return metrics

sdf= sdf.apply(to_metrics,  expand=False)

sdf = sdf.update(lambda value: print('Producing a message:', value))

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)