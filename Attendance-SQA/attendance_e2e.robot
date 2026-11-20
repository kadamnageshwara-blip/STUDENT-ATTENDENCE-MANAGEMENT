*** Settings ***
Library           SeleniumLibrary
Suite Setup       Reset Attendance And Open Browser
Suite Teardown    Close Browser

*** Variables ***
${URL}            http://127.0.0.1:5000
${BROWSER}        Chrome

*** Test Cases ***
TC01 Valid Student Attendance Marking E2E
    [Documentation]    Automatically submits valid student ID 101 and checks count = 1.
    Submit Student Attendance    101
    Wait Until Page Contains    Success: Attendance marked    timeout=5s
    Element Text Should Be      id=message    Success: Attendance marked
    Element Text Should Be      id=count      1

TC02 Duplicate Attendance Prevention E2E
    [Documentation]    Automatically re-submits student ID 101 and blocks duplicate.
    Submit Student Attendance    101
    Wait Until Page Contains    Error: Attendance already marked    timeout=5s
    Element Text Should Be      id=message    Error: Attendance already marked
    Element Text Should Be      id=count      1

TC03 Invalid Student ID Error E2E
    [Documentation]    Automatically submits invalid ID 999 and verifies error.
    Submit Student Attendance    999
    Wait Until Page Contains    Error: Invalid Student ID    timeout=5s
    Element Text Should Be      id=message    Error: Invalid Student ID

TC04 Second Valid Student Increments Count E2E
    [Documentation]    Automatically submits valid student ID 102 and checks count = 2.
    Submit Student Attendance    102
    Wait Until Page Contains    Success: Attendance marked    timeout=5s
    Element Text Should Be      id=message    Success: Attendance marked
    Element Text Should Be      id=count      2

TC05 Blank Student ID Validation E2E
    [Documentation]    Automatically submits empty input and verifies required ID error.
    Submit Student Attendance    ${EMPTY}
    Wait Until Page Contains    Error: Student ID is required    timeout=5s
    Element Text Should Be      id=message    Error: Student ID is required

*** Keywords ***
Reset Attendance And Open Browser
    ${req}=           Evaluate    __import__('importlib').import_module('urllib.request').Request('${URL}/api/reset', method='POST')
    Evaluate          __import__('importlib').import_module('urllib.request').urlopen($req)
    Open Browser      ${URL}    ${BROWSER}
    Maximize Browser Window

Submit Student Attendance
    [Arguments]       ${student_id}
    Go To             ${URL}
    Wait Until Element Is Visible    id=student_id    timeout=5s
    Input Text        id=student_id    ${student_id}
    Click Button      id=submit_btn