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

import os
from datetime import timedelta

# 基础配置
DEBUG = False
TESTING = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'CHANGE_ME_TO_A_RANDOM_STRING')

# 数据库配置
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'postgresql://superset:superset@localhost:5432/superset'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 缓存配置
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
}

# 数据上传配置
UPLOAD_FOLDER = '/var/lib/superset/uploads'
ALLOWED_EXTENSIONS = {'csv', 'json', 'xlsx', 'xls', 'tsv'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

# 安全配置
WTF_CSRF_ENABLED = True
CSRF_EXEMPT_LIST = []
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
PERMANENT_SESSION_LIFETIME = timedelta(days=1)

# 应用配置
ROW_LIMIT = 5000
VIZ_ROW_LIMIT = 10000
SUPERSET_WEBSERVER_PORT = int(os.environ.get('SUPERSET_PORT', 8088))
SUPERSET_WEBSERVER_TIMEOUT = int(os.environ.get('SUPERSET_WEBSERVER_TIMEOUT', 600))

# Celery 配置
CELERY_CONFIG = {
    'broker_url': os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    'result_backend': os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    'worker_concurrency': 4,
    'task_acks_late': True,
    'task_reject_on_worker_lost': True,
}

# 自定义可视化配置
DEFAULT_VIZ_TYPE = 'table'
ALLOW_ADHOC_SUBQUERIES = True

# 国际化配置
BABEL_DEFAULT_LOCALE = 'en'
BABEL_SUPPORTED_LOCALES = [
    'en', 'zh', 'fr', 'es', 'de', 'ru', 'ja', 'pt_BR', 'it', 'ko', 'nl'
]
