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

%define dinky_name dinky
%define dinky_pkg_name dinky%{pkg_name_suffix}

%define lib_dinky %{parent_dir}/%{dinky_name}
%define etc_dinky %{parent_dir}/%{dinky_name}
%define config_dinky %{parent_dir}/%{dinky_name}/conf

%define np_var_run_dinky /var/run/%{dinky_name}
%define np_var_log_dinky /var/log/%{dinky_name}
%define np_etc_dinky /etc/dinky

Name: %{dinky_pkg_name}
Version: %{dinky_version}
Release: %{dinky_release}
BuildArch:      noarch
Summary:        Dinky is a real-time data development platform based on Apache Flink, enabling agile data development, deployment and operation.
URL:            https://www.dinky.org.cn
Group:          Applications/Internet
License:        Apache License 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0:        %{dinky_name}-%{dinky_base_version}.tar.gz
Source1:        do-component-build
Source2:        install_dinky.sh
Requires: bigtop-utils >= 0.7
Requires(pre):  shadow-utils

%description
Dinky is a real-time data development platform based on Apache Flink,
enabling agile data development, deployment and operation.

%prep
%setup -q -n %{dinky_name}-%{dinky_base_version}

%build
bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=`pwd`/build \
  --lib-dir=%{lib_dinky}

%pre
getent group dinky >/dev/null || groupadd -r dinky
getent passwd dinky >/dev/null || useradd -c "Dinky" -s /sbin/nologin -g dinky -r -d %{lib_dinky} dinky 2>/dev/null || :

%post
install --owner dinky --group dinky --directory --mode=0755 %{np_var_log_dinky}

%preun

%postun

%files
%defattr(-,dinky,dinky,755)
%{lib_dinky}
%{np_var_log_dinky}
%{np_var_run_dinky}
%{np_etc_dinky}
