training_data = [[54.4, 14.4, 'Kylrum'],[45.4, 12.4, 'Kylrum'],[89.4, 19.5, 'Klassrum'],[57.4, 18.1, 'Lärarrum'],[22.4, 8.6, 'Kylrum'],[24.4, 11.24, 'Kylrum'],[84.4, 24.4,'Klassrum'],[95.4, 22.4, 'Klassrum'],[81.4, 20.1, 'Lärarrum'],[70, 19.7, 'Lärarrum']]

# training_data.append([70, 19.8,'Klassrum'])

testing_data = [[30, 15.6, 'Kylrum'],[50, 16, 'Klassrum'],[89, 21, 'Klassrum'],[81.7, 19,'Lärarrum'],[87, 19.8, 'Lärarrum']]
header = ["Fukt", "Temp", "Rum"]

class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def moreless(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val <= self.value

    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))

class Decision_Node:
    def __init__(self,question,true_branch,false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
        
class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)
        
def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)
        
def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts
        
def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.moreless(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)

def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.moreless(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)

def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity
    
def find_best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1
    for col in range(n_features): 
        values = set([row[col] for row in rows])
        for val in values: 
            question = Question(col, val)
            true_rows, false_rows = partition(rows, question)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue
            gain = info_gain(true_rows, false_rows, current_uncertainty)
            if gain >= best_gain:
                best_gain, best_question = gain, question
    return best_gain, best_question
    
def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs

def build_tree(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(question, true_branch, false_branch)

def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return
    print(spacing + str(node.question))
    print(spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")
    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")
    
my_tree = build_tree(training_data)
print_tree(my_tree)

for row in testing_data:
    print("Actual: %s. Predicted: %s" % (row[-1], print_leaf(classify(row, my_tree))))