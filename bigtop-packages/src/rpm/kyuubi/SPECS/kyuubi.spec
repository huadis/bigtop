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

%define kyuubi_name kyuubi
%define kyuubi_pkg_name kyuubi%{pkg_name_suffix}

%define lib_kyuubi %{parent_dir}/%{kyuubi_name}
%define etc_kyuubi %{parent_dir}/%{kyuubi_name}
%define config_kyuubi %{parent_dir}/%{kyuubi_name}/conf

%define kyuubi_services server
%define np_var_run_kyuubi /var/run/%{kyuubi_name}
%define np_var_log_kyuubi /var/log/%{kyuubi_name}
%define np_etc_kyuubi /etc/kyuubi

Name: %{kyuubi_pkg_name}
Version: %{kyuubi_version}
Release: %{kyuubi_release}
BuildArch:      noarch
Summary:        Apache Kyuubi is a distributed and multi-tenant gateway to provide SQL service over various computing frameworks.
URL:            https://kyuubi.apache.org/
Group:          Applications/Internet
License:        Apache License 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0:        apache-%{kyuubi_name}-%{kyuubi_base_version}-source.tgz
Source1:        do-component-build
Source2:        install_kyuubi.sh
Source3:        kyuubi.service
Source4:        kyuubi-env.sh
Requires:       hadoop >= 3.0.0
Requires:       spark >= 3.0.0
Requires(pre):  shadow-utils

%description
Apache Kyuubi is a distributed and multi-tenant gateway to provide SQL service over various computing frameworks.
It aims to make the Data Lakehouse accessible via SQL based tools, and decouple the computing and storage.

%prep
%setup -q -n apache-%{kyuubi_name}-%{kyuubi_base_version}-source

%build
env KYUUBI_VERSION=%{kyuubi_base_version} bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=`pwd`/build \
  --lib-dir=%{lib_kyuubi}

%pre
# 创建kyuubi用户和组
getent group kyuubi >/dev/null || groupadd -r kyuubi
getent passwd kyuubi >/dev/null || useradd -c "Kyuubi" -s /sbin/nologin -g kyuubi -r -d %{lib_kyuubi} kyuubi 2>/dev/null || :

%post
install --owner kyuubi --group kyuubi --directory --mode=0755 %{np_var_log_kyuubi}

%preun

%postun

%files
%defattr(644,kyuubi,kyuubi,755)
%{lib_kyuubi}
%{np_var_log_kyuubi}
%{np_var_run_kyuubi}
%{np_etc_kyuubi}
