from quixstreams import Application
import os
import aiohttp
import asyncio
import json
import logging
import sys
from dotenv import load_dotenv
import uuid

load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

metrics_endpoint = os.environ.get("NEWRELIC_ENDPOINT")
metrics_key = os.environ.get("NEWRELIC_KEY")

async def process_message(payload):
    async with aiohttp.ClientSession() as session:
        try:
            if metrics_endpoint and metrics_key:
                url = metrics_endpoint
                headers = {
                    "Content-Type": "application/json",
                    "Api-Key": metrics_key
                }
                async with session.post(url, headers=headers, data=payload) as response:
                    logger.info("Response code: %s", response.status)
                    logger.info("Response content: %s", await response.text())
            else:
                logger.error("Metrics endpoint or key not found in environment variables.")
        except Exception as e:
            logger.error("Error processing message: %s", str(e))

async def consume_messages(app):
    consumer = app.get_consumer()
    input_topic = app.topic(os.environ["input"]).name
    consumer.subscribe([input_topic])
    logger.info("Waiting for messages...")
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is not None:
            try:
                payload = msg.value().decode('utf-8')
                logger.info("Received message: %s", payload)
                await process_message(payload)
            except Exception as e:
                logger.error("Error processing message: %s", str(e))

async def main():
    try:
        app = Application.Quix(
            consumer_group=str(uuid.uuid4()),
            auto_offset_reset="latest",
            auto_create_topics=True,
        )
        await consume_messages(app)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Exiting...")
    except Exception as e:
        logger.error("An error occurred: %s", str(e))

if __name__ == "__main__":
    asyncio.run(main())
