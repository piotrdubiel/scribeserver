import gizeh
import sys
from lxml import objectify
from itertools import chain, combinations
from collections import defaultdict
import numpy as np


def read(filename):
    root = objectify.parse(filename).getroot()
    strokes = [[make_numbers(point.attrib) for point in stroke.Point] for stroke in root.StrokeSet.Stroke]

    points = [s for stroke in strokes for s in stroke]
    xs = map(lambda p: p['x'], points)
    ys = map(lambda p: p['y'], points)

    return [{'id': i, 'stroke': [normalize(point, left=min(xs), top=min(ys)) for point in stroke]} for i, stroke in enumerate(strokes)]

def normalize(point, left, top):
    return {'x': point['x'] - left, 'y': point['y'] - top, 'time': point['time']}

def make_numbers(point):
    return {'x': int(point['x']), 'y': int(point['y']), 'time': float(point['time'])}

def draw(strokes):
    points = [s for stroke in strokes for s in stroke]
    xs = map(lambda p: p['x'], points)
    ys = map(lambda p: p['y'], points)

    width = max(xs)
    height = max(ys)

    surface = gizeh.Surface(width=width, height=height)

    for stroke in strokes:
        line = [(p['x'], p['y']) for p in stroke]
        outline = list(line)
        outline.reverse()
        gizeh.polyline(points=line + outline,
                       stroke_width=3,
                       stroke=(1, 1, 1)).draw(surface)

        #[gizeh.circle(r=9,
        #              xy=(point['x'] - min(xs), point['y'] - min(ys)),
        #              fill=(1,0,0)).draw(surface)
        # for point in generate_cuts(stroke)]
    #time_sum = 0
    #time_threshold = 0.02
    #time_diffs = [0] + map(lambda pair: pair[1]['time'] - pair[0]['time'], zip(points[:-1], points[1:]))
    #for point, diff in zip(points, time_diffs):
    #    time_sum += diff
    #    if time_sum > time_threshold:
    #        gizeh.circle(r=9,xy=(point['x'] - min(xs), point['y'] - min(ys)), fill=(1,0,1)).draw(surface)
    #        time_sum = 0
    surface.write_to_png('a.png')
    return surface.get_npimage()


def draw_points(surface, points, left=0, top=0):
    line = [(p['x'] - left, p['y'] - top) for p in points]
    outline = list(line)
    outline.reverse()
    gizeh.polyline(points=line + outline,
                    stroke_width=3,
                    stroke=(0, 0, 0)).draw(surface)
    return surface

def powerset(iterable):
  xs = list(iterable)
  return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def generate_cuts(points):
    time_sum = 0
    time_threshold = 0.1
    distance_threshold = 100
    distance_sum = 0
    #return points[::(len(points) / 10) + 1]
    time_diffs = [0] + map(lambda pair: pair[1]['time'] - pair[0]['time'], zip(points[:-1], points[1:]))
    distance_diffs = [0] + map(lambda pair: sqrt((pair[1]['x'] - pair[0]['x'])**2 + (pair[1]['y'] - pair[0]['y'])**2), zip(points[:-1], points[1:]))
    for point, time, distance in zip(points, time_diffs, distance_diffs):
        time_sum += time
        distance_sum += distance
        if time_sum > time_threshold or distance_sum > distance_threshold:
            time_sum = 0
            distance_sum = 0
            yield point

def generate_segments(strokes):
    points = [s for stroke in strokes for s in stroke]
    xs = map(lambda p: p['x'], points)
    ys = map(lambda p: p['y'], points)
    width = max(xs)
    height = max(ys)

    surface = gizeh.Surface(width=width, height=height)
    for i, stroke in enumerate(strokes):
        cuts = list(generate_cuts(stroke))
        #if len(cuts) > 12: cuts = cuts[::int(ceil(len(cuts) / 12.0))]
        image = surface.get_npimage()
        histogram = np.sum(np.sum(image/255, 0), 1)
        lines = np.where(histogram == np.min(histogram))

        print len(cuts), 2**len(cuts)
        #x = list(powerset(cuts))
        surface = draw_points(surface, stroke)
        for cut in cuts:
            gizeh.circle(r=9,xy=(cut['x'], cut['y']), fill=(1,0,1)).draw(surface)
    surface.write_to_png('a.png')

class SegmentationGraph(object):
    def __init__(self, strokes):
        self.states = set()
        self.transitions = defaultdict(set)
        for partition in generate_slices(strokes):
            states = map(SegmentationState, partition)
            self.states.update(states)
            for a, b in zip(states[:-1], states[1:]):
                self.transitions[a].add(b)


class SegmentationState(object):
    def __init__(self, strokes):
        self.strokes = strokes
        self.ids = "".join(map(lambda s: str(s['id']), self.strokes))

    def image(self):
        points = [s for stroke in self.strokes for s in stroke['stroke']]
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
        xs = map(lambda p: p['x'], points)
        ys = map(lambda p: p['y'], points)
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        surface = gizeh.Surface(width=width, height=height)
        for stroke in self.strokes:
            draw_points(surface, stroke['stroke'], min(xs), min(ys))
        return surface

    def __hash__(self):
        return hash(self.ids)

    def __eq__(self, other):
        return self.strokes == other.strokes

    def __repr__(self):
        return "<SegmentationState: {}>".format(self.ids)


def generate_slices(sequence):
    if len(sequence) == 0:
        yield []
    elif len(sequence) == 1:
        yield [sequence]
    else:
        for s in xrange(1, len(sequence) + 1):
            for rest in generate_slices(sequence[s:]):
                yield [sequence[:s]] + rest

def getPermutations(string):
    if len(string) == 1:
        yield [string]
    else:
        for i in xrange(len(string)):
            for perm in getPermutations(string[:i] + string[i+1:]):
                yield [string[i]].append(perm)

if __name__ == "__main__":
    filename = sys.argv[1]
    strokes = read(filename)
    image = draw(strokes)
    #m=np.sum(np.sum(image/255, 0), 1)
    #plt.hist(m)

    z=SegmentationGraph(strokes[:4])
    t=z.states.pop()
    t.image()
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT


    #SegmentationGraph(strokes)
    #generate_segments(strokes)
