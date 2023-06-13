import numpy as np
# scipy.special for the sigmoid function expit()
import scipy.special
import pandas as pd
import cv2 as cv
class neuralNetwork:
    
    
    # initialise the neural network
    def __init__(self):
        # set number of nodes in each input, hidden, output layer
        self.inodes = 784
        self.hnodes = 200
        self.onodes = 10
        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc
        self.wih = None
        self.who = None

        # learning rate
        self.lr = 0.1
        
        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)
    

    
    # train the neural network
    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T
        
        # calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # calculate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        
        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = np.dot(self.who.T, output_errors) 
        
        # update the weights for the links between the hidden and output layers
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))
        
        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))
        
        pass

    def loadWeights(self):
        df_ih = pd.read_csv('I-H_Weights.csv')
        df_ho = pd.read_csv('H-O_Weights.csv')
        df_ih.drop(['Unnamed: 0'], axis=1, inplace=True)
        df_ho.drop(['Unnamed: 0'], axis=1, inplace=True)
        # df_ih
        self.wih =  df_ih.to_numpy()
        self.who =  df_ho.to_numpy()
   
    # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        
        # calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # calculate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs

    def predict_number(self,path:str):

        img = cv.imread(path , 0)
        resizedImage = cv.resize(img, (28, 28), interpolation=cv.INTER_AREA)
        resizedImage = cv.normalize(resizedImage, None, 0.01, 1.0, cv.NORM_MINMAX, dtype=cv.CV_32F)
        finalImg = resizedImage.reshape((1,784))[0]
        outputs = self.query(finalImg)
        # the index of the highest value corresponds to the label
        label = np.argmax(outputs)
        return label
