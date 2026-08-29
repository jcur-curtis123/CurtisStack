import numpy as np

def initialize_parameters(layer_sizes):
    """
    layer_sizes: list like [2, 4, 1] meaning
    2 inputs -> 4 hidden neurons -> 1 output
    Returns a dict of W1, b1, W2, b2, ... randomly initialized.
    """
    random_int = np.random.RandomState(42)  
    params = {}
    layers = len(layer_sizes)
    for i in range(1, layers):
        params[f'W{i}'] = random_int.randn(layer_sizes[i], layer_sizes[i-1]) * 0.01
        params[f'b{i}'] = np.zeros((layer_sizes[i], 1)) 
    print(params)
    
    return params
  
def sigmoid(z):

    """Activation function: squashes z into (0,1)."""

    sigmoid = 1 / (1 + np.exp(-z))
    return sigmoid

def sigmoid_derivative(a):

    """f'(z) expressed in terms of a = sigmoid(z)."""

    a = sigmoid(a)
    return a * (1 - a)      

def forward_pass(X, params):

    """
    Compute z and a for every layer, given input X.
    Return a dict, in this case, the cache of all z's and a's — you'll need
    them again in the backward pass.
    """

    cache = {'a0': X}
    a_prev = X
    ...

    for i in range(1, len(params) // 2 + 1):
        W = params[f'W{i}']
        b = params[f'b{i}']
        z = np.dot(W, a_prev) + b
        a = sigmoid(z)
        cache[f'z{i}'] = z
        cache[f'a{i}'] = a
        a_prev = a
    return cache

def compute_loss(a_final, y):

    """Mean squared error (or cross-entropy) between prediction and truth."""

    mse = np.mean((a_final - y) ** 2)
    return mse 



def backward_pass(cache, params, y):

    """
    Walk backward through the cache from forward_pass.
    Compute delta at output layer, then propagate delta
    backward layer by layer, computing dW and db at each step.
    Return a dict of gradients: dW1, db1, dW2, db2, ...
    """

    grads = {}
    m = y.shape[1]  # number of examples

    # Compute delta at output layer
    delta = cache[f'a{len(params)//2}'] - y

    # Propagate delta backward layer by layer
    for i in reversed(range(1, len(params) // 2 + 1)):
        W = params[f'W{i}']
        a_prev = cache[f'a{i-1}'] 
        z = cache[f'z{i}']

        # Compute gradients for current layer
        dW = (1/m) * np.dot(delta, a_prev.T)
        db = (1/m) * np.sum(delta, axis=1, keepdims=True)

        grads[f'W{i}'] = dW
        grads[f'b{i}'] = db

        # Compute delta for previous layer
        if i > 1:
            delta = np.dot(W.T, delta) * sigmoid_derivative(z)

    return grads

def update_parameters(params, grads, learning_rate):

    """
    params[key] -= learning_rate * grads[key] for every weight/bias.
    """

    for key in params:
        params[key] -= learning_rate * grads[key]                   

def train(X, y, layer_sizes, epochs, learning_rate, batch_size=None):

    """
    Main loop:
    1. initialize_parameters
    2. for each epoch (and each mini-batch if batch_size is set):
        - forward_pass
        - compute_loss
        - backward_pass
        - update_parameters
    3. print loss occasionally
    Return trained params.
    """

    params = initialize_parameters(layer_sizes)
    for epoch in range(epochs):
        # Forward pass
        cache = forward_pass(X, params)
        # Compute loss
        loss = compute_loss(cache[f'a{len(params)//2}'], y)
        # Backward pass
        grads = backward_pass(cache, params, y)
        # Update parameters
        update_parameters(params, grads, learning_rate)
        # Print loss 
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss}")

    return params

def predict(X, params):

    """Run forward_pass and return just the final activation."""

    forward_cache = forward_pass(X, params)
    a_final = forward_cache[f'a{len(params)//2}']

    return a_final

if __name__ == "__main__":

    np.random.seed(1)

    n_samples = 200
    X = np.random.uniform(-1, 1, (2, n_samples))   # 2 features, 200 examples (columns)

    # label = 1 if point falls inside a circle of radius 0.6, else 0
    distances = np.sqrt(X[0, :] ** 2 + X[1, :] ** 2)
    y = (distances < 0.6).astype(int).reshape(1, n_samples)


    trained_params = train(
        X, y,
        # bigger hidden layer for a harder boundary
        layer_sizes=[2, 8, 1],   
        epochs=5000,
        learning_rate=0.5,
        batch_size=None
    )

    print("\nSample predictions:")
    preds = predict(X, trained_params)
    correct = (np.round(preds) == y).sum()
    print(f"Accuracy: {correct}/{n_samples} = {correct/n_samples:.2%}")

    for i in range(5):  # just print first 5 to sanity check
        print(f"point={X[:, i].round(2)}  predicted={preds[0,i]:.3f}  actual={y[0,i]}")