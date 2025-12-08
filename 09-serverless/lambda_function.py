import numpy as np
import onnxruntime as ort
from io import BytesIO
from urllib import request

from PIL import Image
import torchvision.models as models
from torchvision import transforms


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


def predict(url, onnx_model_path):
    input_size = 200
    img = download_image(url)
    img = prepare_image(img, (input_size,input_size))

    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    preprocess = transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])

    tensor = preprocess(img)
    tensor = tensor.unsqueeze(0)

    input_array = tensor.numpy().astype(np.float32)

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
    onnx_model_path = event["onnx_model_path"]
    predictions = predict(url, onnx_model_path)
    return predictions

