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

%define knox_name knox
%define knox_pkg_name knox%{pkg_name_suffix}

%define etc_default %{parent_dir}/etc/default

%define usr_lib_knox %{parent_dir}/%{knox_name}
%define etc_knox %{parent_dir}/etc/%{knox_name}

%define np_var_log_knox /var/log/%{knox_name}
%define np_var_run_knox /var/run/%{knox_name}
%define np_etc_knox /etc/%{knox_name}

%define alternatives_cmd alternatives

Name: %{knox_pkg_name}
Version: %{knox_version}
Release: %{knox_release}
BuildArch: noarch
Summary: Apache Knox is a secure gateway for Hadoop ecosystem
URL: http://knox.apache.org/
Group: Development/Libraries
License: ASL 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0: %{knox_name}-%{knox_base_version}-src.zip
Source1: do-component-build
Source2: install_%{knox_name}.sh
Requires: bigtop-utils >= 0.7, openssl
Requires(preun): /sbin/service

%description
Apache Knox provides a single point of authentication and access for Apache Hadoop services.
It acts as a reverse proxy, simplifying secure access to Hadoop clusters by consolidating
authentication, authorization, and audit capabilities. Knox supports multiple authentication
mechanisms (LDAP, Kerberos, etc.) and provides a centralized gateway for HDFS, YARN, Hive,
HBase, and other Hadoop services.

%package server
Summary: Apache Knox gateway server
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description server
This package contains the Apache Knox gateway server, including init scripts and service configuration.
It provides the core reverse proxy functionality for secure Hadoop ecosystem access.

%prep
%setup -q -n %{knox_name}-%{knox_base_version}
#BIGTOP_PATCH_COMMANDS

%build
env KNOX_VERSION=%{knox_base_version} bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=`pwd`/target/%{knox_base_version} \
  --lib-dir=%{usr_lib_knox}

%__install -d -m 0755 $RPM_BUILD_ROOT/%{np_var_log_knox}
%__install -d -m 0755 $RPM_BUILD_ROOT/%{np_var_run_knox}

%pre
# 创建knox用户和组
getent group knox >/dev/null || groupadd -r knox
getent passwd knox >/dev/null || useradd -c "Knox Gateway" -s /sbin/nologin -g knox -r -d %{usr_lib_knox} knox 2>/dev/null || :

%post
install --owner knox --group knox --directory --mode=0755 %{np_var_log_knox}

%preun

%postun

%files
%defattr(644,root,root,755)
%{usr_lib_knox}
%defattr(755,root,root)
%{usr_lib_knox}/bin/*.sh
%defattr(644,knox,knox,755)
%config(noreplace) %{usr_lib_knox}/data
%{np_var_log_knox}
%{np_var_run_knox}
%{np_etc_knox}

%service_macro server
