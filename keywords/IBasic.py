

class IBasic:
    def __init__(self, output_dir="output", screenshots_dir="screenshots", comparison_output_dir = "comparison_output"):
        self.out_dir= output_dir
        self.screenshots_dir = output_dir+"/"+screenshots_dir
        self.comparison_output_dir = output_dir+"/"+comparison_output_dir