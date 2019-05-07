import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.evaluate import plot_decision_regions

from adaline import AdalineGD

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
# setosa and versicolor
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', -1, 1)

# sepal length and petal length
X = df.iloc[0:100, [0,2]].values

ada = AdalineGD(epochs=10, eta=0.01).train(X, y)

plt.plot(range(1, len(ada.cost_)+1), np.log10(ada.cost_), marker='o')
plt.xlabel('Iteraciones')
plt.ylabel('log(Sum-error-cuadrado)')
plt.title('Adaline - %Aprendizaje 0.01')
plt.show()

ada = AdalineGD(epochs=10, eta=0.0001).train(X, y)
plt.plot(range(1, len(ada.cost_)+1), ada.cost_, marker='o')
plt.xlabel('Iteraciones')
plt.ylabel('log(Sum-error-cuadrado)')
plt.title('Adaline - %Aprendizaje 0.0001')
plt.show()

# standardize features
X_std = np.copy(X)
X_std[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()

ada = AdalineGD(epochs=15, eta=0.01)

ada.train(X_std, y)
plot_decision_regions(X_std, y, clf=ada)
plt.title('Adaline - Gradiente Descendiente')
plt.xlabel('longitud sepalo [estandarizado]')
plt.ylabel('longitud petalo [estandarizado]')
plt.show()

plt.plot(range(1, len( ada.cost_)+1), ada.cost_, marker='o')
plt.xlabel('Iteraciones')
plt.ylabel('Sum-error-cuadrado')
plt.show()

from adaline import AdalineSGD

ada = AdalineSGD(epochs=15, eta=0.01)

# shuffle data
np.random.seed(123)
idx = np.random.permutation(len(y))
X_shuffled, y_shuffled =  X_std[idx], y[idx]

# train and adaline and plot decision regions
ada.train(X_shuffled, y_shuffled)
plot_decision_regions(X_shuffled, y_shuffled, clf=ada)
plt.title('Adaline - Gradiente Descendiente')
plt.xlabel('longitud sepalo [estandarizado]')
plt.ylabel('longitud petalo [estandarizado]')
plt.show()

plt.plot(range(1, len(ada.cost_)+1), ada.cost_, marker='o')
plt.xlabel('Iteraciones')
plt.ylabel('Sum-error-cuadrado')
plt.show()
