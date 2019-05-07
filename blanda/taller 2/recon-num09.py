#Ruben Dario Acuña O
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm
from sklearn import metrics

digits = datasets.load_digits()

images_and_labels = list(zip(digits.images, digits.target))

n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

classifier = svm.SVC(gamma=0.001)

classifier.fit(data[:n_samples / 2], digits.target[:n_samples / 2])

expected = digits.target[n_samples / 2:]
predicted = classifier.predict(data[n_samples / 2:])

print("reconocimento de los numeros %s:\n%s\n" 
      % (classifier, metrics.classification_report(expected, predicted)))
print("precision de la red:\n%s" % metrics.confusion_matrix(expected, predicted))


for index, (image, label) in enumerate(images_and_labels[:10]):
    plt.subplot(2, 5, index + 1 )
    plt.axis('on')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('numero : %i' % label)
	plt.show()
