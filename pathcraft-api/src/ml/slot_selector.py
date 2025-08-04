import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

class SlotSelector:
    def __init__(self):
        self.model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=0)
        self._is_trained = False

    def train(self, X, y):
        """
        Train the model on the given data.
        X: Features (e.g., time of day, day of week, etc.)
        y: Target (e.g., whether the slot was productive)
        """
        self.model.fit(X, y)
        self._is_trained = True

    def predict(self, X):
        """
        Predict the best slot for the given features.
        """
        if not self._is_trained:
            raise RuntimeError("Model has not been trained yet.")
        return self.model.predict(X)

    def predict_proba(self, X):
        """
        Predict the probability of each slot being productive.
        """
        if not self._is_trained:
            raise RuntimeError("Model has not been trained yet.")
        return self.model.predict_proba(X)

def get_dummy_data():
    """
    Generate some dummy data for training the model.
    """
    # Features: time of day (0-23), day of week (0-6)
    X = np.random.randint(0, 24, size=(100, 2))
    # Target: whether the slot was productive (0 or 1)
    y = np.random.randint(0, 2, size=100)
    return X, y

if __name__ == '__main__':
    # Example usage
    selector = SlotSelector()
    X_train, y_train = get_dummy_data()
    selector.train(X_train, y_train)

    # Predict on some new data
    X_test = np.array([[10, 2], [18, 5]])
    predictions = selector.predict(X_test)
    probabilities = selector.predict_proba(X_test)

    print(f"Predictions: {predictions}")
    print(f"Probabilities: {probabilities}")
