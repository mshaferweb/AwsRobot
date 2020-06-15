*** Settings ***
Documentation   Robot Framework Demo with Browserstack
Resource  ../resources/AppleApp.robot
Resource  ../resources/CommonWeb.robot

Test Setup  Begin Web Test
Test Teardown  End Web Test

# robot -d results tests/apple.robot

*** Variables ***

*** Test Cases ***
Add Iphone 11 to cart
    [Documentation]     This is test adds Iphone 11 to shopping cart
    Log  ${BROWSER}
    AppleApp.Go to Home Page
    AppleApp.Go to Iphone Page
    AppleApp.Select Iphone 11
    AppleApp.Configure Iphone 11


