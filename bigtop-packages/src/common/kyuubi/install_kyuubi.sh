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
     --build-dir=DIR             path to kyuubi dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --lib-dir=DIR               path to install kyuubi home [/usr/lib/kyuubi]
     --etc-kyuubi=DIR             path to install kyuubi conf [/etc/kyuubi]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'lib-dir:' \
  -l 'etc-kyuubi:' \
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
        --etc-kyuubi)
        ETC_KNOX=$2 ; shift 2
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

LIB_DIR=${LIB_DIR:-/kyuubi}
ETC_KYUUBI=${ETC_KYUUBI:-/etc/kyuubi}

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/beeline-jars
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/charts
install -d -m 0755 $PREFIX/$LIB_DIR/db-scripts
install -d -m 0755 $PREFIX/$LIB_DIR/docker
install -d -m 0755 $PREFIX/$LIB_DIR/externals
install -d -m 0755 $PREFIX/$LIB_DIR/jars
install -d -m 0755 $PREFIX/$LIB_DIR/web-ui
install -d -m 0755 $PREFIX/$LIB_DIR/work
install -d -m 0755 $PREFIX/$ETC_KYUUBI
install -d -m 0755 $PREFIX/$ETC_KYUUBI/conf
install -d -m 0755 $PREFIX/var/log/kyuubi
install -d -m 0755 $PREFIX/var/run/kyuubi

cp -ra $BUILD_DIR/beeline-jars/* ${PREFIX}/${LIB_DIR}/beeline-jars/
cp -ra $BUILD_DIR/bin/* ${PREFIX}/${LIB_DIR}/bin/
cp -ra $BUILD_DIR/charts/* ${PREFIX}/${LIB_DIR}/charts/
cp -ra $BUILD_DIR/db-scripts/* ${PREFIX}/${LIB_DIR}/db-scripts/
cp -ra $BUILD_DIR/docker/* ${PREFIX}/${LIB_DIR}/docker/
cp -ra $BUILD_DIR/externals/* ${PREFIX}/${LIB_DIR}/externals/
cp -ra $BUILD_DIR/jars/* ${PREFIX}/${LIB_DIR}/jars/
cp -ra $BUILD_DIR/web-ui/* ${PREFIX}/${LIB_DIR}/web-ui/

ln -s $ETC_KYUUBI/conf $PREFIX/$LIB_DIR/conf
ln -s /var/log/kyuubi $PREFIX/$LIB_DIR/logs
ln -s /var/run/kyuubi $PREFIX/$LIB_DIR/pid

cp -ra $BUILD_DIR/conf/* ${PREFIX}/$ETC_KYUUBI/conf/
