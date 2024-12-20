# CTP431-Fall

This repository is consist of 3 parts: DatasetProcessor, Model, Application.


# DataProcessor

## Purpose
input = 3 second duration .wav (Data/IRMAS-TrainingData)

![input](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/DataProcessor/input.png)

middle output 1 = db normalized 3 second duration .wav (Data/Output/Normalize)

![middle output 1](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/DataProcessor/output_1.png)

middle output 2 = 224x224 mel-spectrogram image (Data/Output/Spectrogram)

![middle output 2](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/DataProcessor/output_2.jpg)

middle output 3 = tensor datafile for training/test (Data/Output)

![output](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/DataProcessor/output_3.png)



## Code description
The process and description is in DataProcessor.ipynb file. 

## Note
-The data in 'Data' folder in this repository is a subset of the entire dataset.

-the 'training_data.pt', 'test_data.pt' file for train/test are too large to upload in github repository. Instead, 
[link to training data](https://drive.google.com/file/d/1foyqjrKsjKbecpxFYvdISFZDJ7pmim1K/view?usp=sharing) 
[link to test data](https://drive.google.com/file/d/1-3Mu2BdkrplITL1gxGVfnfVXm2u5Xvin/view?usp=sharing) 
is provided.

-'DataProcessor.inpyb' file is clone of code in my google drive. Note that the file input and storage path is different with from the structure of this repository.


# Model

## Source Codes
Simple_CNN.ipynb model for simple CNN

Imporved_CNN.ipynb model for simple CNN and some tests

VGG19_Pure.ipynb model for pure vgg19 model

VGG19_CNN.ipynb model for vgg19 model with pre-trained feature parameters

## VGG19
![Model Structure](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Model/VGG19.png)




# Application - Backend

## main code
processor.py for process file in backend.
flask_app.py for running flask app.

## Process
1. Run flask app with flask_app.py.
2. Wait until frontend sends .wav files.
3. If frontend sends file, save file in input_sounds directory.

![step_3](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Backend/step_3.png)

4. Split file to 3-duration sound chunks.

![step_4](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Backend/step_4.png)

5. Create mel-spectrogram images with sound chunks.

![step_5](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Backend/step_5.png)

6. Run model with model file from 'Model' directory result.
7. Send saved sound file path, mel-spectrogram images and expected label result to frontend.




# Application - Frontend
## main code
App.js for react frontend (Frontend/src)

## Process
1. Run react app with App.js

![react_app](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Frontend/react_app.png)

2. Select .wav file and click 'Upload and Process' button

![select](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Frontend/select.png)

3. If backend process ends, can watch many things! 

![result_total](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Frontend/result_total.png)

- set of (expected instrument index, mel spectrogram image)

![result_set](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Frontend/result_set.png)

- audio player 

![result_player](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Frontend/result_player.png)

- model prediction corresponding current played time index of audio player

![result_predict](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Frontend/result_predict.png)