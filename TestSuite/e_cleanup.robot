
*** Settings ***
Library    ../library/RDSLibrary.py
Library    ../library/EC2Library.py

*** Variables ***
${instance_name}  hello5

*** Test Cases ***
Stop All RDS Instances
    ${instances}=   RDSLibrary.list
    Log To Console    "Stopping DB running ${instances}"

    FOR    ${i}  IN  @{instances}
        RDSLibrary.delete  ${i}
        Log To Console  Deleted DB ${i}
    END

Stop EC2 Instances
    [Documentation]   Stopping ec2 find instances
    EC2Library.terminate_all_instances




