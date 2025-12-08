import requests

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

event = {
    "url": "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg",
    "onnx_model_path": "hair_classifier_empty.onnx"
}
result = requests.post(url, json=event).json()
print(result)