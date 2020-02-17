from sklearn import tree
features = [[300, 1], [400, 0], [325, 1], [375, 0]]
labels = [0, 1, 0, 1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)
print(clf.predict([[315, 1]]))