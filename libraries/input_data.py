import tensorflow as tf
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib import gridspec
from sklearn import preprocessing
from enum import Enum

class Scaling(Enum):
    minmax = 1
    standard = 2

class InputData():
    
    def get_scaler(self):
        return self.scaler
    
    def iterator(self, mb_size, i):
        np.random.seed(i*100+mb_size)
        idx = np.random.randint(0, self.train.shape[0], mb_size)
        
        return self.train[idx, :], self.train_labels[idx, :]
    
    def __scale(self, scaling=Scaling.minmax):
        
        if scaling==Scaling.minmax:
            scaler = preprocessing.MinMaxScaler((-1, 1))
        else:
            scaler = preprocessing.StandardScaler()

        scaler.fit(self.train)
        self.train = scaler.transform(self.train)
            
        self.scaler = scaler
        
    def load_data(self, dataset_path, test=True):
        loader = self.loader
        self.train_raw, self.train_labels = loader.load_train_set(dataset_path)

        if test:
            self.test_raw, self.test_labels = loader.load_test_set(self.test_labels).as_matrix()
        
    
    def __log_transform(self):
        self.train = np.log2(self.train + 1e-8)
    
    def preprocessing(self, log_transformation, scaling):
        
        # Don't allow to do preprocessing twice, just to avoid possible hazards.
        self.train = self.train_raw

        if self.done_preprocessing:
            raise RuntimeError("Already done preprocessing")
        else:
            self.done_preprocessing = True
        
        self.log_transformation = log_transformation
        self.scaling = scaling
        
        if log_transformation:
            self.__log_transform()

        if scaling in Scaling:
            self.__scale(scaling)
    
    @staticmethod
    def inverse_preprocessing(data, log_transformation, scaler=None):

        if(scaler != None):
            data = scaler.inverse_transform(data)

        if(log_transformation):
            data = np.exp2(data)
        return data
    
    def get_raw_data(self, train=True):
        if train:
            return self.train_raw, self.train_labels
        else:
            return self.test_raw, self.test_labels
    
    def get_data(self, train=True):
        if train:
            return self.train, self.train_labels
        else:
            return self.test, self.test_labels
    
    def __init__(self, dataset_path, loader, test_set=False):
        self.done_preprocessing = False
        self.loader = loader
        self.scaler = None
        
        self.load_data(dataset_path, test_set)
