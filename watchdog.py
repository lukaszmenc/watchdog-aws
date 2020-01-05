#! /usr/bin/env  python3

import time
import datetime
import os
import daemon
import sys
import logging

from utils.aws import AWS
from utils.config import LoadConfiguration


logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler("watchdog.log")
logger.addHandler(fh)

aws = AWS()


def watchdog_daemon(config, get_config):

    start_time = time.time()

    while True:
        for service in config["services"]:
            service_status = os.system(f"service {service} status")

            if service_status != 0:

                logger.warning(f"{datetime.datetime.now()}: Service {service} down!")
                aws.sns.publish(
                    TopicArn=aws.sns_topic_arn, Message=f"Service {service} is down",
                )

                for attempt in range(int(config["num_of_attempts"])):
                    os.system(f"sudo service {service} start")
                    service_status = os.system(f"service {service} status")

                    if service_status == 0:
                        logger.info(f"{datetime.datetime.now()}: Attempt {attempt+1}: service {service} started")
                        aws.sns.publish(
                            TopicArn=aws.sns_topic_arn,
                            Message=f"Service {service} has been started after {attempt+1} attempts",
                        )
                        break

                    logger.warning(
                        f"{datetime.datetime.now()}: Attempt {attempt+1}: service {service} not started"
                    )

                    if attempt == config["num_of_attempts"] - 1:
                        aws.sns.publish(
                            TopicArn=aws.sns_topic_arn,
                            Message=f"Service {service} can't be started after {attempt + 1} attempts",
                        )

                    time.sleep(int(config["num_of_sec_wait"]))

        timer = time.time() - start_time

        if int(timer) >= 900:
            config = get_config.load()
            start_time = time.time()

        time.sleep(int(config["num_of_sec_check"]))


def watchdog(id_value):
    get_config = LoadConfiguration(aws=aws, _id=id_value, table_name=aws.table_name)
    config = get_config.load()
    with daemon.DaemonContext(files_preserve=[fh.stream],):
        watchdog_daemon(config, get_config)


if __name__ == "__main__":
    try:
        watchdog(sys.argv[1])
    except IndexError:
        print('Configuration ID missing. \nTry:\n$ ./watchdog.py "configuration_id"')
    except KeyError:
        print("Configuration ID does not exist")
    except Exception as ex:
        print(f"Unknown issue: {ex}")
