# ai-support
AIサポーター

# AI Support Project

## Prerequisites
Setting audio in windows and vechat app: Please refer the documentation file named "AI_avatar_Manual" for VB audio channels settings and follow along:
The doc descirbes the settings to be done in VRChat app audio microphones and also in Windows audio settings.

## Running the Project

Step1: First install the dependencies using:
```
pip install -r requirements.txt
```

Then,
Step2: Run the driver file name "run.py" for enabling speech chat using 
```
python run.py
```

Step3: Run the "fastapi_vr_textchat.py" for enabling text chat using
```
uvicorn faatapi_vr_textchat:app --port 8000 --reload"
```

## Note
For the text chat functionality to work, the corresponding U# files and Unity Scenes for manipulating the UI should exist in the Unity Project.

## Potential Errors and Debug:
if the python version used is 3.12.0 ,this version lacks "distutils" as it was depriciated in this verison. So, if an error 
occurs saying "No module named 'distutils'" when using python verison 3.12.0, it can be solved by installing setuptools using "pip install setuptools"