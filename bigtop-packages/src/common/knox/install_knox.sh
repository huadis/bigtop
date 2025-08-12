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
     --build-dir=DIR             path to knox dist.dir
     --prefix=PREFIX             path to install into

  Optional options:
     --lib-dir=DIR               path to install knox home [/usr/lib/knox]
     --version=VERSION           knox version [2.0.0]
     --etc-knox=DIR             path to install knox conf [/etc/knox]
     ... [ see source for more similar options ]
  "
  exit 1
}

OPTS=$(getopt \
  -n $0 \
  -o '' \
  -l 'prefix:' \
  -l 'lib-dir:' \
  -l 'version:' \
  -l 'etc-knox:' \
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
        --version)
        VERSION=$2 ; shift 2
        ;;
        --etc-knox)
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

LIB_DIR=${LIB_DIR:-/knox}
VERSION=${VERSION:-2.0.0}
ETC_KNOX=${ETC_KNOX:-/etc/knox}

install -d -m 0755 $PREFIX/$LIB_DIR
install -d -m 0755 $PREFIX/$LIB_DIR/bin
install -d -m 0755 $PREFIX/$LIB_DIR/data
install -d -m 0755 $PREFIX/$LIB_DIR/dep
install -d -m 0755 $PREFIX/$LIB_DIR/ext
install -d -m 0755 $PREFIX/$LIB_DIR/lib
install -d -m 0755 $PREFIX/$LIB_DIR/samples
install -d -m 0755 $PREFIX/$LIB_DIR/templates
install -d -m 0755 $PREFIX/$ETC_KNOX
install -d -m 0755 $PREFIX/$ETC_KNOX/conf

tar -xvzf "$BUILD_DIR/knox-${VERSION}.tar.gz" -C "$BUILD_DIR/"
#cp -ra '/opt/bigtop/build/knox/rpm/BUILD/knox-2.0.0/dist/bin/*' /opt/bigtop/build/knox/rpm/BUILDROOT/knox_3_3_0-2.0.0-1.el8.aarch64//usr/hdp/3.3.0/knox/bin/
cp -ra $BUILD_DIR/knox-${VERSION}/bin/* ${PREFIX}/${LIB_DIR}/bin/
cp -ra $BUILD_DIR/knox-${VERSION}/data/* ${PREFIX}/${LIB_DIR}/data/
cp -ra $BUILD_DIR/knox-${VERSION}/dep/* ${PREFIX}/${LIB_DIR}/dep/
cp -ra $BUILD_DIR/knox-${VERSION}/ext/* ${PREFIX}/${LIB_DIR}/ext/
cp -ra $BUILD_DIR/knox-${VERSION}/lib/* ${PREFIX}/${LIB_DIR}/lib/
cp -ra $BUILD_DIR/knox-${VERSION}/samples/* ${PREFIX}/${LIB_DIR}/samples/
cp -ra $BUILD_DIR/knox-${VERSION}/templates/* ${PREFIX}/${LIB_DIR}/templates/

ln -s $ETC_KNOX/conf $PREFIX/$LIB_DIR/conf
ln -s /var/log/knox $PREFIX/$LIB_DIR/logs
ln -s /var/run/knox $PREFIX/$LIB_DIR/pids

cp -ra $BUILD_DIR/knox-${VERSION}/conf/* ${PREFIX}/$ETC_KNOX/conf/
