# Application - Backend

## main code
processor.py for process file in backend.
flask_app.py for running flask app.

## Process
1. Run flask app with flask_app.py.
2. Wait until frontend sends .wav files.
3. If frontend sends file, save file in input_sounds directory.
![step_3](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Backend/step_3.png)

4. Split file to 3-duration sound chunks
![step_4](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Backend/step_4.png)

5. Create mel-spectrogram images with sound chunks.
![step_5](https://github.com/D6-Byun/CTP431-Fall/blob/main/SourceCode/Application/Backend/step_5.png)

6. Run model with model file from 'Model' directory result.
7. Send saved sound file path, mel-spectrogram images and expected label result to frontend.