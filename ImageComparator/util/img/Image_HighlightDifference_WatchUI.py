from WatchUI import WatchUI
import os
import time

from robot.api.deco import not_keyword


class Image_HighlightDifference_WatchUI:
    def __init__(self, comparison_output_dir):
        self.comparison_output_dir = comparison_output_dir
        self.watch_ui = WatchUI()

    @not_keyword
    def compare_images(self, img1, img2):
        # Ensure the comparison output directory exists
        if not os.path.exists(self.comparison_output_dir):
            os.makedirs(self.comparison_output_dir)

        try:
            # Perform the image comparison using WatchUI
            self.watch_ui.compare_images(img1, img2, save_folder=self.comparison_output_dir)

        except Exception as e:
            print(f"Error during WatchUI image comparison: {e}")
