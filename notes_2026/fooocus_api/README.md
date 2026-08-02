# Run Server and Generate Images

## Setup
1. Install and Run Docker
2. git clone https://github.com/mrhan1993/Fooocus-API.git
3. Run docker\_run.bat to run docker container. Specify path to Fooocus-Api models folder.
   e.g. "C:\Users\1\Documents\Fooocus-API\repositories\Fooocus\models"

## Use API
1. Go to http://127.0.0.1:8888/docs
2. Use POST /v1/generation/text-to-image to generate image from prompt

## Generate Images using Python
```
pip install -r requirements.txt
python generate_images.py
```


# Full automatic pipeline Docketr + Python

Fooocus
```powershell
pip install -r requirements.txt
$env:FOOOCUS_MODELS_DIR="C:\Users\1\Documents\Fooocus\Fooocus\models"
python pipeline_generate_images.py
```

Fooocus Api
```powershell
pip install -r requirements.txt
$env:FOOOCUS_MODELS_DIR="C:\Users\1\Documents\Fooocus-API\repositories\Fooocus\models"
python pipeline_generate_images.py
```
