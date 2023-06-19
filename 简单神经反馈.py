import numpy as np

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def cbow(context_words, target_word, word_index, learning_rate, W1, W2, epochs):
    for _ in range(epochs):
        # STEP 3
        # Get vector sum of context words
        v_c = np.sum([W1[word_index[word]] for word in context_words], axis=0)

        # STEP 4
        # Forward pass
        z = np.dot(W2.T, v_c)
        y_pred = softmax(z)

        # STEP 5
        # Calculate error
        E = np.subtract(y_pred, np.array([1 if word_index[word] == word_index[target_word] else 0 for word in word_index.keys()]))

        # Backpropagation
        dL_dW2 = np.outer(v_c, E)
        W2 = W2 - learning_rate * dL_dW2
        
        # Update weights for context words in W1
        for word in context_words:
            W1[word_index[word]] -= learning_rate * np.dot(E, W2.T)

    return W1, W2

words_list = ['我', '喜欢', '读书']
word_index = {word: i for i, word in enumerate(words_list)}
# Initialize word vectors
W1 = np.random.rand(len(words_list), 100)
W2 = np.random.rand(100, len(words_list))

# Training
context_words = ['我', '读书']
target_word = '喜欢'
learning_rate = 0.01
epochs = 1000
W1, W2 = cbow(context_words, target_word, word_index, learning_rate, W1, W2, epochs)
