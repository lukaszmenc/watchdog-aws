# Watchdog
Watchdog is checking if required Linux services are currently running. If a service is found to be down, the watchdog will try to put it up again. You will be notified of errors found and actions taken by AWS SNS. All evens will also be saved into log file.

Watched services and configurations may be prepared in JSON file. Configuration is read from AWS DynamoDB. Example of JSON file structure may be found at the bottom of Readme file.
Settings:
- "id" - string, unique configuration id
- "ListOfServices" - list of strings, names of services to be checked by watchdog
- "NumOfSecCheck" - int, time in secs between subsequent checks of the service operation
- "NumOfSecWait" - int, time in secs between subsequent tries of putting service up
- "NumOfAttempts" - int, number of attempts made to put the service up

## Installation
1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.
    ```bash
    pip3 install -r requirements.txt
    ``` 
2. Set up ```credentials``` file (default location ```~/.aws```)
    ```
    [default]
    aws_access_key_id = YOUR_ACCESS_KEY_ID
    aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
    ```
3. Set up default region in ```config``` file (default location ```~/.aws```)
    ```
    [default]
    region = YOUR_AWS_REGION_NAME
    ```
4. Set up your AWS services information in ```utils/aws.py``` file:
    ```
    self.table_name = "YOUR_DYNAMODB_TABLE_NAME"
    self.sns_topic_arn = "YOUR_SNS_TOPIC_ARN"
    ```
## Usage


### Run watchdog
```bash
./watchdog.py 'CONFIGURATION_ID'
```

### Run load_data to upload data to dynamodb
```bash
./load_data.py 'JSON_FILE_PATH'
```

###Database/JSON structure 
```
{
    "id": "ConfigurationId",
    "ListOfServices":["service1", "service2"],
    "NumOfSecCheck": int,
    "NumOfSecWait": int,
    "NumOfAttempts": int
},
```

