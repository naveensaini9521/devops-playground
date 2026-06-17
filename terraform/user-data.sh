#!/bin/bash

apt update -y

apt install git -y

apt install docket.io -y

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

cd /home/ubuntu

git clone https://github.com/naveensaini9521/smart_voting_system_with_face_recognition.git

cd smart_voting_system_with_face_recognition

docker compose up -d