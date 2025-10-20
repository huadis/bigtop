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

%define elasticsearch_name elasticsearch
%define elasticsearch_pkg_name elasticsearch%{pkg_name_suffix}

%define lib_elasticsearch %{parent_dir}/%{elasticsearch_name}
%define etc_elasticsearch %{parent_dir}/%{elasticsearch_name}
%define config_elasticsearch %{parent_dir}/%{elasticsearch_name}/config

%define np_log_elasticsearch /var/log/%{elasticsearch_name}
%define np_run_elasticsearch /var/run/%{elasticsearch_name}

Name: %{elasticsearch_pkg_name}
Version: %{elasticsearch_version}
Release: %{elasticsearch_release}
Summary: Elasticsearch is a distributed RESTful search engine based on the Lucene library.
URL: https://www.elastic.co/
Group: Application/Internet
BuildArch: %{_arch}
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
License: ASL 2.0
Source0: elasticsearch-%{elasticsearch_base_version}.tar.gz
Source1: do-component-build
Source2: install_%{name}.sh
Requires: bigtop-utils >= 0.7

%description
Elasticsearch is a search engine based on the Lucene library.
It provides a distributed, multitenant-capable full-text search engine with
an HTTP web interface and schema-free JSON documents.

%prep
%setup -n elasticsearch-%{elasticsearch_base_version}

%build
env FULL_VERSION=%{elasticsearch_base_version} bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
  --build-dir=`pwd` \
  --prefix=$RPM_BUILD_ROOT \
  --distro-dir=$RPM_SOURCE_DIR \
  --lib-dir=%{lib_elasticsearch}

%pre
getent group elasticsearch >/dev/null || groupadd -r elasticsearch
getent passwd elasticsearch > /dev/null || useradd -c "Elasticsearch" -s /sbin/nologin -g elasticsearch -r -d %{np_run_elasticsearch} elasticsearch 2> /dev/null || :

%post

%preun

#######################
#### FILES SECTION ####
#######################
%files
%defattr(-,elasticsearch,elasticsearch,755)
%{lib_elasticsearch}
%{np_run_elasticsearch}
%{np_log_elasticsearch}
