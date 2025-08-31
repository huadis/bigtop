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

%define starrocks_name starrocks
%define starrocks_pkg_name starrocks%{pkg_name_suffix}

%define lib_starrocks %{parent_dir}/%{starrocks_name}
%define etc_starrocks %{parent_dir}/%{starrocks_name}
%define config_starrocks %{parent_dir}/%{starrocks_name}/conf

%define np_var_run_starrocks /var/run/%{starrocks_name}
%define np_var_log_starrocks /var/log/%{starrocks_name}
%define np_etc_starrocks /etc/starrocks

Name: %{starrocks_pkg_name}
Version: %{starrocks_version}
Release: %{starrocks_release}
BuildArch:      noarch
Summary:        The world's fastest open query engine for sub-second analytics both on and off the data lakehouse. With the flexibility to support nearly any scenario, StarRocks provides best-in-class performance for multi-dimensional analytics, real-time analytics, and ad-hoc queries. A Linux Foundation project.
URL:            https://www.starrocks.org.cn
Group:          Applications/Internet
License:        Apache License 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0:        %{starrocks_name}-%{starrocks_base_version}.tar.gz
Source1:        do-component-build
Source2:        install_starrocks.sh
Requires: bigtop-utils >= 0.7
Requires(pre):  shadow-utils

%description
The world's fastest open query engine for sub-second analytics both on and off the data lakehouse.
With the flexibility to support nearly any scenario,
StarRocks provides best-in-class performance for multi-dimensional analytics,
real-time analytics, and ad-hoc queries. A Linux Foundation project.

%prep
%setup -q -n %{starrocks_name}-%{starrocks_base_version}

%build
bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=`pwd`/build \
  --lib-dir=%{lib_starrocks}

%pre
getent group starrocks >/dev/null || groupadd -r starrocks
getent passwd starrocks >/dev/null || useradd -c "StarRocks" -s /sbin/nologin -g starrocks -r -d %{lib_starrocks} starrocks 2>/dev/null || :

%post
install --owner starrocks --group starrocks --directory --mode=0755 %{np_var_log_starrocks}

%preun

%postun

%files
%defattr(644,starrocks,starrocks,755)
%{lib_starrocks}
%{np_var_log_starrocks}
%{np_var_run_starrocks}
%{np_etc_starrocks}
