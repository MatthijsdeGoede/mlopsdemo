
# About the demo

This demo showcases a training workflow of a _Logistic Regression Classifier_ on the famous _MNIST Dataset_ using _Azure Machine Learning_ and _Azure Pipelines_. The training step of the model is done via a simple _Python_ script using the machine learning library _Scikit Learn_. The inputs comprise a set of pixel grayscale values for a set of handwritten digit images as well as their corresponding labels. The final output of the workflow is a containerized model that can be leveraged to predict the labels of handwritten digits.  

![MNIST Example](https://i2.paste.pics/a5dcff29c4149a67339595ed0c2b9398.png)
 
## The pipeline that transforms the inputs into outputs has the following steps:

1.	Configure an AzureML _workspace_
2.	Prepare the _input data_ for _data versioning_
3.	Configure an AzureML _Virtual Environment_
4.	Configure an AzureML _Compute Cluster_
5.	Create an AzureML _Datastore/Dataset_
6.	Run an AzureML _Training Job_ on _Compute Cluster_
7.	_Register_ the resulting _Model_ in AzureML
8.	Create a deployable _Model Image_

## Two different approaches to build the pipeline for the training workflow have been implemented:

1. __Local pipeline with AzureML Python SDK (v1)__  
Applying this approach, we make use of _Jupyter Notebooks_ and the _Python SDK (v1) for Azure Machine Learning_. The resulting notebooks define the entire training workflow and can be run locally or in _Azure Machine Learning Studio_. The corresponding files can be found in the [model folder](model/). 

2. __Azure DevOps CI/CD pipeline with AzureML CLI (v2)__  
Applying the second approach, we rely heavily on the _Azure Machine Learning CLI (v2)_, which is currently still in _preview_. This approach leverages _Azure DevOps’ CI/CD functionalities_ by running a pipeline defining every step in the training workflow separately using _Bash_, _Azure CLI_ and/or _PowerShell_ commands. The resulting pipeline is defined in a [YAML file](azure-pipelines.yml). The individual _Infrastructure as Code (IaC)_ components and scripts used in the pipeline can be found under the [pipeline folder](pipeline/).

The image below gives an overview of the main characteristics of both approaches:

![Two approaches summary](https://i2.paste.pics/b54814d9cfac3347efd171742cbd63c0.png)
 
# Getting started

In order to run the training workflow presented in this demo, one must configure several _Azure Resources_ as well as an _Azure DevOps Project_. 


# Setting up Azure Resources

1.	In the _Azure Portal_, create an Azure _resource group_
2.	Create an _Azure Machine Learning_ resource
    -  Make sure that a _Key Vault_ and _Container Registry (Standard)_ resource are created
3.	Create a new _storage account_ with _hierarchical namespace_ enabled under _Advanced settings_
4.	In the _storage account_, create a new _container_ named _mnist-dataset_
5.	Set the _Access Level_ of _mnist-dataset_ to _Blob_ 
6.	Download the [_training_](https://microsofteur-my.sharepoint.com/:x:/g/personal/t-mdegoede_microsoft_com/Edyep_VniLdLsC7g5Iay2R0B7T729Eau9Ddrl2Kxx5R3QQ?e=o8FW8S&wdLOR=c93C93B1C-4468-4E04-A09D-E1EFCA03C792) and [_test_](https://microsofteur-my.sharepoint.com/:x:/g/personal/t-mdegoede_microsoft_com/EQq73u4KbpNJqg6tK_3YVbMB5mWyOgYKaFlc9jqajAtUCg?e=Rq0f61) datasets
7.	Upload the downloaded _.csv_ files to the _mnist-dataset_ container
8.	In the _Key Vault_, create a new secret named _storage-key_, having the value of the _Access Key_ belonging to the _storage account_


# Setting up Azure DevOps

9.	In _Azure DevOps_, create a new _Organization_
10.	Within the _Organization_, create a new _Project_
11.	Under _Project Settings/Service connections_ create a new _Azure Resource Manager connection_ using _service principal_ and check _Grant access permission to all pipelines_
12.	Under _Repos_ click _Import a Repository_ from the [_Clone URL_](https://github.com/MatthijsdeGoede/mlopsdemo.git)
13.	The _repo_ should now look like this:  

![Azure DevOps Repo](https://i2.paste.pics/32ed3380dc5ee0ec24d30c629b1a557a.png)

14.	Under _Pipelines_, create a _new pipeline_ using _Azure Repos Git_ selecting the just created repo. 
15.	Investigate the _pipeline YAML definition_ that can be edited, saved, and ran
    -  Make sure that the _pipeline variables_ have values that correspond to your azure resource names.
16.	Navigate to [train_remote.ipynb](model/notebooks/train_remote.ipynb) and make sure to update the variables indicated below according to your azure resources
    -  Repeat the same procedure for [train.ipynb](model/notebooks/train.ipynb)

![Variables to change](https://i2.paste.pics/90560295b6bda9657a8f24376cee242e.png)

17.	_Commit_ your changes to the _main branch_
18.	One can now find the pipeline under _Pipelines_ and edit, run, and track it from there. 
    -  Pipelines can be run both manually and triggered by incoming commits on a certain _branch_ of the _repository_

# Editing the code 

Instead of to the editor present in _Azure DevOps_, developers typically use _Visual Studio Code_ to modify the code in the repository and run the notebooks. However, the _Azure Machine Learning Studio_ also offers some functionality to do this.


# Running the Notebooks in Azure Machine Learning Studio

1.	In _Azure Machine Learning Studio_, navigate to _Compute_ to create a new _Compute Instance_ to run the notebooks on, the _Standard_DS11_v2_ tier should suffice 
    -  Wait till the creation finishes and click to _Start_
2.	Navigate to the _Notebook_ section and click _Open Terminal_ for which the _Compute Instance_ can be set to the one just created
3.	In _Azure Devops_, navigate to the _Repo_ and click _Clone_ and _Generate Git Credentials_, note the _HTTPS Link_ and _password_ down
4.	In the _Azure Machine Learning Studio terminal_, type _git clone_ followed by the _HTTPS Link_
    -  Enter the _password_ from the _Azure DevOps_ credentials
5.	After _refreshing_ the notebook tree, the cloned _repo_ should be visible on the left:

![Notebook Tree](https://i2.paste.pics/b01228f35135b9b37cc9ad97f08345e4.png)

6.	One can now navigate to the [notebooks](model/notebooks) and inspect, edit, and run them via the _integrated notebook editor_:  

![Notebook editor](https://i2.paste.pics/bbbf7e09bdd0c9b58d3c7cbe84d1c2eb.png)

7.	After making changes, one can leverage normal _git commands_ using the _terminal_ to _commit_ and _push_ the changes to the _Azure DevOps Repo_


