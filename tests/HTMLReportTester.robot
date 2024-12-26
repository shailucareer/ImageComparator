
*** Settings ***
Library    ../ImageComparator/util/CustomHtmlReportGenerator.py
Suite Setup     Setup HTML Report
Suite Teardown     Generate HTML Report


*** Variables ***
${OUTPUT_DIR}     ${CURDIR}/output
${SCREENSHOTS_DIR}     ${OUTPUT_DIR}/screenshots
${HTML_REPORT_FILE_PATH}     ${OUTPUT_DIR}/Custom_Report.html


*** Test Cases ***
TC1
    Report Info    chrome-mobile
    Report Info    Desc 1.1
    Report Info    Comparison    25    img1.png    img2.png
    Report Info    firefox-mobile
    Report Info    Desc 1.1
    Report Info    Comparison    25    img1.png    img2.png

TC2
    Report Info    chrome-mobile
    Report Info    Desc 1.2
    Report Info    Comparison    45    img1.png    img2.png