
from .util  import BrowserManager, CustomHtmlReportGenerator, ExcelFileHandler, ImageManager

class ImageComparator(BrowserManager,CustomHtmlReportGenerator,ExcelFileHandler,ImageManager):
    def __init__(self):
        super().__init__()