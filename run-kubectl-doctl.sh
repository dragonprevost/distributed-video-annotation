sudo docker build -f kubectl-doctl . --tag=do-workspace
sudo docker container rm -f digitalo
sudo docker run -p 8001:8001 -it --name=digitalo do-workspace
