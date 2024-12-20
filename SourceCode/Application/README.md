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