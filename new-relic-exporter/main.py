from quixstreams import Application
import os
import requests
from dotenv import load_dotenv

load_dotenv();

metrics_endpoint= os.environ["NEWRELIC_ENDPOINT"]
metrics_key= os.environ["NEWRELIC_KEY"]

def main():
      
      app = Application.Quix(
            consumer_group='consumer',
            auto_offset_reset="earliest",
            auto_create_topics=True,  # Quix app has an option to auto create topics
        )
      
      with app.get_consumer() as consumer:
            consumer.subscribe([os.environ["input"]])
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is not None:     
                  
                    url = metrics_endpoint
                    headers = {
                        "Content-Type": "application/json",
                        "Api-Key": metrics_key
                    }
                    
                    response = requests.post(url, headers=headers, data=msg.value(), verify=False)
                    
                    print("Response code:", response.status_code)
                    print("Response content:", response.content)

if __name__ == "__main__":
    main()