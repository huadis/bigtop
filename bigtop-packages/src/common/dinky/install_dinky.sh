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

set -ex

usage() {
  echo "
usage: $0 <options>
  Required not-so-options:
     --build-dir=DIR             path to dinky dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --lib-dir=DIR               path to install dinky home [/usr/lib/dinky]
     --etc-dinky=DIR             path to install dinky conf [/etc/dinky]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'lib-dir:' \
  -l 'etc-dinky:' \
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
        --build-dir)
        BUILD_DIR=$2 ; shift 2
        ;;
        --lib-dir)
        LIB_DIR=$2 ; shift 2
        ;;
        --etc-dinky)
        ETC_DINKY=$2 ; shift 2
        ;;
        --)
        shift ; break
        ;;
        *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
done

for var in PREFIX BUILD_DIR ; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

LIB_DIR=${LIB_DIR:-/dinky}
ETC_DINKY=${ETC_DINKY:-/etc/dinky}

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/connectors
install -d -m 0755 $PREFIX/$LIB_DIR/lib
install -d -m 0755 $PREFIX/$LIB_DIR/plugins
install -d -m 0755 $PREFIX/$LIB_DIR/starter
install -d -m 0755 $PREFIX/$ETC_DINKY
install -d -m 0755 $PREFIX/$ETC_DINKY/conf
install -d -m 0755 $PREFIX/var/log/dinky
install -d -m 0755 $PREFIX/var/run/dinky

cp -ra $BUILD_DIR/bin/*.sh ${PREFIX}/${LIB_DIR}/bin/
cp -ra $BUILD_DIR/connectors/* ${PREFIX}/${LIB_DIR}/connectors/
cp -ra $BUILD_DIR/lib/* ${PREFIX}/${LIB_DIR}/lib/
cp -ra $BUILD_DIR/plugins/* ${PREFIX}/${LIB_DIR}/plugins/
cp -ra $BUILD_DIR/starter/* ${PREFIX}/${LIB_DIR}/starter/

ln -s $ETC_DINKY/conf $PREFIX/$LIB_DIR/config
ln -s /var/log/dinky $PREFIX/$LIB_DIR/logs
ln -s /var/run/dinky $PREFIX/$LIB_DIR/pid

cp -ra $BUILD_DIR/config/* ${PREFIX}/$ETC_DINKY/conf/
