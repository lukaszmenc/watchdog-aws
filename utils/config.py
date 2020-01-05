class LoadConfiguration:
    def __init__(self, aws, _id, table_name):
        self.id = _id
        self.table = aws.dynamodb.Table(table_name)

    def load(self):
        service = self.table.get_item(Key={"id": self.id})

        services = service["Item"]["ListOfServices"]
        num_of_sec_check = service["Item"]["NumOfSecCheck"]
        num_of_sec_wait = service["Item"]["NumOfSecWait"]
        num_of_attempts = service["Item"]["NumOfAttempts"]

        return {
            "services": services,
            "num_of_sec_check": num_of_sec_check,
            "num_of_sec_wait": num_of_sec_wait,
            "num_of_attempts": num_of_attempts,
        }
