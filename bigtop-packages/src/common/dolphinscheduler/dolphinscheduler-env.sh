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

# JDK 配置
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export PATH=$JAVA_HOME/bin:$PATH

# DolphinScheduler 安装目录
export DOLPHINSCHEDULER_HOME=/usr/lib/dolphinscheduler

# 数据存储配置
export DATASOURCE_DRIVER_CLASS_NAME=com.mysql.cj.jdbc.Driver
export DATASOURCE_URL=jdbc:mysql://localhost:3306/dolphinscheduler?useUnicode=true&characterEncoding=UTF-8&useSSL=false
export DATASOURCE_USERNAME=root
export DATASOURCE_PASSWORD=password

# Zookeeper 配置
export ZOOKEEPER_QUORUM=localhost:2181

# 服务端口配置
export MASTER_SERVER_PORT=5678
export WORKER_SERVER_PORT=1234
export API_SERVER_PORT=12345

# 日志配置
export LOG_DIR=/var/log/dolphinscheduler
export LOG_LEVEL=INFO

# Hadoop 配置
export HADOOP_CONF_DIR=/etc/hadoop/conf
export YARN_CONF_DIR=/etc/hadoop/conf
