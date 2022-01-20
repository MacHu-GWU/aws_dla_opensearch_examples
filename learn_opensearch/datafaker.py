# -*- coding: utf-8 -*-

import random
from datetime import datetime, date, timedelta
from rich import print
from faker import Faker

fake = Faker()

account_creation_start_date = date(2000, 1, 1)

acc_types = ["checking", "saving"]


def gen_doc():
    creation_date = account_creation_start_date + timedelta(days=random.randint(0, 365 * 20))
    return {
        "account_id": random.randint(1000000000, 9999999999),
        "account_balance": random.randint(500, 200000) // 100 * 100,
        "account_creation_date": creation_date.strftime("%Y%m%d"),
        "account_type": random.choice(acc_types),
        "owner_lastname": fake.last_name(),
        "owner_firstname": fake.first_name(),
        "owner_ssn": fake.ssn(),
        "owner_billing_address": fake.address().replace("\n", ", "),
        "owner_email": fake.email(),
        "owner_preference_vector": [
            random.randint(1, 100)
            for _ in range(10)
        ]
    }


def gen_data(n):
    return [
        gen_doc()
        for _ in range(n)
    ]


if __name__ == "__main__":
    print(gen_doc())
    print(gen_data(10))
