import argparse
from azureml.core import Model, Run, Dataset

def main(args):
    run = Run.get_context()   
    ws = run.experiment.workspace
    model = Model(ws, args.model_name)
    train = Dataset.get_by_name(name=args.train_ds, workspace=ws, version='latest')
    test = Dataset.get_by_name(name=args.test_ds, workspace=ws, version='latest')
    model.add_dataset_references([('training_dataset', train), ('testing_dataset', test)])


def parse_args():
    # parsing the arguments provided by the pipeline
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--train_ds", type=str)
    parser.add_argument("--test_ds", type=str)

    return parser.parse_args()


# run script
if __name__ == "__main__":
    # parse args
    args = parse_args()

    # run main function
    main(args)