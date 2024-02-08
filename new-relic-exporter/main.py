import quixstreams as qx
import os

# Quix injects credentials automatically to the client.
# Alternatively, you can always pass an SDK token manually as an argument.
client = qx.QuixStreamingClient()

# Use Input / Output topics to stream data in or out of your service
consumer_topic = client.get_topic_consumer(os.environ["input"])


import requests
import json
import time

consumer = client.get_topic_consumer(consumer_topic)



consumer.on_stream_received = 


url = "https://metric-api.newrelic.com/metric/v1"
headers = {
    "Content-Type": "application/json",
    "Api-Key": "NRAK-IA821CAJ8G6LAFVBTHCBDQZ3XH1"
}

data = [{
    "metrics": [{
        "name": "memory.heap",
        "type": "gauge",
        "value": 2.3,
        "timestamp": int(time.time()),  # Assuming you want current Unix timestamp
        "attributes": {"host.name": "dev.server.com"}
    }]
}]

response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

print("Response code:", response.status_code)
print("Response content:", response.content)
# for more samples, please see samples or docs
