import os
import json
import asyncio
import aioboto3
from aiokafka import AIOKafkaConsumer


async def save_to_s3(data):
    async with aioboto3.resource("s3") as s3:
        bucket = await s3.Bucket(os.getenv("BUCKET_NAME"))
        key = f'trades/{data["timestamp"]}_{data["symbol"]}.json'
        await bucket.put_object(Key=key, Body=json.dumps(data))


async def consume():
    consumer = AIOKafkaConsumer(
        os.getenv("TOPIC_NAME"),
        bootstrap_servers=os.getenv("BOOTSTRAP_SERVER"),
        auto_offset_reset="earliest",
        group_id=os.getenv("GROUP_ID"),
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    # 시작 컨슈머
    await consumer.start()
    try:
        async for message in consumer:
            trade = message.value
            if trade["price"] > 700:
                await save_to_s3(trade)
    finally:
        # 종료할 때 컨슈머 정리
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
