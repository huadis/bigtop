#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Python 环境配置
export PYTHONPATH=/usr/lib/superset
export VENV_PATH=/usr/lib/superset/venv
export PATH=$VENV_PATH/bin:$PATH

# Superset 配置
export SUPERSET_HOME=/usr/lib/superset
export SUPERSET_CONFIG_PATH=/etc/superset/conf/superset_config.py

# 日志配置
export LOG_DIR=/var/log/superset
export GUNICORN_ACCESS_LOG_FILE=$LOG_DIR/access.log
export GUNICORN_ERROR_LOG_FILE=$LOG_DIR/error.log

# 数据库配置
export SQLALCHEMY_DATABASE_URI=postgresql://superset:superset@localhost:5432/superset

# Web 服务配置
export SUPERSET_PORT=8088
export GUNICORN_WORKERS=4
export GUNICORN_THREADS=4
export GUNICORN_TIMEOUT=120

# Celery 配置
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0

# 安全配置
export SECRET_KEY='CHANGE_ME_TO_A_RANDOM_STRING'
export WTF_CSRF_ENABLED=True
export SESSION_COOKIE_SECURE=False

# 性能配置
export SUPERSET_WEBSERVER_TIMEOUT=600

