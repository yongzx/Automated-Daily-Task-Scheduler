import numpy as np
from Task import Task

X = np.array([])
y = np.array([])

def generate_training_set(slots, satisfaction):
    global X
    global y

    # variety score
    distinct_task = set()
    var_score = 0
    for slot in slots:
        if isinstance(slot.act, Task):
            distinct_task.add(slot.act)
            var_score += 1

    # priority score, to ensure the schedule still focuses on getting the highly prioritized things done
    prio_score = 0
    for slot in slots:
        if isinstance(slot.act, Task):
            prio_score += slot.act.get_priority()

    # deadline score
    deadline_score = 0
    for slot in slots:
        if isinstance(slot.act, Task):
            deadline_score += (slot.act.get_deadline() - datetime.now().date()).days

    # continuous score
    cont_score = 0
    for i in range(1, len(slots)):
        if isinstance(slots[i].act, Task) and isinstance(slots[i - 1].act, Task) and slots[i] == slots[i - 1]:
            cont_score += 1

    var_score = 1 / var_score
    prio_score = 1 / prio_score
    deadline_score = 1 / deadline_score
    cont_score = 1 / cont_score

    if not X:
        X = np.array([[var_score, prio_score, deadline_score, cont_score]])
    else:
        X = np.concatenate((X, np.array([[var_score, prio_score, deadline_score, cont_score]])))

    if not Y:
        y = np.array([satisfaction])
    else:
        y = np.append(y, np.array([satisfaction]))


num_examples = len(X)  # training set size
ann_input_dim = 4  # input layer dimensionality
ann_output_dim = 2  # output layer dimensionality
EPSILON = 0.01  # learning rate for gradient descent
REG_LAMBDA = 0.01  # regularization strength

def generate_scores(slots):
    # variety score
    distinct_task = set()
    var_score = 0
    for slot in slots:
        if isinstance(slot.act, Task):
            distinct_task.add(slot.act)
            var_score += 1

    # priority score, to ensure the schedule still focuses on getting the highly prioritized things done
    prio_score = 0
    for slot in slots:
        if isinstance(slot.act, Task):
            prio_score += slot.act.get_priority()

    # deadline score
    deadline_score = 0
    for slot in slots:
        if isinstance(slot.act, Task):
            deadline_score += (slot.act.get_deadline() - datetime.now().date()).days

    # continuous score
    cont_score = 0
    for i in range(1, len(slots)):
        if isinstance(slots[i].act, Task) and isinstance(slots[i - 1].act, Task) and slots[i] == slots[i - 1]:
            cont_score += 1

    var_score = 1 / var_score
    prio_score = 1 / prio_score
    deadline_score = 1 / deadline_score
    cont_score = 1 / cont_score

    return np.array([var_score, prio_score, deadline_score, cont_score])

# Helper function to predict an output (0 or 1)
def predict(x):
    """
    :param model: parameters of neural network (w1, c1, w2, c2)
    w1 is the weight of the synapse from input layer to hidden layer.
    w2 is the weight of the synapse from hidden layer to output layer.
    c1 is the constant for the synapse from input layer to hidden layer.
    c2 is the constant for the synapse from hidden layer to output layer
    :param x: tuple (variability score, priority score, continuity score)
    :return: 0 or 1 - 0 if unsatisfactory, 1 if satisfactory
    """
    if len(x)>100:
        model = build_model(ann_hidden_dim=3)
        w1, c1, w2, c2 = model['w1'], model['c1'], model['w2'], model['c2']
        # Forward propagation
        z1 = x.dot(w1) + c1
        a1 = np.tanh(z1)
        z2 = a1.dot(w2) + c2
        exp_scores = np.exp(z2)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        return np.argmax(probs, axis=1)

def build_model(ann_hidden_dim, num_passes=20000):
    """
    :param ann_hidden_dim: Number of nodes in the hidden layer
    :param num_passes: Number of passes through the training data for gradient descent
    :return: returns the parameters of artificial neural network for prediction using forward propagation of the parameters
    """
    model = {}
    global X

    # Initialize the parameters to random values.
    np.random.seed(0)
    w1 = np.random.randn(ann_input_dim, ann_hidden_dim) / np.sqrt(ann_input_dim)
    c1 = np.zeros((1, ann_hidden_dim))
    w2 = np.random.randn(ann_hidden_dim, ann_output_dim) / np.sqrt(ann_hidden_dim)
    c2 = np.zeros((1, ann_output_dim))

    # Batch gradient descent
    for i in range(0, num_passes):
        # Forward propagation
        z1 = X.dot(w1) + c1
        a1 = np.tanh(z1)
        z2 = a1.dot(w2) + c2
        exp_scores = np.exp(z2)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

        # Back propagation
        delta3 = probs
        delta3[range(num_examples), y] -= 1
        dw2 = (a1.T).dot(delta3)
        dc2 = np.sum(delta3, axis=0, keepdims=True)
        delta2 = delta3.dot(w2.T) * (1 - np.power(a1, 2))
        dw1 = np.dot(X.T, delta2)
        dc1 = np.sum(delta2, axis=0)

        # Add regularization terms (c1 and c2 don't have regularization terms)
        dw2 += REG_LAMBDA * w2
        dw1 += REG_LAMBDA * w1

        # Gradient descent parameter update
        w1 += -EPSILON * dw1
        c1 += -EPSILON * dc1
        w2 += -EPSILON * dw2
        c2 += -EPSILON * dc2

        # Assign new parameters to the model
        model = {'w1': w1, 'c1': c1, 'w2': w2, 'c2': c2}

    return model
