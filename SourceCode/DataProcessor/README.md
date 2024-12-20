# DataProcessor

## Purpose
input = 3 second duration .wav (Data/IRMAS-TrainingData)
middle output 1 = db normalized 3 second duration .wav (Data/Output/Normalize)
middle output 2 = 224x224 mel-spectrogram image (Data/Output/Spectrogram)
middle output 3 = tensor datafile (Data/Output)

## Code description
The process and description is in DataProcessor.ipynb file. 

## Note
- The data in 'Data' folder in this repository is a subset of the entire dataset.
- the 'dataset.pt' is too large to upload in github repository. Instead, [a link to connected Google Drive] (https://drive.google.com/file/d/1-0pjHdo49dzRGAXVPWdLk4zj95g4c8Dv/view?usp=sharing) is provided.
- 'DataProcessor.inpyb' file is clone of code in my google drive. Note that the file input and storage path is different with from the structure of this repository.
