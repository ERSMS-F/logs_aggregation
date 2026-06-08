import json
import time
import random
from faker import Faker

if __name__ == "__main__":
    fake = Faker()
    while True:
        log = {
            "message": fake.sentence(),
            "level": random.choice([1, 20, 40, 60, 80, 100]),
            "service": "fakelogs"
        }
        print(json.dumps(log, indent=None), flush=True)
        time.sleep(0.5)