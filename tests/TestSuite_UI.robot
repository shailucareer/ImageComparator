*** Settings ***
Library    ../ImageComparator/util/ImageManager.py
Library    ../ImageComparator/util/CustomHtmlReportGenerator.py
Library    ../ImageComparator/util/BrowserManager.py
Library     ../ImageComparator/util/ExcelFileHandler.py
Library    String
Library    SeleniumLibrary
Suite Setup     Setup HTML Report    ${OUTPUT_DIR}    ${SCREENSHOTS_DIR}
Suite Teardown     Generate HTML Report    ${HTML_REPORT_FILE_PATH}

*** Variables ***
${EXCEL_FILE}     ${CURDIR}/Resolutions.xlsx
${SHEET_NAME}     Sheet1
${WAIT_TIME_IN_SECONDS}    5
${OUTPUT_DIR}     ${CURDIR}/output
${FIGMA_DIR}     ${CURDIR}/figma
${SCREENSHOTS_DIR}     ${OUTPUT_DIR}/screenshots
${COMPARISON_OUTPUT_DIR}     ${OUTPUT_DIR}/comparison_output
${HTML_REPORT_FILE_PATH}     ${OUTPUT_DIR}/Custom_Report.html


*** Test Cases ***
Sample test to Compare 2 different images
    ${img1}     Set Variable     ${FIGMA_DIR}/345_figma_1.png
    ${img2}     Set Variable     ${SCREENSHOTS_DIR}/Screenshot1733424304.6816137.png
    Report Browser Device     chrome
    ${timestamp}    Get Timestamp
    ${img2}     Set Variable    ${SCREENSHOTS_DIR}/Screenshot${timestamp}.png
    Capture Page Screenshot    ${img2}
    Report Info    Screenshot saved at: ${img2}
    ${screenshot_width}     ${screenshot_height}     Get Image Dimensions    ${img2}
    Report Info    Screenshot dimension:${screenshot_width}x${screenshot_height}
    Compare 2 Images And Find Difference     ${img1}     ${img2}    ${COMPARISON_OUTPUT_DIR}

Sample test to Compare 2 similar images
    ${img1}     Set Variable     ${FIGMA_DIR}/345_figma.png
    ${img2}     Set Variable     ${SCREENSHOTS_DIR}/headlesschrome_Mobile.png
    Report Browser Device     chrome
    Compare 2 Images And Find Difference  ${img1}     ${img2}       ${COMPARISON_OUTPUT_DIR}

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
            Report Browser Device    ${browser}-${device}
            ${figma_image_path}     Set Variable    ${FIGMA_DIR}/${FIGMA_IMAGE_NAME}
            Report Info     Figma Image path - ${figma_image_path}
            Report Info    Page url - ${url}
            ${figma_width}    ${figma_height}   Get Image Dimensions    ${figma_image_path}
            Report Info    Figma Image Size=${figma_width}x${figma_height}
            ${CONTINUE_EXECUTION}       Launch Browser    ${url}    ${browser}    ${figma_width}    ${figma_height}
            Sleep    ${WAIT_TIME_IN_SECONDS}s
            IF    ${CONTINUE_EXECUTION}
                ##########
                # In case you need to perform some action on the app such as login/navigation/expand/collapse
                # Please write the code just before capture screenshot
                ##########
                Capture Screenshot of live app and compare with passed image    ${figma_image_path}     ${SCREENSHOTS_DIR}      ${COMPARISON_OUTPUT_DIR}
                Close All Browsers
            END
        END
    END
