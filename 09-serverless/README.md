
# download model
run following in terminal
```
PREFIX="https://github.com/alexeygrigorev/large-datasets/releases/download/hairstyle"
DATA_URL="${PREFIX}/hair_classifier_v1.onnx.data"
MODEL_URL="${PREFIX}/hair_classifier_v1.onnx"
wget ${DATA_URL}
wget ${MODEL_URL}
```

# get input name
see test.ipynb

# install torch CPU only
edit pyproject.toml first
then `uv sync`

# load image and preprocess as in validation
use load image function as instructed,   
preprocess include resize, totensor and normalize.   
first turn img into numpy array, add batch size,   
then use the pytorch preprocess function given,   
   
see lambda_function.py.  

# pull docker image
`docker pull agrigorev/model-2025-hairstyle:v1`
`docker image`
it shows image size is 608MB.  

# lambda function in Dockerfile
see lambda function and dockerfile


# run lambda function in docker 
```
docker build -t hairstyle-prediction:v1 .
docker run -it --rm \
    -p 8080:8080 \
    -e MODEL_PATH="hair_classifier_empty.onnx" \
    hairstyle-prediction:v1
```
open another terminal.  
`python test.py`
-0.10220836102962494



