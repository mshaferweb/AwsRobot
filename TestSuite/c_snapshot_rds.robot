*** Settings ***
Documentation     Provisions new postgres rds db and runs db setup scripts.
Library    OperatingSystem
Library    ../library/RDSLibrary.py
Library    ../library/ImportBooks.py

*** Variables ***
${instance_name}  robotdemo2
${snapshot_name}  ${instance_name}-snapshot

*** Test Cases ***
Create Snapshot
    [Documentation]    Create db instance Snapshost
    ${output}=   RDSLibrary.create snapshot  ${instance_name}  ${snapshot_name}
    set global variable  ${snapshot_name}
    Log To Console    "Created ${output}"

    ${output}=   RDSLibrary.wait for snapshot to be available  ${snapshot_name}
    set global variable  ${snapshot_name}
    Log To Console    "Created ${output}"





*** Keywords ***


