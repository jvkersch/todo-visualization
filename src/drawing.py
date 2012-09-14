from PIL import Image, ImageDraw


def _rectangle(input, box, fill, outline, width):
    """
    Helper function to draw rectangle with separate colors for 
    outline and interior. Taken from 
 
        http://nadiana.com/pil-tutorial-basic-advanced-drawing

    Do not use directly.
    """

    draw = ImageDraw.Draw(input)
    draw.rectangle(box, fill=outline) # The outer rectangle
    draw.rectangle( # The inner rectangle
        (box[0] + width, box[1] + width, box[2] - width, box[3] - width),
        fill=fill
    )
 

class RectangleBoard:
    """
    Class to draw lots of rectangles with PIL without having to 
    commit to a fixed-size canvas ahead of time.

    """
    def __init__(self):        
        # Dimensions of drawing area
        self.height = 0
        self.width = 0

        # Rectangle array
        self.rectangles = []

    def _update_size(self, x, y, w, h):
        """Increase size of drawing board."""
        if x + w > self.width:
            self.width = x + w
        if y + h > self.height:
            self.height = y + h

    def add_rectangle(self, corner, size, 
                      color_fg, color_bg=None, thickness=1):
        """Store rectangle for drawing later on."""
        
        # Increase maximum drawing area if necessary
        x, y = corner
        w, h = size

        dim = (x, y, x + w, y + h)

        self._update_size(x, y, w, h)
            
        # Store rectangle data
        if color_bg is None:
            color_bg = color_fg

        self.rectangles.append((dim, color_fg, color_bg, thickness))

    def clear(self):
        """Delete all rectangles and reset drawing area"""

        self.rectangles = []
        self.width = 0
        self.height = 0

    def make_drawing(self, border=5):
        """
        Draw rectangles on the canvas and store result.

        """
        im = Image.new('RGBA', 
                       (self.width + 2*border, self.height + 2*border),
                       (0, 0, 0, 0))

        for dim, color_fg, color_bg, thickness in self.rectangles:
            _rectangle(im, dim, color_bg, color_fg, thickness)
        return im


if __name__ == '__main__':

    r = RectangleBoard()

    r.add_rectangle((3, 4), (5, 6), 'red')
    r.add_rectangle((10, 40), (12, 17), 'green', 'yellow', 3)
    r.add_rectangle((50, 12), (20, 20), 'cyan', 'blue', 2)

    im = r.make_drawing()
    im.save('test.png')
