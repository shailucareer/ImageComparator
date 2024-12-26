*** Settings ***
Library    ../ImageComparator/util/ImageManager.py

*** Test Cases ***
TC1
    ${w}     ${h}    Get Image Dimensions    ${CURDIR}/figma/345_figma.png
    Log    ${w}x${h}
    ${w}     ${h}    Get Image Dimensions    ${CURDIR}/figma/1440_figma.png
    Log    ${w}x${h}

TC2
    ${img1}     Set Variable    ${CURDIR}/output/screenshots/Screenshot1735050493.1878655.png
    ${img2}     Set Variable    ${CURDIR}/figma/1440_figma.png
    Compare Images And Find Difference      ${img1}     ${img2}
