*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${URL}  http://apple.com
# ${BROWSER}   Headless Chrome
${BROWSER}   Chrome
#${REMOTE_URL} =  http://michaelshafer1:Fk2LNJaFwPuWYfzR3yxR@hub.browserstack.com:80/wd/hub
${REMOTE_URL} =  http://172.18.0.1:4444/wd/hub
# ${BROWSER}   Firefox
*** Keywords ***
Begin Web Test
   # --no-sandbox", "--disable-dev-shm-usage"
#    ${list} =     Create List    --no-sandbox    --disable-dev-shm-usage   --remote-debugging-port=9222
#    ${args} =     Create Dictionary    args=${list}
#    ${desired caps} =     Create Dictionary   chromeOptions=${args}
#    Open Browser    about:blank   browser=${BROWSER}    desired_capabilities=${desired caps}
#    Open Browser   ${URL}     ${BROWSER}   remote_url=${REMOTE_URL}
    Open Browser   ${URL}     ${BROWSER}
    Set Selenium Implicit Wait  20
    #maximize browser window

End Web Test
    #log  hello
    Close all browsers


