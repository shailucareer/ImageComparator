import os
import shutil
from collections import defaultdict
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword, not_keyword
from IBasic import IBasic


class CustomHtmlReportGenerator(IBasic):

    TEST_RESULT = defaultdict(list)
    def __init__(self):
        self.ROWS = []

    @keyword
    def setup_html_report(self, output_dir="output", screenshots_dir="output/screenshots"):
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        os.makedirs(screenshots_dir)

    @not_keyword
    def _get_from_test_dict(self):
        test_name = BuiltIn().get_variable_value("${TEST NAME}")
        #print(test_name)
        try:
            existing_items = CustomHtmlReportGenerator.TEST_RESULT[test_name]
        except KeyError:
            CustomHtmlReportGenerator.TEST_RESULT[test_name] = self.ROWS
            existing_items = CustomHtmlReportGenerator.TEST_RESULT[test_name]
        #print(CustomHtmlReportGenerator.TEST_RESULT)
        return existing_items

    # def create_test(self, test_name, description="", matching_percent="", image_path1="", image_path2="",
    #                 browser_device=""):
    #     self._get_from_test_dict(test_name)
    #     print(CustomHtmlReportGenerator.TEST_RESULT)

    @keyword
    def report_browser_device(self, browser_device=""):
        browser_device = browser_device.upper()
        temp_list2 = ["", "", "", "", "", browser_device]
        existing_items = self._get_from_test_dict()
        existing_items.append(temp_list2)
        test_name = BuiltIn().get_variable_value("${TEST NAME}")
        CustomHtmlReportGenerator.TEST_RESULT[test_name] = existing_items
        print(CustomHtmlReportGenerator.TEST_RESULT)

    @keyword
    def report_pass(self, description="", matching_percent="", image_path1="", image_path2="",
                    browser_device=""):
        temp_list = ["PASS", description, matching_percent, image_path1, image_path2, browser_device]
        existing_items = self._get_from_test_dict()
        existing_items.append(temp_list)
        test_name = BuiltIn().get_variable_value("${TEST NAME}")
        CustomHtmlReportGenerator.TEST_RESULT[test_name] = existing_items
        print(CustomHtmlReportGenerator.TEST_RESULT)

    @keyword
    def report_info(self, description="", matching_percent="", image_path1="", image_path2="",
                    browser_device=""):
        temp_list = ["INFO", description, matching_percent, image_path1, image_path2, browser_device]
        existing_items = self._get_from_test_dict()
        existing_items.append(temp_list)
        test_name = BuiltIn().get_variable_value("${TEST NAME}")
        CustomHtmlReportGenerator.TEST_RESULT[test_name] = existing_items
        print(CustomHtmlReportGenerator.TEST_RESULT)

    @keyword
    def report_fail(self, description="", matching_percent="", image_path1="", image_path2="",
                    browser_device=""):
        temp_list = ["FAIL", description, matching_percent, image_path1, image_path2, browser_device]
        existing_items = self._get_from_test_dict()
        existing_items.append(temp_list)
        test_name = BuiltIn().get_variable_value("${TEST NAME}")
        CustomHtmlReportGenerator.TEST_RESULT[test_name] = existing_items
        print(CustomHtmlReportGenerator.TEST_RESULT)

    @keyword
    def generate_html_report(self, html_report_file_path="output/Custom_Report.html"):
        html_content = self._get_html_template()
        #print(html_content)
        with open(html_report_file_path, 'w') as file:
            file.write(html_content)

    @not_keyword
    def _get_html_template(self):
        html = ("<html>"
                "<head>"
                "<title>Responsive Testing Report</title>"
                "<style>"
                "table, th, td {border: 2px solid lightgrey;border-collapse: collapse;font-family: calibri;padding: 5px;} "
                ".desc{max-width: 700px;word-wrap: break-word;}"
                "</style>"
                "</head>"
                "<body>"
                "<h1>Test Report</h1>"
                "<table style='width:100%'>"
                "<h4>Note: Make sure the Display Scaling is set to 100% before running the tests</h4>"
                "<tr><th>Test Case/Browser/Device</th><th>Status</th><th class='desc'>Description</th><th>Matching %</th><th>Overlay Image</th><th>Highlight Diff Image</th></tr>")
        keylist = CustomHtmlReportGenerator.TEST_RESULT.keys()
        #print(keylist)

        for key in keylist:
            html += f"<tr><td>{key}</td><td></td><td></td><td></td><td></td><td></td></tr>"
            list_items = CustomHtmlReportGenerator.TEST_RESULT[key]
            for row in list_items:
                #print(html)
                matching_percent = row[2]
                if matching_percent != "":
                    matching_percent = int(matching_percent)
                image1 = row[3]
                if image1 != "":
                    image1 = f"<a href='{image1}' target='_blank'>Overlayed Img</a>"
                image2 = row[4]
                if image2 != "":
                    image2 = f"<a href='{image2}' target='_blank'>Highlighted Img</a>"
                html += f"<tr><td>{row[5]}</td><td>{row[0]}</td><td class='desc'>{row[1]}</td><td>{matching_percent}</td><td>{image1}</td><td>{image2}</td></tr>"
        html += "</table></body></html>"
        return html

