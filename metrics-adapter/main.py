
import os
import quixstreams as qx
from dotenv import load_dotenv
from app_factory import get_app
from quixstreams.models.serializers.quix import QuixDeserializer, QuixTimeseriesSerializer

load_dotenv();

# get the environment variable value or default to False
USE_LOCAL_KAFKA=os.getenv("use_local_kafka", False)

app = get_app(use_local_kafka=USE_LOCAL_KAFKA)

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

# Create a StreamingDataFrame instance
# StreamingDataFrame is a primary interface to define the message processing pipeline
sdf = app.dataframe(topic=input_topic)

# Print the incoming messages
# sdf = sdf.update(lambda value, ctx: print('Received a message:', value))

sdf['symbol'] = sdf['s']
sdf['timestamp'] = sdf['t']
sdf['price']  = sdf['p']
sdf['volume']  = sdf['v']

sdf = sdf[["symbol", "timestamp", "price", "volume"]]

sdf = sdf.update(lambda value: print('Producing a message:', value))

sdf = sdf.to_topic(output_topic)



if __name__ == "__main__":
    # Run the streaming application 
    app.run(sdf)