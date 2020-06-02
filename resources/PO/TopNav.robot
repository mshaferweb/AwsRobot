*** Settings ***
Library  SeleniumLibrary


*** Variables ***
${IPHONE_LINK}  css=a[class="ac-gn-link ac-gn-link-iphone"]
*** Keywords ***
Select Iphone Page
    #click link  Team
    click element  ${IPHONE_LINK}