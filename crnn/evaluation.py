#!/usr/bin/env python
__author__ = "solivr"
__license__ = "GPL"

import os
from glob import glob

import click
from tf_crnn.callbacks import CustomLoaderCallback, FOLDER_SAVED_MODEL
from tf_crnn.config import Params, CONST
from tf_crnn.data_handler import dataset_generator
from tf_crnn.preprocessing import preprocess_csv
from tf_crnn.model import get_model_train


@click.command()
@click.option('--csv_filename')
@click.option('--model_dir')
def evaluation(csv_filename: str,
               model_dir: str):

    config_filename = os.path.join(model_dir, 'config.json')
    parameters = Params.from_json_file(config_filename)

    saving_dir = os.path.join(parameters.output_model_dir, FOLDER_SAVED_MODEL)

    # Callback for model weights loading
    last_time_stamp = max([int(p.split(os.path.sep)[-1].split('-')[0])
                           for p in glob(os.path.join(saving_dir, '*'))])
    loading_dir = os.path.join(saving_dir, str(last_time_stamp))
    ld_callback = CustomLoaderCallback(loading_dir)

    # Preprocess csv data
    csv_evaluation_file = os.path.join(parameters.output_model_dir, CONST.PREPROCESSING_FOLDER, 'evaluation_data.csv')
    n_samples = preprocess_csv(csv_filename,
                               parameters,
                               csv_evaluation_file)

    dataset_evaluation = dataset_generator([csv_evaluation_file],
                                           parameters,
                                           batch_size=parameters.eval_batch_size,
                                           num_epochs=1)

    # get model and evaluation
    model = get_model_train(parameters)
    eval_output = model.evaluate(dataset_evaluation,
                                 callbacks=[ld_callback])
    print('-- Metrics: ', eval_output)


if __name__ == '__main__':
    evaluation()
