*** Settings ***
Documentation     Renames db and then Restores snapshot
Library    OperatingSystem
Library    ../library/RDSLibrary.py
Library    ../library/ImportBooks.py

*** Variables ***
${instance_name}  robotdemo1

*** Test Cases ***
Restore Snapshot
    [Documentation]    Rename instance and then restore snapshot.
    ${output}=   RDSLibrary.modify instance name  ${instance_name}  ${instance_name}-deleteme
    Log To Console    "Created ${output}"

    ${output}=   RDSLibrary.wait for instance to be running  ${instance_name}-deleteme
    Log To Console    "${instance_name}  ${output}"

    ${output}=   RDSLibrary.restore snapshot  ${instance_name}  ${snapshot_name}
    Log To Console    "Restored snapshot ${snapshot_name} to ${instance_name}
    Log To Console    ${output}"

    ${output}=   RDSLibrary.wait for instance to be running  ${instance_name}
    Log To Console    "${instance_name}  ${output}"

*** Keywords ***


