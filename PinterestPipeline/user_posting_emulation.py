import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
from pprint import pprint
import argparse
import yaml

random.seed(100)


def print_keys(d):
    for k in d.keys():
        print(f'`{k}`')
    print()


class AWSDBConnector:
    def __init__(self):
        with open('db_creds_pinterest.yaml') as f:
            creds = yaml.safe_load(f)
        self.HOST = creds['HOST']
        self.USER = creds['USER']
        self.PASSWORD = creds['PASSWORD']
        self.DATABASE = creds['DATABASE']
        self.PORT = creds['PORT']

    def create_db_connector(self):
        engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4'
        )
        return engine


new_connector = AWSDBConnector()


def run_infinite_post_data_loop(num_posts=-1):
    while num_posts > 0:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:
            pin_string = text(f'SELECT * FROM pinterest_data LIMIT {random_row}, 1')
            pin_selected_row = connection.execute(pin_string)

            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f'SELECT * FROM geolocation_data LIMIT {random_row}, 1')
            geo_selected_row = connection.execute(geo_string)

            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f'SELECT * FROM user_data LIMIT {random_row}, 1')
            user_selected_row = connection.execute(user_string)

            for row in user_selected_row:
                user_result = dict(row._mapping)

            # print_keys(pin_result)
            # print_keys(geo_result)
            # print_keys(user_result)

            # pprint(pin_result.keys())
            # pprint(geo_result.keys())
            # pprint(user_result.keys())

            pprint(pin_result)
            pprint(geo_result)
            pprint(user_result)

            num_posts -= 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Retrieve given number of posts')
    parser.add_argument('-n', default=10000, type=int, help='number of posts, default 10000')

    args = parser.parse_args()

    run_infinite_post_data_loop(num_posts=args.n)
    print('Working')
