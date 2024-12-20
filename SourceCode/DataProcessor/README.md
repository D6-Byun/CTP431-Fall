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
