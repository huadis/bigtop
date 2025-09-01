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

%define dataease_name dataease
%define dataease_pkg_name dataease%{pkg_name_suffix}

%define lib_dataease %{parent_dir}/%{dataease_name}
%define etc_dataease %{parent_dir}/%{dataease_name}
%define config_dataease %{parent_dir}/%{dataease_name}/conf

%define np_var_run_dataease /var/run/%{dataease_name}
%define np_var_log_dataease /var/log/%{dataease_name}
%define np_etc_dataease /etc/dataease

Name: %{dataease_pkg_name}
Version: %{dataease_version}
Release: %{dataease_release}
BuildArch:      noarch
Summary:        DataEase is an open-source data visualization and analysis tool that helps users quickly analyze data and gain insights into business trends, thereby enabling business improvement and optimization.
URL:            https://dataease.io
Group:          Applications/Internet
License:        Apache License 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0:        %{dataease_name}-%{dataease_base_version}.tar.gz
Source1:        do-component-build
Source2:        install_dataease.sh
Requires: bigtop-utils >= 0.7

%description
DataEase is an open-source data visualization and analysis tool that helps users quickly analyze data and gain insights into business trends,
thereby enabling business improvement and optimization.

%prep
%setup -q -n %{dataease_name}-%{dataease_base_version}

%build
bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --distro-dir=$RPM_SOURCE_DIR \
  --src-dir=`pwd` \
  --build-dir=`pwd`/build \
  --lib-dir=%{lib_dataease}

%pre
getent group dataease >/dev/null || groupadd -r dataease
getent passwd dataease >/dev/null || useradd -c "DataEase" -s /sbin/nologin -g dataease -r -d %{lib_dataease} dataease 2>/dev/null || :

%post
install --owner dataease --group dataease --directory --mode=0755 %{np_var_log_dataease}

%preun

%postun

%files
%defattr(-,dataease,dataease,755)
%{lib_dataease}
%{np_var_log_dataease}
%{np_var_run_dataease}
%{np_etc_dataease}
