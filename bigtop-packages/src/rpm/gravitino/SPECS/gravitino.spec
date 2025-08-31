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

%define gravitino_name gravitino
%define gravitino_pkg_name gravitino%{pkg_name_suffix}

%define lib_gravitino %{parent_dir}/%{gravitino_name}
%define etc_gravitino %{parent_dir}/%{gravitino_name}

%define np_var_run_gravitino /var/run/%{gravitino_name}
%define np_var_log_gravitino /var/log/%{gravitino_name}
%define np_etc_gravitino /etc/gravitino

Name: %{gravitino_pkg_name}
Version: %{gravitino_version}
Release: %{gravitino_release}
BuildArch:      noarch
Summary:        The world's fastest open query engine for sub-second analytics both on and off the data lakehouse. With the flexibility to support nearly any scenario, StarRocks provides best-in-class performance for multi-dimensional analytics, real-time analytics, and ad-hoc queries. A Linux Foundation project.
URL:            https://gravitino.apache.org/
Group:          Applications/Internet
License:        Apache License 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0:        %{gravitino_name}-%{gravitino_base_version}-src.tar.gz
Source1:        do-component-build
Source2:        install_gravitino.sh
Requires: bigtop-utils >= 0.7

%description
The world's fastest open query engine for sub-second analytics both on and off the data lakehouse.
With the flexibility to support nearly any scenario,
StarRocks provides best-in-class performance for multi-dimensional analytics, real-time analytics, and ad-hoc queries.
A Linux Foundation project.

%prep
%setup -q -n apache-%{gravitino_name}-%{gravitino_base_version}-src

%build
bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=`pwd`/build \
  --lib-dir=%{lib_gravitino}

%pre
getent group gravitino >/dev/null || groupadd -r gravitino
getent passwd gravitino >/dev/null || useradd -c "Gravitino" -s /sbin/nologin -g gravitino -r -d %{lib_gravitino} gravitino 2>/dev/null || :

%post
install --owner gravitino --group gravitino --directory --mode=0755 %{np_var_log_gravitino}

%preun

%postun

%files
%defattr(644,gravitino,gravitino,755)
%{lib_gravitino}
%{np_var_log_gravitino}
%{np_var_run_gravitino}
%{np_etc_gravitino}
