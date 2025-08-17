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

%define streampark_name streampark
%define streampark_pkg_name streampark%{pkg_name_suffix}

%define lib_streampark %{parent_dir}/%{streampark_name}
%define etc_streampark %{parent_dir}/%{streampark_name}
%define config_streampark %{parent_dir}/%{streampark_name}/conf

%define np_var_run_streampark /var/run/%{streampark_name}
%define np_var_log_streampark /var/log/%{streampark_name}
%define np_etc_streampark /etc/streampark

%define alternatives_cmd alternatives

Name: %{streampark_pkg_name}
Version: %{streampark_version}
Release: %{streampark_release}
BuildArch: noarch
Summary: Apache StreamPark is a stream processing platform based on Flink
Group: Applications/System
License: Apache License 2.0
URL: https://streampark.apache.org/
Source0: apache-%{streampark_name}-%{version}-src.tar.gz
Source1: do-component-build
Source2: install_streampark.sh

%description
Apache StreamPark (incubating) is a one-stop stream processing platform based on Apache Flink,
which provides stream processing job development, deployment, operation, maintenance and
monitoring capabilities. It supports Flink SQL and DataStream, and integrates with various
data sources and sinks.

%package server
Summary: Apache StreamPark server component
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: hadoop-client >= 3.3.4
Requires: hive-client >= 3.1.3

%description server
This package contains the core server components of Apache StreamPark, including
the web server, job manager, and resource manager. It provides the main functionality
for stream processing job management and execution.

%package client
Summary: Apache StreamPark command-line client
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description client
This package provides command-line tools for interacting with Apache StreamPark server,
enabling users to submit, manage and monitor Flink jobs.

%prep
%setup -q -n apache-%{streampark_name}-%{version}-src

%build
env SCALA_VERSION="2.12" STREAMPARK_VERSION=%{streampark_base_version} bash %{SOURCE1}

%install
rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
    --prefix=$RPM_BUILD_ROOT \
    --source-dir=`pwd`/build \
    --install-dir=%{lib_streampark}

%pre
# 创建streampark用户和组
getent group streampark >/dev/null || groupadd -r streampark
getent passwd streampark >/dev/null || useradd -c "Streampark" -s /sbin/nologin -g streampark -r -d %{lib_streampark} streampark 2>/dev/null || :

%post
install --owner streampark --group streampark --directory --mode=0755 %{np_var_log_streampark}

%preun

%postun

%files
%defattr(644,root,root,755)
%{lib_streampark}
%{np_var_log_streampark}
%{np_var_run_streampark}
%{np_etc_streampark}
