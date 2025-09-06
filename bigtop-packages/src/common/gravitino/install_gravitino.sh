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
     --src-dir=DIR               path to gravitino source.dir
     --build-dir=DIR             path to gravitino dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --lib-dir=DIR               path to install gravitino home [/usr/lib/gravitino]
     --etc-gravitino=DIR             path to install gravitino conf [/etc/gravitino]
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
  -l 'etc-gravitino:' \
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
        --etc-gravitino)
        ETC_GRAVITINO=$2 ; shift 2
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

LIB_DIR=${LIB_DIR:-/gravitino}
ETC_GRAVITINO=${ETC_GRAVITINO:-/etc/gravitino}

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/authorizations
install -d -m 0755 $PREFIX/$LIB_DIR/auxlib
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/catalogs
install -d -m 0755 $PREFIX/$LIB_DIR/data
install -d -m 0755 $PREFIX/$LIB_DIR/iceberg-rest-server
install -d -m 0755 $PREFIX/$LIB_DIR/libs
install -d -m 0755 $PREFIX/$LIB_DIR/scripts
install -d -m 0755 $PREFIX/$LIB_DIR/web
install -d -m 0755 $PREFIX/$ETC_GRAVITINO
install -d -m 0755 $PREFIX/$ETC_GRAVITINO/conf
install -d -m 0755 $PREFIX/var/log/gravitino
install -d -m 0755 $PREFIX/var/run/gravitino

cp -ra $BUILD_DIR/authorizations/* ${PREFIX}/${LIB_DIR}/authorizations
cp -ra $BUILD_DIR/auxlib/* ${PREFIX}/${LIB_DIR}/auxlib
cp -ra $BUILD_DIR/bin/* ${PREFIX}/${LIB_DIR}/bin
cp -ra $BUILD_DIR/catalogs/* ${PREFIX}/${LIB_DIR}/catalogs
cp -ra $BUILD_DIR/data/* ${PREFIX}/${LIB_DIR}/data
cp -ra $BUILD_DIR/iceberg-rest-server/* ${PREFIX}/${LIB_DIR}/iceberg-rest-server
cp -ra $BUILD_DIR/libs/* ${PREFIX}/${LIB_DIR}/libs
cp -ra $BUILD_DIR/scripts/* ${PREFIX}/${LIB_DIR}/scripts/
cp -ra $BUILD_DIR/web/* ${PREFIX}/${LIB_DIR}/web/

ln -s $ETC_GRAVITINO/conf $PREFIX/$LIB_DIR/config
ln -s /var/log/gravitino $PREFIX/$LIB_DIR/logs
ln -s /var/run/gravitino $PREFIX/$LIB_DIR/pid
cp -ra $BUILD_DIR/conf/* ${PREFIX}/$ETC_GRAVITINO/conf/
