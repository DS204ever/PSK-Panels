from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw

class Matrix:
    def __init__(self) -> None:
        self.options = RGBMatrixOptions()
        self.options.rows = 16
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.multiplexing = 4
        self.options.disable_hardware_pulsing = True
        self.options.hardware_mapping = 'regular'
        self.matrix = RGBMatrix(options = self.options)

    def lightZone(self, rgb: tuple[int, int, int], brightness: int, zone: int) -> None:
        self.matrix.Clear()
        self.matrix.brightness = brightness
        self.image = Image.new("RGB", (self.matrix.height,self.matrix.width))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0,0,int(self.matrix.width/3),self.matrix.height), fill=(rgb[0],rgb[1],rgb[2]))
        self.matrix.SetImage(self.image, zone*self.matrix.width/3, 0)
        
    def applyImage(self, image: Image.Image, brightness: int):
        self.matrix.Clear()
        self.matrix.brightness = brightness
        image.thumbnail((self.matrix.width,self.matrix.height), resample=Image.ANTIALIAS)
        self.matrix.SetImage(image.convert("RGB"))

    