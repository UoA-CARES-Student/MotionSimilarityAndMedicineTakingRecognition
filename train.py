from exercise_recognition import folder_setup
from exercise_recognition import train as exercise_train
from exercise_recognition.train import define_model as exercise_define_model 
from exercise_recognition.train import train_model as exercise_train_model

# Ninger's imports
from medicine_taking import Train
from medicine_taking.Train import build_feat_extractor
from medicine_taking.Train import build_model
from medicine_taking.Train import trainVggRnn

import os
import sys
import argparse
import torch

from warnings import filterwarnings
filterwarnings('ignore')

def train_combined(arguments): 
    # If the model path does not exist, create it 
    if not os.path.exists(os.path.join(arguments.model_path)): 
        os.mkdir(os.path.join(arguments.model_path))

    # If the model name is not entered, throw an error
    if not arguments.model_name: 
        print("Need a model name to store weights to, please input it using --model_name and try again!")
        quit()

    # If the dataset does not exist in path, throw error
    if not os.path.exists(arguments.dataset_path): 
        print("Dataset path invalid, please check that the right path is referenced in --dataset_path and try again!")
        quit()

    # CPU or GPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 

    # Define the model 
    if(arguments.model_type != "VGG"):
        # Change dataset path
        folder_setup.DATA_PATH = arguments.dataset_path

        exercise_train.RNN_type = arguments.model_type
        exercise_train.train = True
        exercise_train.loc = os.getcwd()
        model = exercise_define_model(exercise_train.RNN_type)
        print(model.summary())
    else: #VGG model
        model1 = build_feat_extractor(); #VGG16 Model for feature extractor Save as Feature_Extractor.h5
        model = build_model(); #RNN model save as RNN.h5
        print(model1.summary()) #VGG16 Model Summary
        print(model.summary()) #RNN model Summary


    # Train the model
    if(arguments.model_type != "VGG"):
       model = exercise_train_model(model, arguments.model_name, arguments.model_path)
    else: 
        #for VGG16 model
        Train.POSITIVES_PATH_TRAIN = 'medicine_taking/data/Train/Class1/'
        Train.NEGATIVES_PATH_TRAIN = 'medicine_taking/data/Train/Class2/'
        Train.POSITIVES_PATH_VALID = 'medicine_taking/data/Val/Class1/'
        Train.NEGATIVES_PATH_VALID = 'medicine_taking/data/Val/Class2/'
        trainVggRnn()


if __name__ == '__main__':
    # Create an ArgumentParser for each of the parameters 
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', type=str, default='./dataset')
    parser.add_argument('--model_path', type=str, default='./models')
    parser.add_argument('--model_name', type=str)
    parser.add_argument('--model_type', type=str, choices=['VGG','LSTM','GRU'])

    # Parse them and begin training
    arguments = parser.parse_args()
    train_combined(arguments)
