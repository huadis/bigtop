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

set -euo pipefail

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        --prefix)
            PREFIX="$2"
            shift 2
            ;;
        --source-dir)
            SOURCE_DIR="$2"
            shift 2
            ;;
        --install-dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        *)
            echo "Error: Unknown option $1"
            exit 1
            ;;
    esac
done

# 校验参数
if [ -z "${PREFIX:-}" ] || [ -z "${SOURCE_DIR:-}" ] || [ -z "${INSTALL_DIR:-}" ]; then
    echo "Usage: $0 --prefix <rpm_build_root> --source-dir <source_dir> --install-dir <install_dir>"
    exit 1
fi

# 定义目标路径
TARGET_DIR="${PREFIX}${INSTALL_DIR}"

# 创建安装目录
mkdir -p "${TARGET_DIR}"

# 复制核心文件
cp -r "${SOURCE_DIR}/bin" "${TARGET_DIR}/"
cp -r "${SOURCE_DIR}/lib" "${TARGET_DIR}/"
cp -r "${SOURCE_DIR}/server" "${TARGET_DIR}/"
cp -r "${SOURCE_DIR}/client" "${TARGET_DIR}/"
cp -r "${SOURCE_DIR}/static" "${TARGET_DIR}/"
cp -r "${SOURCE_DIR}/licenses" "${TARGET_DIR}/"
cp -r "${SOURCE_DIR}/plugins" "${TARGET_DIR}/"

# 创建配置目录
mkdir -p "${TARGET_DIR}/conf"

# 设置可执行权限
chmod +x "${TARGET_DIR}/bin/"*.sh
chmod +x "${TARGET_DIR}/bin/streampark-cli"

echo "StreamPark installed to ${TARGET_DIR}"
