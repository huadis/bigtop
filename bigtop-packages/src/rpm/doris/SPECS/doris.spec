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

%define doris_name doris
%define doris_pkg_name doris%{pkg_name_suffix}

%define lib_doris %{parent_dir}/%{doris_name}
%define etc_doris %{parent_dir}/%{doris_name}
%define config_doris %{parent_dir}/%{doris_name}/conf

%define np_var_run_doris /var/run/%{doris_name}
%define np_var_log_doris /var/log/%{doris_name}
%define np_etc_doris /etc/doris

Name: %{doris_pkg_name}
Version: %{doris_version}
Release: %{doris_release}
BuildArch:      noarch
Summary:        Dinky is a real-time data development platform based on Apache Flink, enabling agile data development, deployment and operation.
URL:            https://www.doris.org.cn
Group:          Applications/Internet
License:        Apache License 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0:        apache-%{doris_name}-%{doris_base_version}-src.tar.gz
Source1:        do-component-build
Source2:        install_doris.sh
Requires: bigtop-utils >= 0.7
Requires(pre):  shadow-utils

%description
Dinky is a real-time data development platform based on Apache Flink,
enabling agile data development, deployment and operation.

%prep
%setup -q -n %{doris_name}-%{doris_base_version}

%build
bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=`pwd`/build \
  --lib-dir=%{lib_doris}

%pre
getent group doris >/dev/null || groupadd -r doris
getent passwd doris >/dev/null || useradd -c "Dinky" -s /sbin/nologin -g doris -r -d %{lib_doris} doris 2>/dev/null || :

%post
install --owner doris --group doris --directory --mode=0755 %{np_var_log_doris}

%preun

%postun

%files
%defattr(-,doris,doris,755)
%{lib_doris}
%{np_var_log_doris}
%{np_var_run_doris}
%{np_etc_doris}
