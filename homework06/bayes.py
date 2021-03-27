from collections import defaultdict
from math import log


class NaiveBayesClassifier:
    def __init__(self, alpha: float = 1e-5):
        self.d = 0
        self.word = defaultdict(lambda: 0)  # type: ignore
        self.class_words = defaultdict(lambda: 0)  # type: ignore
        self.y = defaultdict(lambda: 0)  # type: ignore
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        for x in range(len(X)):
            self.y[y[x]] += 1
            words = X[x].split()
            for wrd in words:
                self.word[wrd] += 1
                self.class_words[wrd, y[x]] += 1

        for cl in self.y:
            self.y[cl] /= len(X)

        self.d = len(self.word)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        assert len(self.y) > 0
        return max(
            self.y.keys(),
            key=lambda cl: log(self.y[cl])
            + sum(
                log(
                    (self.class_words[wrd, cl] + self.alpha)
                    / (self.word[wrd] + self.alpha * self.d)
                )
                for wrd in X.split()
            ),
        )

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        prediction = []
        for one in X_test:
            prediction.append(self.predict(one))
        return sum(0 if prediction[k] != y_test[k] else 1 for k in range(len(X_test))) / len(X_test)
