import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.evaluate import plot_decision_regions
class Perceptron(object):

    def __init__(self, eta=0.01, epochs=50):
        self.eta = eta
        self.epochs = epochs

    def train(self, X, y):

        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.epochs):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] +=  update * xi
                self.w_[0] +=  update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, -1)


df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)

# setosa and versicolor
#X = np.array([[-1,-1],[-1,1],[1,-1],[1,1]])
#y = np.array([-1,1,1,1])

X = np.array([[-1.5,0],[-1,1],[-1,0],[-1,-0.5],[-1,-1],[-1,-1.5],[-1,-2]])
y = np.array([1,1,1,1,1,1])



# sepal length and petal length



ppn = Perceptron(epochs=10, eta=0.1)

ppn.train(X, y)
print('Pesos: %s' % ppn.w_)
plot_decision_regions(X, y, clf=ppn)
plt.title('Perceptron')
plt.xlabel('longitud sepalo [cm]')
plt.ylabel('longitud petalo [cm]')
plt.show()

plt.plot(range(1, len(ppn.errors_)+1), ppn.errors_, marker='o')
plt.xlabel('Iteraciones')
plt.ylabel('Missclasificaciones')
plt.show()
