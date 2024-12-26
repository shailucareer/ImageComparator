
from .util  import BrowserManager, CustomHtmlReportGenerator, ExcelFileHandler, ImageManager

class ImageComparator(BrowserManager,CustomHtmlReportGenerator,ExcelFileHandler,ImageManager):
    def __init__(self):
        BrowserManager.__init__(self)
        CustomHtmlReportGenerator.__init__(self)
        ExcelFileHandler.__init__(self)
        ImageManager.__init__(self)

