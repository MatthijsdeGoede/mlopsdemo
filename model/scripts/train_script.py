
import os
import numpy as np
import joblib

from sklearn.linear_model import LogisticRegression
from azureml.core import Dataset, Run

# Workspace and Run configuration
run = Run.get_context()
ws = run.experiment.workspace

#Import data here!
train = Dataset.get_by_name(name='demo_train_set_mnist', workspace=ws, version='latest')
test = Dataset.get_by_name(name='demo_test_set_mnist', workspace=ws, version='latest')

# Data preparation: Separate labels from features, and normalize features on the fly
train_df = train.to_pandas_dataframe()
test_df = test.to_pandas_dataframe()  
x_train = train_df.iloc[:, 1:] / 255
y_train = train_df.loc[:,"label"]
x_test = test_df.iloc[:, 1:] / 255
y_test = test_df.loc[:, "label"]

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
