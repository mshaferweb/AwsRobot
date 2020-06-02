*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${VERIFY_MAIN}  css=#body > main > section:nth-child(2) > div:nth-child(1) > div > div > a

*** Keywords ***
Select Iphone 11
    Click Link   	/iphone-11/
    Click Link   	/us/shop/goto/buy_iphone/iphone_11

Configure No Trade In
    Wait until page contains element   css=#noTradeIn
    Click Element   	css=#noTradeIn

Configure No Trade In Bottom Page
    Wait until page contains element   xpath:(.//label[contains(., 'No')])[1]
    Click Element   	xpath:(.//label[contains(., 'No')])[1]


Configure Color
    Set Selenium Speed    0.25
    Wait Until Element Is Enabled    css=#Item1 > div > fieldset > div.form-selector.form-selector-rowwithgutters.as-dimension-choices.row > div:nth-child(5) > div > div
    Click Element  Item1purple_label

Configure Capacity
    Wait Until Element Is Enabled    css=#Item2 > div > fieldset > div > div:nth-child(3) > div
    Click Element    css=#Item2 > div > fieldset > div > div:nth-child(3) > div

Configure Carrier
    Wait Until Element Is Enabled   css=#Item40_label > span > h2
    Click Element    css=#Item40_label > span > h2

Configure Coverage
    Wait Until Element Is Enabled   applecareplus_55_noapplecare
    Click Button  applecareplus_55_noapplecare

Add To Bag
    Wait Until Element Is Enabled   css=#primary > summary-builder > div.as-purchaseinfo > div.as-purchaseinfo-details.as-purchaseinfo-background > div > div > div.grouped-button-left > div > div > form > div > span > button
    Click Button    css=#primary > summary-builder > div.as-purchaseinfo > div.as-purchaseinfo-details.as-purchaseinfo-background > div > div > div.grouped-button-left > div > div > form > div > span > button

Verify_Page_Loaded
    Wait until page contains element  ${VERIFY_MAIN}

