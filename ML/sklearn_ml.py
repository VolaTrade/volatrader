import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text

#An array X, sparse or dense, of size [n_samples, n_features] holding the training samples.
#An array Y of integer values, size [n_samples], holding the class labels for the training samples.
#An array features of string values to label the X features and samples
#An array predictions, sparse or dense, of size [n_samples, n_features] holding the testing samples.
def DecisionTree(X, y, features, predictions): 
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    clf = DecisionTreeClassifier(random_state=0)
    path = clf.cost_complexity_pruning_path(X_train, y_train)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities
    clfs = []
    for ccp_alpha in ccp_alphas:
        clf = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
        clf.fit(X_train, y_train)
        clfs.append(clf)

    train_scores = [clf.score(X_train, y_train) for clf in clfs]
    test_scores = [clf.score(X_test, y_test) for clf in clfs]

    fig, ax = plt.subplots()
    ax.set_xlabel("alpha")
    ax.set_ylabel("accuracy")
    ax.set_title("Accuracy vs alpha for training and testing sets")
    ax.plot(ccp_alphas, train_scores, marker='o', label="train",
            drawstyle="steps-post")
    ax.plot(ccp_alphas, test_scores, marker='o', label="test",
            drawstyle="steps-post")
    ax.legend()
    plt.show() #graphic for alpha vs accuracy

    max_index = 0
    i = 0
    max_score = 0
    for score in test_scores:
        if score > max_score:
            max_score = score
            max_index = i
        i += 1

    clf_cur = clfs[max_index]
    r = export_text(clf_cur, feature_names=features)
    print(r) #prints the tree
    return clf_cur.predict(predictions)
    