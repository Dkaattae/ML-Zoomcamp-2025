# HomeWork

## 1, version
0.9.5

## 2, sciket-learn hash
this is the hash from sdist
sha256:b4fc2525eca2c69a59260f583c56a7557c6ccdf8deafdba6e060f94c1c59738e

## 3, predict
predicted_probability = 0.533

## 4, fastAPI

curl -X POST 'http://localhost:9696/predict' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
        "lead_source": "organic_search",
        "number_of_courses_viewed": 4,
        "annual_income": 80304.0
    }'
{'pred_converted': 0.5340417283801275}

## 5, docker
docker image ls
REPOSITORY                 TAG       IMAGE ID       CREATED      SIZE
agrigorev/zoomcamp-model   2025      4a9ecc576ae9   3 days ago   121MB

## 6, dockerfile
```
docker build -t predict-converted .
docker run -it --rm -p 9696:9696 predict-converted
```

{'pred_converted': 0.9933071490756734}
