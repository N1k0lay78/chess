from core.UI.BaseUI import BaseUI


class TransformLogo(BaseUI):
    def __init__(self, window, center, img, start_size, end_size, time):
        super().__init__(window, [center[0] - start_size[0], center[1] - start_size[1]], image=img)
        self.start_size = start_size
        self.end_size = end_size
        self.time = time

    def update(self, event):