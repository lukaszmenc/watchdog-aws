#! /usr/bin/env  python3

import json
import decimal
import sys

from json import JSONDecodeError
from utils.aws import AWS


aws = AWS()


def load_data(json_file_path):
    table = aws.dynamodb.Table(aws.table_name)

    with open(json_file_path) as json_file:
        services = json.load(json_file, parse_float=decimal.Decimal)

        for service in services:
            _id = service["id"]
            list_of_services = service["ListOfServices"]
            num_of_sec_check = int(service["NumOfSecCheck"])
            num_of_sec_wait = int(service["NumOfSecWait"])
            num_of_attempts = int(service["NumOfAttempts"])

            table.put_item(
                Item={
                    "id": _id,
                    "ListOfServices": list_of_services,
                    "NumOfSecCheck": num_of_sec_check,
                    "NumOfSecWait": num_of_sec_wait,
                    "NumOfAttempts": num_of_attempts,
                }
            )


if __name__ == "__main__":
    try:
        load_data(sys.argv[1])
    except IndexError:
        print('File path parameter missing. \nTry:\n$ ./load_data.py "file_path"')
    except FileNotFoundError:
        print("Requested file does not exist. Make sure you provide the file extension")
    except JSONDecodeError:
        print("It looks like your file is not JSON format. Make sure you provide the path to the JSON file")
