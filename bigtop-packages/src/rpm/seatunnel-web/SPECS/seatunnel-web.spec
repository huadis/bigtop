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

%define seatunnel_web_name seatunnel-web
%define seatunnel_web_pkg_name seatunnel%{pkg_name_suffix}
%define hadoop_pkg_name hadoop%{pkg_name_suffix}
%define spark_pkg_name spark%{pkg_name_suffix}

%define lib_seatunnel_web %{parent_dir}/%{seatunnel_web_name}
%define etc_seatunnel_web %{parent_dir}/%{seatunnel_web_name}
%define config_seatunnel_web %{parent_dir}/%{seatunnel_web_name}/conf

%define np_var_run_seatunnel_web /var/run/%{seatunnel_web_name}
%define np_var_log_seatunnel_web /var/log/%{seatunnel_web_name}
%define np_etc_seatunnel_web /etc/seatunnel-web

Name: %{seatunnel_web_pkg_name}
Version: %{seatunnel_web_version}
Release: %{seatunnel_web_release}
BuildArch:      noarch
Summary:        Apache SeaTunnel is a distributed and multi-tenant gateway to provide SQL service over various computing frameworks.
URL:            https://seatunnel.apache.org/
Group:          Applications/Internet
License:        Apache License 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0:        apache-%{seatunnel_web_name}-%{seatunnel_web_base_version}-src.tar.gz
Source1:        do-component-build
Source2:        install_seatunnel.sh
Requires: bigtop-utils >= 0.7, %{hadoop_pkg_name}-client, %{hadoop_pkg_name}-yarn, %{spark_pkg_name}
Requires(pre):  shadow-utils

%description
Apache SeaTunnel is an open-source distributed data integration platform that supports
batch and streaming data synchronization. It provides rich connectors for databases,
message queues, and data warehouses, enabling efficient data migration and transformation.

%prep
%setup -q -n apache-%{seatunnel_web_name}-%{seatunnel_web_base_version}-src

%build
bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=`pwd`/build \
  --lib-dir=%{lib_seatunnel_web}

%pre
getent group seatunnel >/dev/null || groupadd -r seatunnel
getent passwd seatunnel >/dev/null || useradd -c "SeaTunnel" -s /sbin/nologin -g seatunnel -r -d %{lib_seatunnel_web} seatunnel 2>/dev/null || :

%post
install --owner seatunnel --group seatunnel --directory --mode=0755 %{np_var_log_seatunnel_web}

%preun

%postun

%files web
%defattr(-,seatunnel,seatunnel,755)
%{lib_seatunnel_web}
%{np_var_log_seatunnel_web}
%{np_var_run_seatunnel_web}
%{np_etc_seatunnel_web}
