from numpy import exp, array, random, dot


class NeuralNetwork():
    def __init__(self):
        random.seed(1)
        self.synaptic_weights = 2 * random.random((3, 1)) - 1

    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    def train(self, training_inputs, training_outputs, no_trainings):
        for iteration in xrange(no_trainings):
            output = self.think(training_inputs)
            error = training_outputs - output
            adjustment = dot(training_inputs.T, error * self.__sigmoid_derivative(output))
            self.synaptic_weights += adjustment

    def think(self, inputs):
        return self.__sigmoid(dot(inputs, self.synaptic_weights))


if __name__ == "__main__":
    neural_network = NeuralNetwork()

    print "Random starting synaptic weights: ", neural_network.synaptic_weights

    training_inputs = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    training_outputs = array([[0, 1, 1, 0]]).T
    neural_network.train(training_inputs, training_outputs, 1000000)

    print "New synaptic weights after training: ", neural_network.synaptic_weights
    print "Considering new situation [1, 0, 0] -> ?: ", neural_network.think(array([1, 0, 0]))
