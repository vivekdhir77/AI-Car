import random
import math
class NN:
    def __init__(self, neuronCount):
        self.levels = []
        for i in range(len(neuronCount)-1):
            self.levels.append(Level(neuronCount[i], neuronCount[i+1]))
        
        
    
    def feedForeward(self, givenInputs, network):
        outputs =  network.levels[0].feedForward(givenInputs, network.levels[0]);
        for i in range(1, len(network.levels)):
            outputs= network.levels[i].feedForward(outputs,network.levels[i])
        return outputs

    def mutate(self, network, amount = 1):
        for level in network.levels:
            for i in range(len(level.biases)):
                level.biases[i]=lerp(level.biases[i], random.random()*2-1,amount)

            for i in range(len(level.weights)):
                for j in range(len(level.weights[i])):
                    level.weights[i][j]=lerp(level.weights[i][j],random.random()*2-1,amount)

class Level:
    def __init__(self,inputCount,outputCount):
        self.inputs =[0 for i in range(inputCount)]
        self.outputs = [0 for i in range(outputCount)]
        self.biases = [0 for i in range(outputCount)]

        self.weights=[];
        for i in range(inputCount):
            self.weights.append([0 for i in range(outputCount)])

        # self.randomize()
        try:
            f = open('database.json')
            data = json.load(f)
            self.weights = data['weights']
            self.biases = data['weights']
        except:
            for i in range(inputCount):
                for j  in range(outputCount):
                    self.weights[i][j]=random.random()*2-1

            for i in range(outputCount): #biases
                self.biases[i]=random.random()*2-1

    def feedForward(self, givenInputs,level):
        for i in range(len(level.inputs)):
            level.inputs[i]=givenInputs[i]

        for i in range(len(level.outputs)):
            sum = 0
            for j in range(len(level.inputs)):
                sum+=level.inputs[j]*level.weights[j][i]

            if(sum>level.biases[i]):
                level.outputs[i]=1
            else:
                level.outputs[i]=0
        return level.outputs
def lerp(A, B, t): # linear interpolation
    return A+(B-A)*t;