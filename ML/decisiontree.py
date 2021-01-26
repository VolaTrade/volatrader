# Toy dataset.
# Format: each row is an example.
# The last column is the label.
# The first two columns are features.
# Feel free to play with it by adding more features & examples.
# Interesting note: I've written this so the 2nd and 5th examples
# have the same features, but different labels - so we can see how the
# tree handles this case.
training_data = [ #Numbers TQQQ Daily
    [1.976, 1.896, 0.08, 65.61, 71.99, 73.71, 'down'],
    [1.913, 1.900, 0.013, 63.76, 64.59, 71.59, 'up'],
    [1.923, 1.904, 0.018, 66.96, 68.79, 68.46, 'up'],
    [1.909, 1.905, 0.004, 66.99, 66.78, 68.72, 'up'],
    [1.887, 1.902, -0.014, 67.41, 73.38, 69.65, 'down'],
    [1.777, 1.877, -0.100, 61.51, 54.79, 64.98, 'down'],
    [1.521, 1.805, -0.285, 51.44, 37.76, 55.31, "down"],
    [2.582, 2.480, .0102, 70.61, 83.07, 82.19, "up"],
    [1.105, 2.035, -0.931, 43.70, 24.14, 41.20, "up"],
    [-3.064, -2.025, -1.038, 26.74, 15.17, 16.74, "up"],
    [2.073, 2.125, -0.051, 60.83, 72.91, 79.81, "down"],
    [-1.157, 0.437, -1.594, 37.79, 21.06, 16.24, "up"],
    [-1.424, -1.292, -.132, 44.7, 39.9, 59.19, "down"],
    [1.685, 2.021, -0.335, 58.59, 73.77, 60.34, "down"],
    [1.607, 1.938, -0.331, 57.93, 74.35, 70.68, "up"],
    [-4.404, -7.729, 3.325, 50.99, 90.80, 84.82, "up"],
    [4.427, 3.995, 0.433, 61.17, 56.89, 72.34, "up"],
    [4.448, 4.085, 0.363, 62.35, 54.09, 62.70, "down"],
    [1.864, 1.449, 0.415, 60.48, 74.13, 82.15, "down"],
    [1.845, 1.557, 0.288, 62.35, 82.13, 67.78, "up"],
    [2.930, 2.408, 0.522, 76.57, 86.66, 92.07, "down"],
    [1.504, 1.367, 0.138, 70.64, 67.14, 76.76, "down"],
    [.492, .231, .26, 65.27, 82.34, 84.78, "down"],
    [-.163, -.217, .054, 52.50, 87.88, 87.28, "up"],
    [.445, .68, -.234, 58.63, 59.33, 33.63, "up"],
    [1.167, 1.025, .142, 71.70, 68.49, 76.40, "down"],
    [-.429, -.461, .032, 40.58, 23.02, 22.58, "down"],
    [-.831, -.227, -.604, 20.38, 10.31, 19.94, "down"],
    [-.348, -.173, -.175, 35.79, 32.60, 45.20, "up"],
    [.761, .667, .094, 78.35, 92.81, 90.60, "down"],
    [.401, .417, -.016, 64.58, 51.23, 55.02, "down"],
    [.175, .255, -.080, 45.22, 15.63, 31.24, "down"],
    [1.661, -.239, 1.9, 56.73, 72.26, 56.46, "down"],
    [1.659, 0.141, 1.519, 52.89, 66.28, 66.20, "up"],
    [-5.37, -8.56, 3.19, 49.47, 80.96, 74.14, "up"],
    
     
]
'''
training_data = [
    [108.42, 16.416, 6.66, 6.48, "down"],
    [107.02, 17.409, 6.81, 6.54, "up"],
    [110.88, 19.223, 7.10, 6.64, 70.74, "up"],
    [110.96, 21.019, 7.31, 6.76, 70.81, "up"],
    [114.21, 23.246, 7.62, 6.92, 73.72, "down"],
    [113.77, 24.549, 7.81, 7.08, 72.67, "up"],
    [114.54, 26.026, 7.97, 7.24, 73.38, "up"],
    [114.74, 27.302, 8.06, 7.39, 73.58, "up"],
    [118.06, 29.112, 8.27, 7.55, 76.63, "down"],
    [114.70, 29.681, 8.23, 7.67, 68.06, "down"],
    [108.14, 29.405, 7.82, 7.70, 55.11, "down"],
    [95.68, 30.110, 6.78, 7.53, 39.67, "down"],
    [87.94, 31.886, 5.39, 7.14, 33.41, "up"],
    [89.15, 34.139, 4.25, 6.62, 35.13, "down"],
    [75.82, 42.031, 2.42, 5.85, 26.87, "up"],
    [77.00, 48.154, .93, 4.96, 28.48, "up"],
    [87.51, 49.476, .44, 4.14, 40.90, "down"],
    [79.27, 53.750, -.51, 3.29, 35.67, "up"],
    [88.89, 55.240, -.62, 2.58, 44.58, "down"],
    [81.09, 58.370, -1.21, 1.89, 39.77, "down"],
    [76.84, 62.094, -2.01, 1.18, 37.40, "down"],
    [76.84, 62.094, -2.01, 1.18, 37.40, "down"],
    [61.23, 71.260, -3.83, .27, 30.27, "up"],
]'''

# Column labels.
# These are used only to print the tree.

header = ["MACDblack", "MACDred", "MACDblue", "RSI", "SSblack", "SSred", "label"]
#header = ["DMA", "BBW", "PMOblack", "PMOred", "RSI", "label"]


def unique_vals(rows, col):
    """Find the unique values for a column in a dataset."""
    return set([row[col] for row in rows])

#######
# Demo:
# unique_vals(training_data, 0)
# unique_vals(training_data, 1)
#######


def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

#######
# Demo:
# class_counts(training_data)
#######


def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)

#######
# Demo:
# is_numeric(7)
# is_numeric("Red")
#######


class Question:
    """A Question is used to partition a dataset.
    This class just records a 'column number' (e.g., 0 for Color) and a
    'column value' (e.g., Green). The 'match' method is used to compare
    the feature value in an example to the feature value stored in the
    question. See the demo below.
    """

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))

#######
# Demo:
# Let's write a question for a numeric attribute
# Question(1, 3)
# How about one for a categorical attribute
# q = Question(0, 'Green')
# Let's pick an example from the training set...
# example = training_data[0]
# ... and see if it matches the question
# q.match(example)
#######


def partition(rows, question):
    """Partitions a dataset.
    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


#######
# Demo:
# Let's partition the training data based on whether rows are Red.
# true_rows, false_rows = partition(training_data, Question(0, 'Red'))
# This will contain all the 'Red' rows.
# true_rows
# This will contain everything else.
# false_rows
#######

def gini(rows):
    """Calculate the Gini Impurity for a list of rows.
    There are a few different ways to do this, I thought this one was
    the most concise. See:
    https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
    """
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity


#######
# Demo:
# Let's look at some example to understand how Gini Impurity works.
#
# First, we'll look at a dataset with no mixing.
# no_mixing = [['Apple'],
#              ['Apple']]
# this will return 0
# gini(no_mixing)
#
# Now, we'll look at dataset with a 50:50 apples:oranges ratio
# some_mixing = [['Apple'],
#               ['Orange']]
# this will return 0.5 - meaning, there's a 50% chance of misclassifying
# a random example we draw from the dataset.
# gini(some_mixing)
#
# Now, we'll look at a dataset with many different labels
# lots_of_mixing = [['Apple'],
#                  ['Orange'],
#                  ['Grape'],
#                  ['Grapefruit'],
#                  ['Blueberry']]
# This will return 0.8
# gini(lots_of_mixing)
#######

def info_gain(left, right, current_uncertainty):
    """Information Gain.
    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

#######
# Demo:
# Calculate the uncertainy of our training data.
# current_uncertainty = gini(training_data)
#
# How much information do we gain by partioning on 'Green'?
# true_rows, false_rows = partition(training_data, Question(0, 'Green'))
# info_gain(true_rows, false_rows, current_uncertainty)
#
# What about if we partioned on 'Red' instead?
# true_rows, false_rows = partition(training_data, Question(0,'Red'))
# info_gain(true_rows, false_rows, current_uncertainty)
#
# It looks like we learned more using 'Red' (0.37), than 'Green' (0.14).
# Why? Look at the different splits that result, and see which one
# looks more 'unmixed' to you.
# true_rows, false_rows = partition(training_data, Question(0,'Red'))
#
# Here, the true_rows contain only 'Grapes'.
# true_rows
#
# And the false rows contain two types of fruit. Not too bad.
# false_rows
#
# On the other hand, partitioning by Green doesn't help so much.
# true_rows, false_rows = partition(training_data, Question(0,'Green'))
#
# We've isolated one apple in the true rows.
# true_rows
#
# But, the false-rows are badly mixed up.
# false_rows
#######


def find_best_split(rows):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
    best_gain = 0  # keep track of the best information gain
    best_question = None  # keep track of the feature / value that produced it
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  # number of columns

    for col in range(n_features):  # for each feature

        values = set([row[col] for row in rows])  # unique values in the column

        for val in values:  # for each value

            question = Question(col, val)

            # try splitting the dataset
            true_rows, false_rows = partition(rows, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy dataset.
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question

#######
# Demo:
# Find the best question to ask first for our toy dataset.
# best_gain, best_question = find_best_split(training_data)
# FYI: is color == Red is just as good. See the note in the code above
# where I used '>='.
#######

class Leaf:
    """A Leaf node classifies data.
    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training data that reach this leaf.
    """

    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    """A Decision Node asks a question.
    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    """Builds the tree.
    Rules of recursion: 1) Believe that it works. 2) Start by checking
    for the base case (no further information gain). 3) Prepare for
    giant stack traces.
    """

    # Try partitioing the dataset on each of the unique attribute,
    # calculate the information gain,
    # and return the question that produces the highest gain.
    gain, question = find_best_split(rows)

    # Base case: no further info gain
    # Since we can ask no further questions,
    # we'll return a leaf.
    if gain == 0:
        return Leaf(rows)

    # If we reach here, we have found a useful feature / value
    # to partition on.
    true_rows, false_rows = partition(rows, question)

    
    #added pruning, 
    '''Should use machine learning to optimize pruning'''
    #Pre-Pruning
    if (gini(rows) <= 1/2 * gini(true_rows) + 1/2 * gini(false_rows)):
        return Leaf(rows)
    
    # Recursively build the true branch.
    true_branch = build_tree(true_rows)

    # Recursively build the false branch.
    false_branch = build_tree(false_rows)

    # Return a Question node.
    # This records the best feature / value to ask at this point,
    # as well as the branches to follow
    # dependingo on the answer.
    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):
    """World's most elegant tree printing function."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    print (spacing + str(node.question))

    # Call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
    """See the 'rules of recursion' above."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


#######
# Demo:
# The tree predicts the 1st row of our
# training data is an apple with confidence 1.
# my_tree = build_tree(training_data)
# classify(training_data[0], my_tree)
#######

def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


#######
# Demo:
# Printing that a bit nicer
# print_leaf(classify(training_data[0], my_tree))
#######

#######
# Demo:
# On the second example, the confidence is lower
# print_leaf(classify(training_data[1], my_tree))
#######

if __name__ == '__main__':

    my_tree = build_tree(training_data)

    print_tree(my_tree)
    correct = 0
    total = 0

    # Evaluate
    testing_data = [ #TQQQ numbers Daily
        [-4.456, -1.327, -3.129, 44.58, 65.90, 47.76, "down"],
        [3.741, 3.293, 0.447, 61.61, 64.52, 47.34, "down"],
        [-10.876, -6.468, -4.408, 28.31, 15.11, 17.14, "up"],
        [6.301, 5.448, 0.853, 76.63, 90.34, 90.6, "down"],
        [4.144, 3.753, 0.391, 73.73, 85.55, 85.87, "up"],
        [3.123, 2.520, 0.604, 77.83, 93.23, 92.74, "up"],
        [.505, .674, -.170, 48.99, 33.88, 37.73, "up"],
        [1.047, 0.440, 0.607, 58.75, 85.30, 68.13, "up"],
        [1.794, 1.962, -.168, 61.22, 40.56, 31.18, "up"],
        [2.570, 2313, 0.258, 68.93, 85.89, 87.04, "up"],
        [2.620, 2.374, 0.246, 71.20, 87.92, 87.80, "down"],
        [2.592, 2.418, 0.174, 68.64, 77.51, 83.77, "up"],
        [2.601, 2.454, 0.146, 70.49, 85.99, 83.80, "up"],
        [-1.030, -.019, -1.011, 38.47, 52.15, 58.60, "up"],
        [-1.140, -0.243, -0.897, 42.87, 36.18, 52.03, "down"],
        [-1.273, -0.449, -0.824, 41.44, 23.98, 37.44, "down"],
        [-1.576, -0.674, -0.902, 36.74, 23.95, 28.04, "down"],
        [2.451, 2.273, 0.178, 61.08, 57.79, 78.80, "up"],
        [2.351, 2.288, 0.063, 61.82, 42.36, 62.06, "down"],
        [2.116, 2.254, -0.138, 55.43, 24.91, 41.69, "up"],
        [2.031, 2.209, -0.178, 59.69, 36.92, 34.73, "up"],
        [-.797, .835, -1.632, 35.59, 15.27, 15.42, "up"],
        [-1.118, .126, -1.244, 46.77, 46.96, 27.77, "down"],
        [-1.221, -.144, -1.078, 43.54, 65.02, 44.35, "down"],  
        
        #old data ^
        [4.374, 4.143, 0.231, 61.43, 54.68, 55.22, "down"],
        [.862, .782, .080, 51.22, 35.32, 45.62, "down"],
        [.558, .737, -.179, 44.48, 16.47, 32.60, "up"],
        [.470, .684, -.214, 49.98, 27.21, 26.33, "down"],
    ]
    '''testing_data =[
        
        [70.76, 74.845, -4.47, -.59, 38.04, "down"]
    ]'''

    for row in testing_data:
        print ("Actual: %s. Predicted: %s" %
               (row[-1], print_leaf(classify(row, my_tree))))

        directory = classify(row, my_tree)
        max_int = 0
        max_lbl = ""
        for lbl in directory:
            x = directory[lbl]
            if x > max_int:
                max_int = x
                max_lbl = lbl
            elif x == max_int:
                max_lbl = ""
        if (row[-1] == max_lbl):
            correct += 1
            total += 1
        else:
            total += 1
    
    print("Accuracy: %d%%" % (correct/total *100))

# Next steps
# - add support for missing (or unseen) attributes
# - prune the tree to prevent overfitting
# - add support for regression

