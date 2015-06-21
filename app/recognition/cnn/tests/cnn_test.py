from nose.tools import ok_
from nose.tools import eq_
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from ..new import CNN
import numpy
import theano


def test_cnn_create():
    cnn = CNN("cnn.json")
    ok_(cnn.layers)
    eq_(len(cnn.layers), 4)


def test_classify():
    rng = numpy.random.RandomState(23455)
    example = numpy.asarray(
                    rng.uniform(low=0.0, high=1.0, size=(28,28)),
                    dtype=theano.config.floatX
                )
    cnn = CNN("cnn.json")
    result = cnn.classify(example)
    ok_(result)
