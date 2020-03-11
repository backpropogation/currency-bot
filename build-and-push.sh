#!/bin/bash

docker build -t backpropogation/currency_bot:server_latest  . -f ./server/Dockerfile
docker build -t backpropogation/currency_bot:bot_latest . -f ./Dockerfile.bot

docker push backpropogation/currency_bot:server_latest
docker push backpropogation/currency_bot:bot_latest
