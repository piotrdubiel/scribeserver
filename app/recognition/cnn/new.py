import numpy
import theano
import theano.tensor as T
import json
from .convolution_layer import LeNetConvPoolLayer
from .hidden_layer import HiddenLayer
from .softmax_layer import LogisticRegression

class CNN(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.network = json.loads(f.read())
        self.init_network()

    def classify(self, example):
        index = T.lscalar()
        train_set_x = theano.shared(numpy.asarray([example.flatten()],
                                                  dtype=theano.config.floatX), borrow=True)
        fun = theano.function([index], [self.layers[0].output,
                                        self.layers[1].output,
                                        self.layers[2].output,
                                        self.layers[3].p_y_given_x,
                                        self.layers[3].y_pred],
            givens={
                self.x: train_set_x[index:(index + 1) ],
            }, on_unused_input='ignore')

        return fun(0)[-1][0]

    def init_network(self):
        batch_size = 1
        rng = numpy.random.RandomState(23455)

        self.x = T.matrix('x')
        self.y = T.ivector('y')
        self.input_layer = self.x.reshape((batch_size, 1, 28, 28))
        self.layers = []
        self.network['layers'][0]['image_shape'] = (1, 1, 28, 28)
        self.network['layers'][1]['image_shape'] = (1, 20, 12, 12)

        current_input = self.input_layer
        for layer in self.network['layers']:
            if layer['type'] == 'convolutional':
                self.layers.append(LeNetConvPoolLayer(
                    rng,
                    input=current_input,
                    image_shape=layer['image_shape'],
                    filter_shape=layer['filter_shape'],
                    W=theano.shared(numpy.asarray(layer['W'], dtype=theano.config.floatX), borrow=True),
                    b=theano.shared(numpy.asarray(layer['b'], dtype=theano.config.floatX), borrow=True),
                    poolsize=layer['poolsize'])
                )
                current_input = self.layers[-1].output
            elif layer['type'] == 'hidden':
                W = numpy.asarray(layer['W'], dtype=theano.config.floatX)
                b = numpy.asarray(layer['b'], dtype=theano.config.floatX)
                self.layers.append(HiddenLayer(
                        rng,
                        input=current_input.flatten(2),
                        n_in=W.shape[0],
                        n_out=W.shape[1],
                        W=theano.shared(W, borrow=True),
                        b=theano.shared(b, borrow=True),
                        activation=T.tanh)
                )
                current_input = self.layers[-1].output
            elif layer['type'] == 'softmax':
                W = numpy.asarray(layer['W'], dtype=theano.config.floatX)
                b = numpy.asarray(layer['b'], dtype=theano.config.floatX)
                self.layers.append(LogisticRegression(
                    input=current_input,
                    n_in=W.shape[0],
                    n_out=W.shape[1],
                    W=theano.shared(W, borrow=True),
                    b=theano.shared(b, borrow=True))
                )
