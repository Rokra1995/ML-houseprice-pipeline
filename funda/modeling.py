
class NeuralNetworkModeller(object):

    def __init__(self, hidden_layers, nodes, activation_function):
        self.hidden_layers = hidden_layers
        self.nodes = nodes
        self.activation_function = activation_function

    def build_neural_network(self, input_data, target):
        NN_model= []
        return NN_model