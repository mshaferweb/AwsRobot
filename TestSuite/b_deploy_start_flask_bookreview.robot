*** Settings ***
Library    SSHLibrary
Library    SCPLibrary
Library    Process
Library    Collections
Library    ../library/EC2Library.py
Library    ../library/pyrequests.py

Suite Setup    Open Connection And Log In
Suite Teardown    Close All Connections and Stop Ec2

*** Variables ***
${USERNAME}    ubuntu
${AWS_PEM_PATH}  /home/ubuntu/.ssh/aws.pem
${instance_id}    i-0f1d884cd26a36745

*** Test Cases ***
CLone Flask Book Review Repo
    [Documentation]  Clone Book Review Repo on EC2 Flask host
    ${output}=   Execute Command  echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
    Log To Console    "Git output ${output}"
    ${output}=   Execute Command  git clone https://github.com/mshaferweb/FlaskBookReview.git
    Log To Console    "Git output ${output}"

Install Python Requirement
    [Documentation]  Install python requirements on EC2 Flask host
    Log To console  "Installing python requirements"

    ${output}=   Execute Command  apt update  sudo=True
    Log To Console    "Excuted apt update

    ${output}=   Execute Command  apt install -y python3-pip  sudo=True
    Log To Console    "Excuted apt install -y python3-pip"

    ${output}=   Execute Command  pip3 install -r FlaskBookReview/requirements.txt  sudo=True
    Log To Console    "Executed Command  pip3 install"

Start Flask Server
    [Documentation]  Copy Start up script and start flask server
    Copy Flask StartUp Script to EC2
    SSHLibrary.Start Command     nohup ./start_flask.sh > myout.file 2>&1
    Log To Console    "Started Flask"

Wait for Connection to be Live

   pyrequests.httprequest_check_200  http://${HOST}:5000


*** Keywords ***

Open Connection And Log In
    [Documentation]  Spin up new EC2 instance
    ${instance_id}=  EC2Library.create instance
    EC2Library.wait for instance to be running  ${instance_id}
    ${HOST}=  EC2Library.find running instance public ip  ${instance_id}
    set global variable  ${HOST}
    Log To Console    "Instance Id ${instance_id} :: HOST ${HOST}"
    Copy Key to Known Hosts
    SSHLibrary.Open Connection    ${HOST}
    # Sleep required for SSH to be ready
    Builtin.sleep  20
    SSHLibrary.Login With Public Key    ${USERNAME}    ${AWS_PEM_PATH}    password=    allow_agent=False    look_for_keys=False    delay=10 seconds    proxy_cmd=

Copy Key to Known Hosts
    ${result}=    Run Process    ssh-keyscan -H ${HOST} > known_hosts    shell=True    cwd=%{HOME}/.ssh
    Log To Console    "Copy key: ${result}"

Copy Flask StartUp Script to EC2
    SCPLibrary.Open Connection   ${HOST}  port=22  username=${USERNAME}    password=None  key_filename=${AWS_PEM_PATH}
    SCPLibrary.Put File          scripts/start_flask.sh       /home/ubuntu/
    SCPLibrary.Close Connection
    Execute Command  chmod 777 start_flask.sh

Close All Connections and Stop Ec2
    Log To Console    "Start Flask at ${HOST}:5000"
    Log To Console    "Stopped connections"
    #Close All Connections