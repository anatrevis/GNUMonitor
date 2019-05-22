#!/bin/bash

source ~/.bash_profile

conda activate myDjangoEnv

cd server

nohup python3 manage.py runserver &

python3 reqrep_server.py

