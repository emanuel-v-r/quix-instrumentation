from quixstreams import Application
import os
import requests
from dotenv import load_dotenv
import json
import logging
import sys

load_dotenv()

# Logging Configuration
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

metrics_endpoint = os.environ.get("NEWRELIC_ENDPOINT")
metrics_key = os.environ.get("NEWRELIC_KEY")

def main():
    try:
        app = Application.Quix(
            consumer_group='consumer',
            auto_offset_reset="earliest",
            auto_create_topics=True,
        )

        with app.get_consumer() as consumer:
            input_topic = app.topic(os.environ["input"])
            consumer.subscribe([input_topic])
            logger.info("Waiting for messages...")
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is not None:
                    try:
                        payload = msg.value().decode('utf-8')
                        logger.info("Received message: %s", payload)

                        if metrics_endpoint and metrics_key:
                            url = metrics_endpoint
                            headers = {
                                "Content-Type": "application/json",
                                "Api-Key": metrics_key
                            }

                            response = requests.post(url, headers=headers, data=payload)
                            logger.info("Response code: %s", response.status_code)
                            logger.info("Response content: %s", response.content)
                        else:
                            logger.error("Metrics endpoint or key not found in environment variables.")
                    except Exception as e:
                        logger.error("Error processing message: %s", str(e))
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Exiting...")
    except Exception as e:
        logger.error("An error occurred: %s", str(e))

if __name__ == "__main__":
    main()
