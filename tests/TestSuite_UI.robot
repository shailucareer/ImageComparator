*** Settings ***
Resource    util/CustomHtmlReportGenerator.robot
Resource    util/ImageManager.robot
Resource    util/BrowserManager.robot
Library     util/ExcelFileHandler.py
Suite Setup     Setup HTML Report
Suite Teardown     Generate HTML Report

*** Test Cases ***
Sample test to Compare 2 different images
    ${img1}     Set Variable     ${FIGMA_DIR}/345_figma_1.png
    ${img2}     Set Variable     ${SCREENSHOTS_DIR}/Screenshot1733424304.6816137.png
    Report-Browser/Device     chrome
    Compare 2 Images And Find Difference  ${img1}     ${img2}

Sample test to Compare 2 similar images
    ${img1}     Set Variable     ${FIGMA_DIR}/345_figma.png
    ${img2}     Set Variable     ${SCREENSHOTS_DIR}/headlesschrome_Mobile.png
    Report-Browser/Device     chrome
    Compare 2 Images And Find Difference  ${img1}     ${img2}

Data driven test to Compare figma images fetched from excel with live site in Cross-Browser setting
    [Template]    Responsive and Cross-Browser Testing Common Keyword
    chrome
    #firefox
    #edge

*** Keywords ***
Responsive and Cross-Browser Testing Common Keyword
    [Arguments]      ${browser}
    ${row_len}      Get Row Count    ${EXCEL_FILE}    ${SHEET_NAME}
    FOR    ${row}    IN RANGE    0    ${row_len}
        ${run}    Get Cell Value    ${EXCEL_FILE}    ${SHEET_NAME}    ${row}     0

        ${run}  Convert To Lower Case    ${run}
        IF    "${run}" == "y"
            ${device}      Get Cell Value    ${EXCEL_FILE}    ${SHEET_NAME}    ${row}     1
            ${figma_image_name}      Get Cell Value    ${EXCEL_FILE}    ${SHEET_NAME}    ${row}     2
            ${url}      Get Cell Value    ${EXCEL_FILE}    ${SHEET_NAME}    ${row}     3
            Report-Browser/Device     ${browser}-${device}
            ${figma_image_path}     Set Variable    ${FIGMA_DIR}/${FIGMA_IMAGE_NAME}
            Report-Info     Figma Image path - ${figma_image_path}
            Report-Info     Page url - ${url}
            ${STOP_EXECUTION}       Launch Browser    ${url}    ${browser}    ${figma_image_path}
            IF    "${STOP_EXECUTION}"=="NO"
                ##########
                # In case you need to perform some action on the app such as login/navigation/expand/collapse
                # Please write the code just before capture screenshot
                ##########
                Capture Screenshot of live app and compare with passed image    ${figma_image_path}
                Close All Browsers
            END
        END
    END
