*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${VERIFY_MAIN}  id=ac-globalnav

*** Keywords ***
Navigate to
    Go To   ${URL}
    # Maximize Browser Window


Verify_Page_Loaded
    Wait until page contains element  ${VERIFY_MAIN}