from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, validation_curve, learning_curve, train_test_split, ShuffleSplit
import matplotlib.pyplot as plt
import numpy as np
import os, json, pickle

def getBestParameters(X_train, y_train, X_test, y_test):
    learning_algorithm = SVC(kernel='linear', random_state = 42, verbose=False)
    search_space = [{'kernel':['linear'], 'C':np.logspace(-3,3,7)},
                    {'kernel':['rbf'], 'C':np.logspace(-3,3,7), 'gamma':np.logspace(-3,2,6)}]
    gridsearch = GridSearchCV(learning_algorithm, param_grid=search_space, refit = True, n_jobs=-1, cv= 10, verbose=10)
    gridsearch.fit(X_train, y_train)
    print('Best parameter: %s' %str(gridsearch.best_params_))
    cv_performance = gridsearch.best_score_
    test_performance = gridsearch.score(X_test, y_test)
    print('Cross-validation accuracy score: %0.3f,' 'test accuracy score: %0.3f' %(cv_performance, test_performance))
    return None;

def graphLearning(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

def graph(save):
    data_path = os.path.dirname(os.path.realpath(__file__))+"\\Docs\\startingDataset.json"
    with open(data_path) as f:
        data = json.load(f)
    X = data["Data"]
    y = data["Target"]
    #X_train, X_test, y_train, y_test =train_test_split(X, y, test_size =.2, random_state=42)
    space = [i*25 for i in range(1,5)]
    Rf = RandomForestClassifier(oob_score=True, n_jobs=-1)
    train_scores, valid_scores = validation_curve(Rf,X,y,"n_estimators", space, cv=5)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(valid_scores, axis=1)
    test_scores_std = np.std(valid_scores, axis=1)

    plt.title("Validation Curve with Random Forest Classifier")
    plt.xlabel("n_estimators")
    plt.ylabel("Score")
    plt.ylim(0.0, 1.1)
    plt.xlim(25,100)
    plt.grid(True)
    lw = 2
    plt.semilogx(space, train_scores_mean, label="Training score",
                 color="darkorange", lw=lw)
    plt.fill_between(space, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.2,
                     color="darkorange", lw=lw)
    plt.semilogx(space, test_scores_mean, label="Cross-validation score",
                 color="navy", lw=lw)
    plt.fill_between(space, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.2,
                     color="navy", lw=lw)
    plt.legend(loc="best")
    if(save):
        plt.savefig("Validation Curve")
    plt.show()

    title = "Learning Curves with RandomForest"
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)

    graphLearning(Rf, title, X, y, ylim=(0.0, 1.01), cv=cv, n_jobs=-1)
    if(save):
        plt.savefig("Learning Curve")
    plt.show()
    return None;

def trainModel(saveIt):
    model_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.dirname(os.path.realpath(__file__))+"\\Docs\\startingDataset.json"
    with open(data_path) as f:
        data = json.load(f)
    X = data["Data"]
    y = data["Target"]
    X_train, X_test, y_train, y_test =train_test_split(X, y, test_size =.2)
    Rf_model = RandomForestClassifier(n_estimators=25, bootstrap=True, oob_score=True, n_jobs=-1, random_state = 42)
    Rf_model.fit(X_train, y_train)
    print(Rf_model.oob_score_)
    print(accuracy_score(y_test,Rf_model.predict(X_test)))
    print(accuracy_score(y, Rf_model.predict(X)))
    Essay_probabilities = Rf_model.predict_proba(X)
    predicted = Rf_model.predict(X)
    if(saveIt):
        pickle.dump(Rf_model, open("model.pickle",'wb'))
    for i in range(len(predicted)):
        if(y[i]!=predicted[i]):
            print("Incorrectly predicted "+str(predicted[i]) + " with a confidence of " + str(Essay_probabilities[i]))

    print(Rf_model.feature_importances_)
    '''
    getBestParameters(X_train, y_train, X_test, y_test)
    input()
    clf = SVC(kernel='linear', C=0.001)
    clf.fit(X_train, y_train)

    print(accuracy_score(y_train, clf.predict(X_train)))
    print(accuracy_score(y_test, clf.predict(X_test)))
    predicted = clf.predict(X)
    print(accuracy_score(y, predicted))
    print("\n")
    '''
    return None;
