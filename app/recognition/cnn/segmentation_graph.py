import gizeh
from collections import defaultdict

def normalize(point, left, top):
    point['x'] = point['x'] - left
    point['y'] = point['y'] - top
    return point

class SegmentationGraph(object):
    def __init__(self, strokes):
        self.states = set()
        self.transitions = defaultdict(set)
        # TODO
        points = [s for stroke in strokes for s in stroke['stroke']]
        xs = map(lambda p: p['x'], points)
        ys = map(lambda p: p['y'], points)
        self.strokes = [{'id': i, 'stroke': [normalize(point, left=min(xs), top=min(ys)) for point in stroke['stroke']]} for i, stroke in enumerate(strokes)]
        for partition in self.generate_slices(strokes):
            states = map(SegmentationState, partition)
            self.states.update(states)
            for a, b in zip(states[:-1], states[1:]):
                self.transitions[a].add(b)

    def generate_slices(self, sequence):
        if len(sequence) == 0:
            yield []
        elif len(sequence) == 1:
            yield [sequence]
        else:
            for s in xrange(1, len(sequence) + 1):
                for rest in self.generate_slices(sequence[s:]):
                    yield [sequence[:s]] + rest


class SegmentationState(object):
    def __init__(self, strokes):
        self.strokes = strokes
        self.ids = "".join(map(lambda s: str(s['id']), self.strokes))

    def image(self):
        points = [s for stroke in self.strokes for s in stroke['stroke']]
        xs = map(lambda p: p['x'], points)
        ys = map(lambda p: p['y'], points)
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        surface = gizeh.Surface(width=width, height=height)
        for stroke in self.strokes:
            self.draw_points(surface, stroke['stroke'], min(xs), min(ys))
        return surface

    def __hash__(self):
        return hash(self.ids)

    def __eq__(self, other):
        return self.strokes == other.strokes

    def __repr__(self):
        return "<SegmentationState: {}>".format(self.ids)

    def draw_points(surface, points, left=0, top=0):
        line = [(p['x'] - left, p['y'] - top) for p in points]
        outline = list(line)
        outline.reverse()
        gizeh.polyline(points=line + outline,
                       stroke_width=3,
                       stroke=(0, 0, 0)).draw(surface)
        return surface
