from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np
import matplotlib.pyplot as plt 

# Load the digits dataset: digits
digits = load_digits()

(X_train, X_test, y_train, y_test) = train_test_split(digits.data, digits.target, test_size=0.2, random_state=42, stratify=digits.target)

ks = np.arange(2, 10)
scores = []
for k in ks:
    knn = KNeighborsClassifier(n_neighbors=k)
    score = cross_val_score(knn, X_train, y_train, cv=5)
    scores.append(np.mean(score))
 
plt.plot(ks, scores)
plt.xlabel('accuracy')
plt.ylabel('k')
plt.show()


