*** Settings ***
Documentation     Provisions new postgres rds db and runs db setup scripts.
Library    OperatingSystem
Library    ../library/RDSLibrary.py
Library    ../library/ImportBooks.py

*** Variables ***
${instance_name}  hello2

*** Test Cases ***
Provision New Postgres RDS Instance
    [Documentation]    Create new RDS instance w
    ${output}=   RDSLibrary.create  ${instance_name}
    Log To Console    "Created ${output}"

    ${output}=   RDSLibrary.wait for instance to be running  ${instance_name}
    Log To Console    "${instance_name}  ${output}"

    ${output}=   RDSLibrary.get public host address  ${instance_name}
    Log To Console    "List of DBs ${output}"

    ${postgres_url}=  RDSLibrary.build postgres url  ${instance_name}
    set global variable  ${postgres_url}
    Log To Console    "postgres URL ${postgres_url}"

Setup Books Request Table
    ${output}=  ImportBooks.drop tables   ${postgres_url}
    Append To File  scripts/start_flask    ${output}

    ${output}=  ImportBooks.create tables   ${postgres_url}
    Log To Console    ${output}

     ${output}=  ImportBooks.load books   ${postgres_url}
    Log To Console    ${output}

Add DB Url to start_flask script
    Remove File     scripts/start_flask.sh
    Append To File  scripts/start_flask.sh  export DATABASE_URL=${postgres_url}\n
    Append To File  scripts/start_flask.sh  export FLASK_ENV=development\n
    Append To File  scripts/start_flask.sh  export FLASK_APP=application.py\n
    Append To File  scripts/start_flask.sh  export GOOD_READS_KEY="47rkiBSFHxWjMgqGv6pd3A"\n
    Append To File  scripts/start_flask.sh  cd FlaskBookReview\n
    Append To File  scripts/start_flask.sh  flask run --host=0.0.0.0\n



*** Keywords ***


