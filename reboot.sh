#!/usr/bin/env bash

echo -e "\033[34m---------------------wsgi process--------------------------\033[0m"

ps -ef|grep uwsgi.ini | grep -v grep

sleep 0.5

echo -e '\n------------------------going to close -----------------'

ps -ef |grep uwsgi.ini | grep -v grep | awk '{print $2}' | xargs kill -9

sleep 0.5

echo -e '\n------------------------check if the kill action is correct -----------------'


source /www/wwwroot/root/my_django_project/newenv/bin/activate
sleep 1

uwsgi --ini  uwsgi.ini & >/dev/null

echo -e "\033[34m---------------------started...--------------------------\033[0m"
sleep 1

ps -ef|grep uwsgi.ini | grep -v grep