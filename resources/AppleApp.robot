*** Settings ***
Resource  ./PO/Home.robot
Resource  ./PO/TopNav.robot
Resource  ./PO/Iphone.robot

*** Variables ***


*** Keywords ***
Go to Home Page
    Home.Navigate_To
    Home.Verify_Page_Loaded

Go to Iphone Page
    TopNav.Select_Iphone_Page
    Iphone.Verify_Page_Loaded

Select Iphone 11
    Iphone.Select_Iphone_11

Configure Iphone 11
    #Iphone.Configure_No_Trade_in
    Iphone.Configure_Color
    Iphone.Configure_Capacity
    Iphone.Configure_Carrier
    Iphone.Configure_No_Trade_in_Bottom Page
    Iphone.Configure_Coverage
    Iphone.Add_To_Bag

Validate Iphone Page
    Iphone.Verify_Page_Loaded