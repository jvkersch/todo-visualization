import os
import sys

from drawing import RectangleBoard
from summary import SummaryList
from todo_api import parse_todo_file

colors = {
    "A": ("red", "red"),
    "B": ("gold", "gold"),
    "None": ("lawngreen", "lawngreen")
}

# Size of rectangles
rw = 10
rh = 10


def visualize(r, x, y, s):
    """
    Adds visualization of given summaries to drawing board, starting
    at specific location.

    """

    for pri, age in s.summaries:
        if pri is None:
            pri = "None"
        
        fg, bg = colors[pri]
        r.add_rectangle((x, y), (10, 10), fg, bg)
        
        x += rw + 5 # size of rectangle + space

    return r

def process_summaries_folder(foldername, output_filename):
    """
    Create image based on summaries in given folder.

    """

    r = RectangleBoard()
    x, y = 5, 5

    files = os.listdir(foldername)
    files.sort(reverse=True)

    for filename in files:
        s = SummaryList()
        s.load(foldername + '/' + filename)

        visualize(r, x, y, s)
        y += rh + 5 # Next line

    im = r.make_drawing()
    im.save(output_filename)


if __name__ == '__main__':
    # Process summary folder specified on command line

    try: 
        folder = sys.argv[1]
        image_out = sys.argv[2]
    except IndexError:
        print "Usage: %s [folder name] [filename for image file]" % \
            sys.argv[0]

    process_summaries_folder(folder, image_out)
