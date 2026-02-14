import numpy as np  

X = np.random.randint(low=0, high=100, size=30)
Y = (0.6*X + 21) * np.random.random(size=len(X))

print(X[:5])
print()
print(Y[:5])