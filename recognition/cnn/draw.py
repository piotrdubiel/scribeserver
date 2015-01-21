import gizeh
import sys
import os


def draw(strokes):
    points = [s for stroke in strokes for s in stroke]
    xs = map(lambda p: int(p['x']), points)
    ys = map(lambda p: int(p['y']), points)

    width = max(xs) - min(xs)
    height = max(ys) - min(ys)

    surface = gizeh.Surface(width=width, height=height)

    for stroke in strokes:
        line = [(int(p['x']) - min(xs), int(p['y']) - min(ys)) for p in stroke]
        outline = list(line)
        outline.reverse()
        gizeh.polyline(points=line+outline,
                       stroke_width=3,
                       stroke=(1, 1, 1)).draw(surface)
    surface.write_to_png('a.png')
    return surface.get_npimage()

if __name__ == "__main__":
    filename = sys.argv[1]
    draw(filename, os.path.splitext(filename)[0] + ".png")
