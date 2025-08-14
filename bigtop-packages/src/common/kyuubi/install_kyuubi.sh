#!/bin/bash
#
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
#

set -e

# 定义安装路径和用户
KYUUBI_HOME=/usr/lib/kyuubi
KYUUBI_CONF_DIR=/etc/kyuubi/conf
KYUUBI_LOG_DIR=/var/log/kyuubi
KYUUBI_PID_DIR=/var/run/kyuubi
KYUUBI_USER=kyuubi
KYUUBI_GROUP=hadoop

# 创建用户和组
if ! id -u ${KYUUBI_USER} >/dev/null 2>&1; then
  groupadd -r ${KYUUBI_GROUP}
  useradd -r -g ${KYUUBI_GROUP} -d ${KYUUBI_HOME} -s /sbin/nologin ${KYUUBI_USER}
fi

# 创建目录
mkdir -p ${KYUUBI_HOME}
mkdir -p ${KYUUBI_CONF_DIR}
mkdir -p ${KYUUBI_LOG_DIR}
mkdir -p ${KYUUBI_PID_DIR}

# 复制文件
cp -r ${BUILD_DIR}/kyuubi/* ${KYUUBI_HOME}/

# 移动配置文件到标准位置
mv ${KYUUBI_HOME}/conf/* ${KYUUBI_CONF_DIR}/
ln -s ${KYUUBI_CONF_DIR} ${KYUUBI_HOME}/conf

# 设置权限
chown -R ${KYUUBI_USER}:${KYUUBI_GROUP} ${KYUUBI_HOME}
chown -R ${KYUUBI_USER}:${KYUUBI_GROUP} ${KYUUBI_CONF_DIR}
chown -R ${KYUUBI_USER}:${KYUUBI_GROUP} ${KYUUBI_LOG_DIR}
chown -R ${KYUUBI_USER}:${KYUUBI_GROUP} ${KYUUBI_PID_DIR}

# 创建符号链接到 /usr/bin
ln -s ${KYUUBI_HOME}/bin/kyuubi ${KYUUBI_HOME}/bin/kyuubi-daemon.sh /usr/bin/

# 配置环境变量
cat > /etc/profile.d/kyuubi.sh << EOF
export KYUUBI_HOME=${KYUUBI_HOME}
export KYUUBI_CONF_DIR=${KYUUBI_CONF_DIR}
export PATH=\$PATH:\$KYUUBI_HOME/bin
EOF
