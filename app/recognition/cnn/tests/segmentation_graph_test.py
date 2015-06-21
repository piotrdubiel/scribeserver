from nose.tools import ok_
from nose.tools import eq_
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from ..segmentation_graph import SegmentationGraph


def test_graph_create():
    # given
    strokes = [{
        'id': 1,
        'stroke': [
            {'x': 4.0, 'y': 4.0},
            {'x': 5.0, 'y': 5.0}
        ]
    }]

    # when
    graph = SegmentationGraph(strokes)

    # then
    ok_(graph)
