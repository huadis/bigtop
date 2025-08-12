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
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=$JAVA_HOME/bin:$PATH

# StreamPark 安装目录
export STREAM_PARK_HOME=/usr/lib/streampark

# 日志配置
export LOG_DIR=/var/log/streampark
export LOG_LEVEL=INFO

# 服务端口配置
export SERVER_PORT=10000

# 数据库配置
export SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/streampark?useUnicode=true&characterEncoding=UTF-8&useSSL=false
export SPRING_DATASOURCE_USERNAME=root
export SPRING_DATASOURCE_PASSWORD=password
export SPRING_DATASOURCE_DRIVER_CLASS_NAME=com.mysql.cj.jdbc.Driver

# Flink 配置
export FLINK_HOME=/usr/lib/flink
export FLINK_CONF_DIR=/etc/flink/conf

# Hadoop 配置
export HADOOP_HOME=/usr/lib/hadoop
export HADOOP_CONF_DIR=/etc/hadoop/conf

# Zookeeper 配置
export ZOOKEEPER_QUORUM=localhost:2181

# 内存配置
export JVM_XMS=1g
export JVM_XMX=2g
export JVM_METASPACE_SIZE=256m
export JVM_MAX_METASPACE_SIZE=512m
