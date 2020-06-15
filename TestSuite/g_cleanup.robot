
*** Settings ***
Library    ../library/RDSLibrary.py
Library    ../library/EC2Library.py

*** Variables ***

*** Test Cases ***
Stop All RDS Instances
    ${instances}=   RDSLibrary.list
    Log To Console    "Stopping DB running ${instances}"

    FOR    ${i}  IN  @{instances}
        RDSLibrary.delete  ${i}
        Log To Console  Deleted DB ${i}
    END

Delete All RDS Snapshots
    ${snapshots}=   RDSLibrary.list_snapshots
    Log To Console    "Deleting snapshots: ${snapshots}"

    FOR    ${i}  IN  @{snapshots}
        RDSLibrary.delete_snapshot  ${i}
        Log To Console  Deleted DB ${i}
    END

Stop EC2 Instances
    [Documentation]   Stopping ec2 find instances
    EC2Library.terminate_all_instances




