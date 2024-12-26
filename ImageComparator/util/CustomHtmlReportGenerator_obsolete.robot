*** Settings ***
Library    Collections
Library    OperatingSystem
Library    String

*** Variables ***
&{TEST_RESULT}
@{ROWS}

*** Keywords ***
Setup HTML Report
    [Arguments]     ${OUTPUT_DIR}       ${SCREENSHOTS_DIR}
    Remove Directory    ${OUTPUT_DIR}    recursive=True
    Create Directory    ${OUTPUT_DIR}
    Create Directory    ${SCREENSHOTS_DIR}

Private_Get From Test Dict
    TRY
        ${existing_items}     Get From Dictionary    ${TEST_RESULT}   ${TEST_NAME}
    EXCEPT
        Set To Dictionary       ${TEST_RESULT}      ${TEST_NAME}=@{ROWS}
        ${existing_items}     Get From Dictionary    ${TEST_RESULT}   ${TEST_NAME}
    END
    Log    ${TEST_RESULT}
    RETURN      ${existing_items}


Report-Browser/Device
    [Arguments]     ${BrowserDevice}=${EMPTY}
    ${BrowserDevice}    Convert To Upper Case    ${BrowserDevice}
    ${temp_list2}     Create List     ${EMPTY}       ${EMPTY}      ${EMPTY}     ${EMPTY}    ${EMPTY}    ${BrowserDevice}
    ${existing_items}     Private_Get From Test Dict
    Append To List     ${existing_items}   ${temp_list2}
    Set To Dictionary       ${TEST_RESULT}      ${TEST_NAME}=${existing_items}
    Log    ${TEST_RESULT}


Report-Pass
    [Arguments]     ${Description}=${EMPTY}      ${Matching_Percent}=${EMPTY}     ${Image_Path1}=${EMPTY}     ${Image_Path2}=${EMPTY}        ${BrowserDevice}=${EMPTY}
    ${temp_list}     Create List     PASS       ${Description}      ${Matching_Percent}     ${Image_Path1}     ${Image_Path2}   ${BrowserDevice}
    ${existing_items}     Private_Get From Test Dict
    Append To List     ${existing_items}   ${temp_list}
    Set To Dictionary       ${TEST_RESULT}      ${TEST_NAME}=${existing_items}
    Log    ${TEST_RESULT}

Report-Info
    [Arguments]     ${Description}=${EMPTY}      ${Matching_Percent}=${EMPTY}     ${Image_Path1}=${EMPTY}     ${Image_Path2}=${EMPTY}        ${BrowserDevice}=${EMPTY}
    ${temp_list}     Create List     INFO       ${Description}      ${Matching_Percent}     ${Image_Path1}     ${Image_Path2}   ${BrowserDevice}
    ${existing_items}     Private_Get From Test Dict
    Append To List     ${existing_items}   ${temp_list}
    Set To Dictionary       ${TEST_RESULT}      ${TEST_NAME}=${existing_items}
    Log    ${TEST_RESULT}

Report-Fail
    [Arguments]     ${Description}=${EMPTY}      ${Matching_Percent}=${EMPTY}     ${Image_Path1}=${EMPTY}     ${Image_Path2}=${EMPTY}        ${BrowserDevice}=${EMPTY}
    ${temp_list}     Create List     FAIL       ${Description}      ${Matching_Percent}     ${Image_Path1}     ${Image_Path2}   ${BrowserDevice}
    ${existing_items}     Private_Get From Test Dict
    Append To List     ${existing_items}   ${temp_list}
    Set To Dictionary       ${TEST_RESULT}      ${TEST_NAME}=${existing_items}
    Log    ${TEST_RESULT}

Generate HTML Report
    [Arguments]     ${HTML_REPORT_FILE_PATH}
    ${html_content}    Private_Get HTML Template
    Create File    ${HTML_REPORT_FILE_PATH}    ${html_content}


Private_Get HTML Template
    ${html}=    Set Variable    <html><head><title>Responsive Testing Report</title><style>table, th, td {border: 2px solid lightgrey;border-collapse: collapse;font-family: calibri;padding: 5px;} .desc{max-width: 700px;word-wrap: break-word;}</style></head><body><h1>Test Report</h1><table style="width:100%"><tr><th>Test Case/Browser/Device</th><th>Status</th><th class='desc'>Description</th><th>Matching %</th><th>Overlay Image</th><th>Highlight Diff Image</th></tr>
    ${keylist}      Get Dictionary Keys    ${TEST_RESULT}
    FOR    ${key}    IN    @{keylist}
        ${html}=    Set Variable    ${html}<tr><td>${key}</td><td></td><td></td><td></td><td></td><td></td></tr>
        ${list}     Get From Dictionary    ${TEST_RESULT}    ${key}
        FOR    ${row}    IN    @{list}
            ${matching_percent}     Set Variable    ${row[2]}
            IF     "${matching_percent}" != "${EMPTY}"
                 ${matching_percent}     Convert To Integer    ${matching_percent}
            END

            ${image1}     Set Variable    ${row[3]}
            ${flag}     Evaluate    r"${image1}" != "${EMPTY}"
            IF     ${flag}
                 ${image1}     Set Variable      <a href="${image1}" target="_blank">Overlayed Img</a>
            END

            ${image2}     Set Variable    ${row[4]}
            ${flag}     Evaluate    r"${image2}" != "${EMPTY}"
            IF     ${flag}
                 ${image2}     Set Variable      <a href="${image2}" target="_blank">Highlighted Img</a>
            END

            ${html}=    Set Variable    ${html}<tr><td>${row[5]}</td><td>${row[0]}</td><td class='desc'>${row[1]}</td><td>${matching_percent}</td><td>${image1}</td><td>${image2}</td></tr>
        END
    END
    ${html}=    Set Variable    ${html}</table></body></html>
    RETURN    ${html}

