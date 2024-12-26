from PIL import Image, ImageChops, ImageDraw, ImageFont
import os
import time

from robot.api.deco import not_keyword
from ImageComparator.IBasic import IBasic


class Image_HighlightDifference_PIL(IBasic):
    def __init__(self, out_image_dir):
        self.out_image_dir = out_image_dir

    @not_keyword
    def find_diff(self, path_one, path_two):
        try:
            # Open the two images
            image1 = Image.open(path_one)
            image2 = Image.open(path_two)

            # Ensure both images have the same mode
            image1 = image1.convert('RGB')
            image2 = image2.convert('RGB')

            # Find the difference between the images
            diff = ImageChops.difference(image1, image2)

            # Calculate the percentage of matching pixels
            diff_data = diff.getdata()
            total_pixels = len(diff_data)
            matching_pixels = sum(1 for pixel in diff_data if pixel == (0, 0, 0))
            matching_percentage = (matching_pixels / total_pixels) * 100
            matching_percentage = round(matching_percentage, 0)

            print(f"Matching Percentage: {matching_percentage:.2f}%")

            # Highlight the differences by enhancing the contrast
            diff = ImageChops.add(diff, diff, 2.0, -100)

            # Create a white background image
            white_bg = Image.new('RGB', image1.size, (255, 255, 255))

            # Convert the difference image to grayscale to use as a mask
            mask = diff.convert('L')

            # Paste the difference image onto the white background using the mask
            white_bg.paste(diff, (0, 0), mask)

            # Create a new image with a width that is the sum of the widths of the three images
            total_width = image1.width + image2.width + white_bg.width
            max_height = max(image1.height, image2.height, white_bg.height) + 20

            merged_image = Image.new('RGB', (total_width, max_height))

            # Paste the images side by side
            merged_image.paste(image1, (0, 20))
            merged_image.paste(white_bg, (image1.width, 20))
            merged_image.paste(image2, (image1.width + white_bg.width, 20))

            try:
                font = ImageFont.truetype("arial.ttf", 24)  # Use a truetype font if available
            except IOError:
                font = ImageFont.load_default()  # Fallback to default font if truetype font is not available

            # Draw the matching percentage on the white background image
            draw = ImageDraw.Draw(merged_image)
            font = ImageFont.load_default()
            image1_name = os.path.basename(path_one)
            image2_name = os.path.basename(path_two)
            text = f"Matching: {matching_percentage:.2f}%"
            draw.text((image1.width, 5), text, fill="white", font=font)
            draw.text((10, 5), image1_name, fill="white", font=font)
            draw.text(((image1.width + white_bg.width), 5), image2_name, fill="white", font=font)

            # Save or display the result
            timestamp = str(time.time())
            out_image_path = os.path.join(self.out_image_dir, f"Overlay{timestamp}.png")
            merged_image.save(out_image_path)

            return matching_percentage, out_image_path

        except Exception as e:
            print(f"Error during PIL image comparison: {e}")
            return None, None

    @not_keyword
    def get_image_dimensions(self, image_path):
        with Image.open(image_path) as img:
            return img.size
