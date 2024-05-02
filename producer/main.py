import os
from faker import Faker
import json
import random
from kafka import KafkaProducer
from datetime import datetime
import time


fake = Faker()

# Kafka 설정
producer = KafkaProducer(
    bootstrap_servers=[os.getenv("BOOTSTRAP_SERVER")],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

# 주식 종목 코드 목록
stock_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "FB", "TSLA"]
TOPIC_NAME = os.getenv("TOPIC_NAME")
PRODUCE_SPEED = os.getenv("PRODUCE_SPEED")


def generate_trade():
    return {
        "symbol": random.choice(stock_symbols),
        "price": round(random.uniform(100, 1000), 2),
        "quantity": random.randint(1, 100),
        "timestamp": datetime.now().isoformat(),
    }


# 초당 데이터 생성 루프
if __name__ == "__main__":
    while True:
        start_time = time.time()
        for _ in range(PRODUCE_SPEED):  # 초당 천 개의 데이터를 생성하고 전송
            trade = generate_trade()
            producer.send(TOPIC_NAME, value=trade)
            # 실시간으로 생성된 데이터 출력 (출력을 원치 않는다면 이 줄을 주석 처리)
        end_time = time.time()
        # 처리 시간 계산 후, 1초 안에 작업을 완료했다면, 나머지 시간 동안 대기
        elapsed_time = end_time - start_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)
