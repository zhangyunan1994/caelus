#!/usr/bin/env bash
kill -9 $(ps -ef | grep gunicorn | grep -v grep | awk '{print $2}')