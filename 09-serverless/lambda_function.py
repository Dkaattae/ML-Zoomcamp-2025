import os
import numpy as np
import onnxruntime as ort
from io import BytesIO
from urllib import request

from PIL import Image

onnx_model_path = os.getenv("MODEL_PATH", "hair_classifier_v1.onnx")


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def preprocess_pytorch_style(X):
    # X: shape (1, 299, 299, 3), dtype=float32, values in [0, 255]
    X = X / 255.0

    mean = np.array([0.485, 0.456, 0.406]).reshape(1, 3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)

    # Convert NHWC → NCHW
    # from (batch, height, width, channels) → (batch, channels, height, width)
    X = X.transpose(0, 3, 1, 2)  

    # Normalize
    X = (X - mean) / std

    return X.astype(np.float32)


def predict(url, onnx_model_path):
    input_size = 200
    img = download_image(url)
    img = prepare_image(img, (input_size,input_size))

    X = np.array(img)
    X = np.expand_dims(X, axis=0)
    input_array = preprocess_pytorch_style(X)

    session = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])

    inputs = session.get_inputs()
    outputs = session.get_outputs()

    input_name = inputs[0].name
    output_name = outputs[0].name

    results = session.run([output_name], {input_name: input_array})
    predictions = results[0][0].tolist()
    return predictions


def lambda_handler(event, context):
    # url = 'https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'
    # onnx_model_path = "hair_classifier_v1.onnx"
    url = event["url"]
    predictions = predict(url, onnx_model_path)
    return predictions

