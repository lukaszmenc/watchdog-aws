import boto3


class AWS:
    def __init__(self):
        session = boto3.session.Session()
        self.dynamodb = session.resource("dynamodb")
        self.sns = session.client("sns")

        self.table_name = "YOUR_DYNAMODB_TABLE_NAME"
        self.sns_topic_arn = "YOUR_SNS_TOPIC_ARN"
