# 10-k8s
## install kind
```
sudo curl -Lo /usr/local/bin/kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
sudo chmod +x /usr/local/bin/kind
```
note that codespaces does not let me edit bin without sudo

## clone folder
```
git clone --no-checkout https://github.com/DataTalksClub/machine-learning-zoomcamp.git
cd machine-learning-zoomcamp
git sparse-checkout init --cone
git sparse-checkout set cohorts/2025/05-deployment/homework
git checkout master
```

## build image
`docker build -f Dockerfile_full -t zoomcamp-model:3.13.10-hw10 .`

## test running
{'conversion_probability': 0.49999999999842815, 'conversion': False}

## kind version
kind v0.20.0

## k8s basic
- pod: one docker image.  
- node: a worker machine, (physical or VM)
- deployment: manager of pods. it creates pods, if a pod is dead, create a new one.
- service: network abstraction, it assigns IP address to pods
- HPA: decide how many pods based on CPU usage. 
the smallest unit is pod

## check running services
```
kubectl get services
```
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   4m8s

## kind load image
```
kind load docker-image zoomcamp-model:3.13.10-hw10 --name mlzoomcamp
```

## apply deployment

## apply service
targetPort is the port exposed in docker image.  
port is an internal port, ClientIP:port.  
nodePort is an external port, NodeIP: nodePort 30000-32767.  
```
kubectl apply -f service.yaml
```

kubectl get services
NAME           TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes     ClusterIP      10.96.0.1       <none>        443/TCP        15m
subscription   LoadBalancer   10.96.199.193   <pending>     80:30520/TCP   9s

## forward port locally
```
kubectl port-forward service/subscription 9696:80
```
in another terminal, run test again

## autoscaling
apply components.yaml.  
and patch metric server.  
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

kubectl patch -n kube-system deployment metrics-server --type=json -p '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
```
run python q6_test.py to test it. 

## delete cluster
```
kind delete cluster --name mlzoomcamp
```