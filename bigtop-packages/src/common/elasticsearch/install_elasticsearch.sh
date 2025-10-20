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

set -e

usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --distro-dir=DIR            path to distro specific files (debian/RPM)
     --build-dir=DIR             path to dist dir
     --prefix=PREFIX             path to install into

  Optional options:
     --lib-dir=DIR               path to install bits [/usr/lib/elasticsearch]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'distro-dir:' \
  -l 'lib-dir:' \
  -l 'build-dir:' -- "$@")

if [ $? != 0 ] ; then
    usage
fi

eval set -- "$OPTS"
while true ; do
    case "$1" in
        --prefix)
        PREFIX=$2 ; shift 2
        ;;
        --distro-dir)
        DISTRO_DIR=$2 ; shift 2
        ;;
        --build-dir)
        BUILD_DIR=$2 ; shift 2
        ;;
        --lib-dir)
        LIB_DIR=$2 ; shift 2
        ;;
        --)
        shift; break
        ;;
        *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
done

for var in PREFIX BUILD_DIR DISTRO_DIR ; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

LIB_DIR=${LIB_DIR:-/usr/lib/elasticsearch}
ETC_ELASTICSEARCH=${ETC_ELASTICSEARCH:-/etc/elasticsearch}
VAR_DIR=$PREFIX/var

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/lib
install -d -m 0755 $PREFIX/$LIB_DIR/modules
install -d -m 0755 $PREFIX/$LIB_DIR/plugins
install -d -m 0755 $PREFIX/$LIB_DIR/licenses
install -d -m 0755 $PREFIX/$ETC_ELASTICSEARCH
install -d -m 0755 $PREFIX/$ETC_ELASTICSEARCH/config
install -d -m 0755 $PREFIX/var/log/elasticsearch
install -d -m 0755 $PREFIX/var/run/elasticsearch


cp -ra $BUILD_DIR/bin/* ${PREFIX}/${LIB_DIR}/bin/
cp -ra $BUILD_DIR/lib/* ${PREFIX}/${LIB_DIR}/lib/
cp -ra $BUILD_DIR/modules/* ${PREFIX}/${LIB_DIR}/modules/
cp -a  $BUILD_DIR/LICENSE.txt ${PREFIX}/${LIB_DIR}/licenses/
chmod 755 ${PREFIX}/${LIB_DIR}/bin/*

# 手动为 x-pack-ml 的二进制文件生成 build-id
ML_BIN_DIR="${PREFIX}/${LIB_DIR}/modules/x-pack-ml/platform/linux-aarch64/bin"
for file in $ML_BIN_DIR/{data_frame_analyzer,autodetect,normalize,categorize,controller}; do
  if [ -f "$file" ]; then
    eu-strip --build-id=sha1 "$file"  # 替换为 sha1 格式，兼容低版本
    # eu-strip --build-id=both "$file"  # 生成并嵌入 build-id
  fi
done

ln -s $ETC_ELASTICSEARCH/config $PREFIX/$LIB_DIR/config
ln -s /var/log/elasticsearch $PREFIX/$LIB_DIR/logs
ln -s /var/run/elasticsearch $PREFIX/$LIB_DIR/pid

cp -ra $BUILD_DIR/config/* ${PREFIX}/$ETC_ELASTICSEARCH/config/
