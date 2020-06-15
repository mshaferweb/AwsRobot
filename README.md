# Robot Framework Demo

### Demonstrates RobotFramework, Python Library and AWS coordination

- TS (a) Create Postgresql RDS instance 
  - python boto3 RDS lib
- TS (b) Deploy Flask application
  - python3 boto3 EC2 lib
  - RobotFramework SSHLibrary and SCPLibrary
- TS (c) Create Snapshot
  - python boto3 RDS lib
- TS (d) Execute book review UI test
  - RobotFramework SeleniumLibrary RequestsLibrary
- TS (e) UI test Apple.com 
  - Browserstack configurable with ${REMOTE_URL} in resource/CommonWeb.robot
- TS (f)  Restore RDS Snapshot
  - python boto3 RDS lib
- TS (g)  Cleanup AWS resources


Create AWS config and credentials file in ~/.aws
> config
```
[default]
region = us-east-2
```
> credentials
```[default]
aws_access_key_id = <>
aws_secret_access_key = <>
```

Install Python Requirements:
> sudo apt-get install python3-pip
> sudo pip3 install -r requirements.txt

Run Suite:

> robot -d results -L debug --variable instance_name:robotdemo TestSuite/ 

