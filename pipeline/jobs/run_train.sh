# Initiate the job on the compute cluster
az ml job create --name $1 --file pipeline/jobs/train.yml --set inputs.data_folder.path=$2
# Track the output stream of the job running on the compute cluster
az ml job stream --name $1