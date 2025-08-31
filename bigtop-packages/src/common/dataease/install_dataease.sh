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
     --distro-dir=DIR            path to distro specific files (debian/RPM)
     --src-dir=DIR               path to dataease source.dir
     --build-dir=DIR             path to dataease dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --lib-dir=DIR               path to install dataease home [/usr/lib/dataease]
     --etc-dataease=DIR             path to install dataease conf [/etc/dataease]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'distro-dir:' \
  -l 'prefix:' \
  -l 'lib-dir:' \
  -l 'etc-dataease:' \
  -l 'src-dir:' \
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
        --src-dir)
        SRC_DIR=$2 ; shift 2
        ;;
        --lib-dir)
        LIB_DIR=$2 ; shift 2
        ;;
        --etc-dataease)
        ETC_DATAEASE=$2 ; shift 2
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

for var in PREFIX BUILD_DIR SRC_DIR; do
  if [ -z "$(eval "echo \$$var")" ]; then
    echo Missing param: $var
    usage
  fi
done

LIB_DIR=${LIB_DIR:-/dataease}
ETC_DATAEASE=${ETC_DATAEASE:-/etc/dataease}

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/lib
install -d -m 0755 $PREFIX/$LIB_DIR/drivers
install -d -m 0755 $PREFIX/$LIB_DIR/cache
install -d -m 0755 $PREFIX/$LIB_DIR/data
install -d -m 0755 $PREFIX/$LIB_DIR/data/map
install -d -m 0755 $PREFIX/$LIB_DIR/data/static-resource
install -d -m 0755 $PREFIX/$ETC_DATAEASE
install -d -m 0755 $PREFIX/$ETC_DATAEASE/conf
install -d -m 0755 $PREFIX/var/log/dataease
install -d -m 0755 $PREFIX/var/run/dataease

cp -ra $BUILD_DIR/* ${PREFIX}/${LIB_DIR}/lib/
cp -ra $SRC_DIR/drivers/* ${PREFIX}/${LIB_DIR}/drivers
cp -ra $SRC_DIR/mapFiles/* ${PREFIX}/${LIB_DIR}/data/map/
cp -ra $SRC_DIR/staticResource/* ${PREFIX}/${LIB_DIR}/data/static-resource/

ln -s $ETC_DATAEASE/conf $PREFIX/$LIB_DIR/config
ln -s /var/log/dataease $PREFIX/$LIB_DIR/logs
ln -s /var/run/dataease $PREFIX/$LIB_DIR/pid
cp -ra $DISTRO_DIR/application.yml ${PREFIX}/$ETC_DATAEASE/conf/
