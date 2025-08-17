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
     --build-dir=DIR             path to streampark dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --lib-dir=DIR               path to install streampark home [/usr/lib/streampark]
     --etc-streampark=DIR             path to install streampark conf [/etc/streampark]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'lib-dir:' \
  -l 'etc-streampark:' \
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
        --etc-streampark)
        ETC_STREAMPARK=$2 ; shift 2
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

LIB_DIR=${LIB_DIR:-/streampark}
ETC_STREAMPARK=${ETC_STREAMPARK:-/etc/streampark}

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/client
install -d -m 0755 $PREFIX/$LIB_DIR/lib
install -d -m 0755 $PREFIX/$LIB_DIR/plugins
install -d -m 0755 $PREFIX/$LIB_DIR/script
install -d -m 0755 $PREFIX/$LIB_DIR/temp
install -d -m 0755 $PREFIX/$LIB_DIR/temp/streampark
install -d -m 0755 $PREFIX/$ETC_STREAMPARK
install -d -m 0755 $PREFIX/$ETC_STREAMPARK/conf
install -d -m 0755 $PREFIX/var/log/streampark
install -d -m 0755 $PREFIX/var/run/streampark

cp -ra $BUILD_DIR/bin/* ${PREFIX}/${LIB_DIR}/bin/
cp -ra $BUILD_DIR/client/* ${PREFIX}/${LIB_DIR}/client/
cp -ra $BUILD_DIR/lib/* ${PREFIX}/${LIB_DIR}/lib/
cp -ra $BUILD_DIR/script/* ${PREFIX}/${LIB_DIR}/script/

ln -s $ETC_STREAMPARK/conf $PREFIX/$LIB_DIR/conf
ln -s /var/log/streampark $PREFIX/$LIB_DIR/logs

cp -ra $BUILD_DIR/conf/* ${PREFIX}/$ETC_STREAMPARK/conf/
