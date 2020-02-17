# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '..\\..\AppData\Local\Temp'))
	print(os.getcwd())
except:
	pass
#%%
import random
import pandas as pd


#%%
def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.moreless(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)

class Decision_Node:
    def __init__(self,question,true_branch,false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

def build_tree(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(question, true_branch, false_branch)

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

def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

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

def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)

def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return
    print(spacing + str(node.question))
    print(spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")
    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")

def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


#%%
def createvalues():
    values=[]
    template=[{"label":"Klassrum","minheat":23,"maxheat":26,"minhum":27,"maxhum":37,"minco2":600,"maxco2":1200,"minlux":150,"maxlux":250},{"label":"Fikarum","minheat":25,"maxheat":28,"minhum":37,"maxhum":44,"minco2":0,"maxco2":0,"minlux":300,"maxlux":550}]
    for roomtype in template:
        amount = random.randint(5,11)
        for i in range(0,amount):
            newtemp=random.uniform(roomtype["minheat"], roomtype["maxheat"])
            newhum=random.uniform(roomtype["minhum"], roomtype["maxhum"])
            newco2=random.uniform(roomtype["minco2"], roomtype["maxco2"])
            newlux=random.uniform(roomtype["minlux"], roomtype["maxlux"])
            values.append([newtemp, newhum, newco2, newlux, roomtype["label"]])
    return values


#%%
newvalues = pd.DataFrame(createvalues())
print(newvalues)


#%%
import requests

urls = ["https://car9o7qv7j.execute-api.us-east-1.amazonaws.com/iot/device?MAC=84:F3:EB:B4:6F:61","https://nkclsbr32f.execute-api.us-east-1.amazonaws.com/beta/device?MAC=DC:4F:22:5F:43:75"]
Simon = pd.DataFrame()
BBB = pd.DataFrame()

info = requests.get(urls[0]).json()
for k in info['data']:            
    if k['CO2'] < 5000:
        k["time"]="Klassrum"
        Simon = Simon.append(k, ignore_index=True)

info = requests.get(urls[1]).json()
for k in info['data']:
    if k['CO2'] < 5000:
        k["time"]="Fikarum"
        Simon = Simon.append(k, ignore_index=True)

newvalues = Simon
newvalues.columns  = ["CO2", "Hum", "LDR", "Temp", "Rum"]
testing_data = createvalues()
print(newvalues)


#%%
def splitdata(inputdata, n_trees, ownvalue):
    subsets=[]
    splitone=inputdata.sample(frac=0.5, random_state=200)
    splittwo=inputdata.drop(splitone.index)
    if n_trees != 1:
        feedback=splitdata(splitone, n_trees-1, ownvalue+"a")
        feedback2=splitdata(splittwo, n_trees-1, ownvalue+"b")
        for i in range(0,len(feedback)):
            subsets.append(feedback[i])
            subsets.append(feedback2[i])
    else:
        return [splitone,splittwo]
    return subsets


#%%
subsets=splitdata(newvalues,3,"a") # fler än 1
print("antalsubsets", len(subsets))
print("antalvärden", len(subsets[0]))
print(subsets[0])


#%%
forrest=[]
i=1
header = ["CO2", "Hum", "LDR", "Temp", "Rum"]

for sets in subsets:
    if i == 1:
        testing_data = sets.tail(5).values.tolist() # no work
    lists = sets.values.tolist()
    i+=1
    tree = build_tree(lists)
    forrest.append(tree)
    print_tree(tree)


#%%
def predictioncounter(row,trees,labels):
    length=len(labels)
    predictions=[0 for i in range(length)]
    for tree in trees:
        prediction=classify(row,tree)
        for i in range(length):
            if(prediction.get(labels[i]) is not None):
                predictions[i]+=1
        print("Actual: %s. Predicted: %s" %(row[-1], print_leaf(classify(row, tree))))
    return predictions


#%%
def randomforest(trees, data):
    labels=["Fikarum","Klassrum"]
    for row in data:
        predictions=predictioncounter(row,trees,labels)
        high=max(predictions)
        print("Ratio:",high,"/",len(trees))


#%%
randomforest(forrest,testing_data)


#%%


