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

LIB_DIR=${LIB_DIR:-/usr/lib/kibana}
ETC_KIBANA=${ETC_KIBANA:-/etc/kibana}
VAR_DIR=$PREFIX/var

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/data
install -d -m 0755 $PREFIX/$LIB_DIR/node
install -d -m 0755 $PREFIX/$LIB_DIR/node_modules
install -d -m 0755 $PREFIX/$LIB_DIR/plugins
install -d -m 0755 $PREFIX/$LIB_DIR/src
install -d -m 0755 $PREFIX/$LIB_DIR/x-pack
install -d -m 0755 $PREFIX/$ETC_KIBANA
install -d -m 0755 $PREFIX/$ETC_KIBANA/config
install -d -m 0755 $PREFIX/var/log/kibana
install -d -m 0755 $PREFIX/var/run/kibana

# Copy to LIB_DIR
ARCH=$(uname -m)
if [ "${ARCH}" = "x86_64" ];then
  cp -ra $BUILD_DIR/bin/* ${PREFIX}/${LIB_DIR}/bin/
  cp -ra $BUILD_DIR/node/* ${PREFIX}/${LIB_DIR}/node/
  cp -ra $BUILD_DIR/node_modules/* ${PREFIX}/${LIB_DIR}/node_modules/
  cp -ra $BUILD_DIR/src/* ${PREFIX}/${LIB_DIR}/src/
  cp -ra $BUILD_DIR/x-pack/* ${PREFIX}/${LIB_DIR}/x-pack/
fi
if [ "${ARCH}" = "aarch64" ];then
  cp $BUILD_DIR/package.json ${PREFIX}/${LIB_DIR}/
  cp -ra $BUILD_DIR/bin/* ${PREFIX}/${LIB_DIR}/bin/
  cp -ra $BUILD_DIR/node/* ${PREFIX}/${LIB_DIR}/node/
  cp -ra $BUILD_DIR/node_modules/* ${PREFIX}/${LIB_DIR}/node_modules/
  cp -ra $BUILD_DIR/src/* ${PREFIX}/${LIB_DIR}/src/
  cp -ra $BUILD_DIR/x-pack/* ${PREFIX}/${LIB_DIR}/x-pack/
fi


ln -s $ETC_KIBANA/config $PREFIX/$LIB_DIR/config
ln -s /var/log/kibana $PREFIX/$LIB_DIR/logs
ln -s /var/run/kibana $PREFIX/$LIB_DIR/pid

cp -ra $BUILD_DIR/config/* ${PREFIX}/kibana/config/
