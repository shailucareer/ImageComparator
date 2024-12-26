import os
import time
from ImageComparator.util.img.Image_HighlightDifference_PIL import Image_HighlightDifference_PIL
from ImageComparator.util.img.Image_HighlightDifference_WatchUI import Image_HighlightDifference_WatchUI
from CustomHtmlReportGenerator import CustomHtmlReportGenerator
from robot.api.deco import keyword, not_keyword


class ImageManager:
    def __init__(self):
        self.comparison_output_dir = "output/comparison_output"
        self.img_compare_watchui = Image_HighlightDifference_WatchUI(self.comparison_output_dir)
        self.img_compare_pil = Image_HighlightDifference_PIL(self.comparison_output_dir)
        self.report = CustomHtmlReportGenerator()

    @keyword
    def get_image_dimensions(self, image_path):
        return self.img_compare_pil.get_image_dimensions(image_path)

    @keyword
    def compare_images_and_find_difference(self, img1, img2):
        self.img_compare_watchui.compare_images(img1, img2)
        diff_img = self._get_last_updated_file_path(self.comparison_output_dir)
        print(f"WatchUI highlighted difference image : {diff_img}")

        matching_percent, overlay_img = self.img_compare_pil.find_diff(img1, img2)
        print(f"PIL overlayed difference image: {overlay_img}")
        return matching_percent, overlay_img, diff_img

    @not_keyword
    def _get_last_updated_file_path(self, folder):
        # adding a 1 sec sleep, so that watch ui output img.png gets saved in the file system
        time.sleep(1)
        files = os.listdir(folder)
        latest_file = None
        latest_time = 0
        for file in files:
            file_path = os.path.join(folder, file)
            modified_time = os.path.getmtime(file_path)
            if modified_time > latest_time:
                latest_time = modified_time
                latest_file = file
        print(f"Fetching the path of the latest file in {folder} folder {latest_file}")
        return os.path.join(folder, latest_file)

    @keyword
    def get_timestamp(self):
        return str(time.time())