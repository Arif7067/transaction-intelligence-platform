import json
import random
import time
import uuid
from datetime import datetime, timezone

from faker import Faker
from kafka import KafkaProducer

fake = Faker()
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

MERCHANT_CATEGORIES = ["grocery","electronics","travel","restaurant","online_retail"]


def generate_transaction(force_anomaly: bool = False) -> dict:
    amount = round(random.uniform(5, 500), 2)
    if force_anomaly or random.random() < 0.02:  # ~2% synthetic anomalies
        amount = round(random.uniform(2000,10000), 2)

    return {
        "transaction_id": str(uuid.uuid4()),
        "account_id": f"acc_{random.randint(1000,9999)}",
        "amount": amount,
        "currency": "USD",
        "merchant_category": random.choice(MERCHANT_CATEGORIES),
        "country": fake.country_code(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

if __name__ == "__main__":
    print("producing transactions to topic 'transactions' ... Ctrl+C to stop.")
    try:
        while True:
            txn = generate_transaction()
            producer.send("transactions", value=txn)
            print(txn)
            time.sleep(random.uniform(0.1, 0.5))
    except KeyboardInterrupt:
        producer.flush()
        print("Stopped.")
