## Robot Framework Demo
#### Create Postgresql RDS instance using boto3 python lib
#### Run SQL setup for RDS instance using sql alchemy python lib
#### Spin up EC2 instance using boto3 lib
#### Configure Flask application using Robot SSHLibrary and SCPLibrary
#### Run Robot UI test for book review flask application
#### Run UI from Browserstack add Iphone11 to cart on Apple

Install Requirements:

`sudo pip3 install -r requirements.txt`

Run Suite

`robot -d results -L debug --variable instance_name:robotdemo TestSuite/ 
`
