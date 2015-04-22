import numpy

import theano
import theano.tensor as T

from logistic_sgd import LogisticRegression, load_data
from mlp import HiddenLayer
import json
from cnn import LeNetConvPoolLayer


def classify(example):
    with open("cnn.json") as f:
        network = json.loads(f.read())

    batch_size = 1
    rng = numpy.random.RandomState(23455)
    x = T.matrix('x')
    y = T.ivector('y')

    layer0_input = x.reshape((batch_size, 1, 28, 28))

    input = layer0_input
    layers = []
    network['layers'][0]['image_shape'] = (1,1,28,28)
    network['layers'][1]['image_shape'] = (1,20,12,12)
    for layer in network['layers']:
        if layer['type'] == 'convolutional':
            layers.append(LeNetConvPoolLayer(
                rng,
                input=input,
                image_shape=layer['image_shape'],
                filter_shape=layer['filter_shape'],
                W=theano.shared(numpy.asarray(layer['W'], dtype=theano.config.floatX), borrow=True),
                b=theano.shared(numpy.asarray(layer['b'], dtype=theano.config.floatX), borrow=True),
                poolsize=layer['poolsize'])
            )
            input = layers[-1].output
        elif layer['type'] == 'hidden':
            W = numpy.asarray(layer['W'], dtype=theano.config.floatX)
            b = numpy.asarray(layer['b'], dtype=theano.config.floatX)
            layers.append(HiddenLayer(
                    rng,
                    input=input.flatten(2),
                    n_in=W.shape[0],
                    n_out=W.shape[1],
                    W=theano.shared(W, borrow=True),
                    b=theano.shared(b, borrow=True),
                    activation=T.tanh)
            )
            input = layers[-1].output
        elif layer['type'] == 'softmax':
            W = numpy.asarray(layer['W'], dtype=theano.config.floatX)
            b = numpy.asarray(layer['b'], dtype=theano.config.floatX)
            layers.append(LogisticRegression(
                input=input,
                n_in=W.shape[0],
                n_out=W.shape[1],
                W=theano.shared(W, borrow=True),
                b=theano.shared(b, borrow=True))
            )

    index = T.lscalar()  # index to a [mini]batch
    #datasets = load_data('mnist.pkl.gz')
    #train_set_x, train_set_y = datasets[0]
    #data = train_set_x.get_value()
    #data[0] = example.flatten()
    #train_set_x = theano.shared(data, borrow=True)
    train_set_x = theano.shared(numpy.asarray([example.flatten()], dtype=theano.config.floatX), borrow=True)
    fun = theano.function([index], [layers[0].output, layers[1].output, layers[2].output, layers[3].p_y_given_x, layers[3].y_pred],
            givens={
                x: train_set_x[index * batch_size: (index + 1) * batch_size],
            }, on_unused_input='ignore')
    #fun = theano.function([index], [layers[0].output, layers[1].output, layers[2].output, layers[3].p_y_given_x, layers[3].y_pred],
    #        givens={
    #            x: train_set_x[index * batch_size: (index + 1) * batch_size],
    #            y: train_set_y[index * batch_size: (index + 1) * batch_size]
    #        }, on_unused_input='ignore')

    return fun(0)[-1][0]
