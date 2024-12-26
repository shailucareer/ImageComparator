from time import sleep

from robot.api.deco import keyword, not_keyword
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from robot.libraries.BuiltIn import BuiltIn


from IBasic import IBasic
from CustomHtmlReportGenerator import CustomHtmlReportGenerator

class BrowserManager(IBasic):
    def __init__(self):
        self.driver = None
        self.report = CustomHtmlReportGenerator()

    @keyword
    def launch_browser(self, url, browser, width, height):
        width = int(width)
        height = int(height)

        browser = browser.lower()
        if browser in "headlessedge":
            continue_execution =self._launch_edge(url, width, height)
        elif browser in "headlesschrome":
            continue_execution =self._launch_chrome(url, width, height)
        else:
            continue_execution =self._launch_firefox(url, width, height)

        self.driver.get(url)
        selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
        selenium_lib.register_driver(self.driver, 'webdriver')
        return continue_execution

    @not_keyword
    def _resize_browser_window(self, width, height):
        new_width, new_height = self.driver.get_window_size().values()
        #self.report.report_info(f"Browser window size: {new_width}x{new_height}")

        self.driver.set_window_size(width, height)

        inner_width = self.driver.execute_script("return window.innerWidth;")
        inner_height = self.driver.execute_script("return window.innerHeight;")
        
        #new_width, new_height = self.driver.get_window_size().values()
        #self.report.report_info(f"Browser window size: {new_width}x{new_height}")


        new_width = width + (width - inner_width)
        #self.report.report_info(f"new_width: {new_width}")
        new_height = height + (height - inner_height)
        #self.report.report_info(f"new_height: {new_height}")

        self.driver.set_window_size(new_width, new_height)
        new_width, new_height = self.driver.get_window_size().values()
        self.report.report_info(f"Adjusted Browser window size: {new_width}x{new_height}")

    @not_keyword
    def _launch_firefox(self, url, width, height):
        continue_execution = True
        options = FirefoxOptions()
        options.add_argument("--headless")
        if width <= 500:
            print("FIREFOX NOT SUPPORTED FOR RESOLUTIONS LESS THAN 500 px")
            self.report.report_info("FIREFOX NOT SUPPORTED FOR RESOLUTIONS LESS THAN 500 px")
            continue_execution = False

        self.driver = webdriver.Firefox(options=options)
        self._resize_browser_window(width, height)
        return continue_execution

    @not_keyword
    def _launch_edge(self, url, width, height):
        continue_execution = True
        options = EdgeOptions()
        options.add_argument("--headless")
        if width <= 500:
            device_metrics = {"width": width, "height": height}
            mobile_emulation = {"deviceMetrics": device_metrics}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            self.driver = webdriver.Edge(options=options)
            new_width, new_height = self.driver.get_window_size().values()
            print(f"Browser window size: {new_width}x{new_height}")
            self.report.report_info(f"Browser window size: {new_width}x{new_height}")
        else:
            self.driver = webdriver.Edge(options=options)
            self._resize_browser_window(width, height)
        return continue_execution

    @not_keyword
    def _launch_chrome(self, url, width, height):
        continue_execution = True
        options = ChromeOptions()
        options.add_argument("--headless")
        if width <= 500:
            device_metrics = {"width": width, "height": height}
            mobile_emulation = {"deviceMetrics": device_metrics}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            self.driver = webdriver.Chrome(options=options)
            new_width, new_height = self.driver.get_window_size().values()
            print(f"Browser window size: {new_width}x{new_height}")
            self.report.report_info(f"Browser window size: {new_width}x{new_height}")
        else:
            self.driver = webdriver.Chrome(options=options)
            self._resize_browser_window(width, height)
        return continue_execution

    @keyword
    def switch_to_active_element(self):
        element = self.driver.switch_to.active_element
        return element

    @keyword
    def get_browser(self):
        return self.driver
