import numpy as np
from mlp import NeuralNetwork
from hopfield import A, B, C, D,to_pattern, display

X = np.array ([to_pattern(A), to_pattern(B), to_pattern(C), to_pattern(C)])
y = np.array ([
	[0,1,0,0,0,0,0,1],
	[0,1,0,0,0,0,1,0],
	[0,1,0,0,0,0,1,1],
	[0,1,0,0,0,1,0,0]])

nn = NeuralNetwork([42,50,8], 'tanh')
nn.fit(X, y, epochs=250)

sgn = np.vectorize(lambda x: 0 if x < 0.1 else +1)
for i in range (X.shape[0]):
	print sgn(nn.predict(X[i]))