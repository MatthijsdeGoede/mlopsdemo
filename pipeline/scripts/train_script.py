
import os
import numpy as np
import pandas as pd
import joblib
import argparse

from sklearn.linear_model import LogisticRegression
from azureml.core import Run


def main(args):
    # Workspace and Run configuration
    run = Run.get_context()   
    
    x_train, y_train, x_test, y_test = get_data(args)
    print(f'Training set dimension: {x_train.shape, y_train.shape}, Test set dimension: {x_test.shape, y_test.shape}')

    reg = 0.5
    print('Train a logistic regression model with regularization rate of', reg)
    clf = LogisticRegression(C=1.0/reg, solver="liblinear", multi_class="auto", random_state=42)
    clf.fit(x_train, y_train)

    print('Predict the test set')
    y_hat = clf.predict(x_test)

    # calculate accuracy on the prediction
    acc = np.average(y_hat == y_test)
    print('Accuracy is', acc)

    run.log('regularization rate', np.float(reg))
    run.log('accuracy', np.float(acc))

    os.makedirs('outputs', exist_ok=True)
    # note file saved in the outputs folder is automatically uploaded into experiment record
    joblib.dump(value=clf, filename='outputs/sklearn_mnist_model.pkl')


def get_data(args):            
        # Copying the placeholder blobs over to a newly created directory for this run
        train_df = pd.read_csv(args.train_blob)
        test_df = pd.read_csv(args.test_blob)
        return preprocess_data(train_df, test_df)


def preprocess_data(train_df, test_df):
    # Data preparation: Separate labels from features, and normalize features on the fly
    x_train = train_df.iloc[:, 1:] / 255
    y_train = train_df.loc[:,"label"]
    x_test = test_df.iloc[:, 1:] / 255
    y_test = test_df.loc[:, "label"]
    return x_train, y_train, x_test, y_test


def parse_args():
    # parsing the arguments provided by the pipeline
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_blob", type=str)
    parser.add_argument("--test_blob", type=str)
    return parser.parse_args()


# run script
if __name__ == "__main__":
    # parse args
    args = parse_args()

    # run main function
    main(args)