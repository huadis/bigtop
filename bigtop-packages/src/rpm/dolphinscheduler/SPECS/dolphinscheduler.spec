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
# See the License for the specific language governing governing permissions and
# limitations under the License.

# 基础定义
%define ds_name dolphinscheduler
%define ds_version %{dolphinscheduler_version}
%define ds_release %{dolphinscheduler_release}
%define ds_pkg_name %{ds_name}%{pkg_name_suffix}
%define etc_ds %{parent_dir}/etc/%{ds_name}
%define usr_lib_ds %{parent_dir}/%{ds_name}

%define ds_user %{ds_name}
%define ds_group %{ds_name}

%define np_var_log_ds /var/log/%{ds_name}
%define np_var_run_ds /var/run/%{ds_name}
%define np_etc_ds /etc/%{ds_name}

%define alternatives_cmd alternatives

Name: %{ds_pkg_name}
Version: %{ds_version}
Release: %{ds_release}
BuildArch: noarch
Summary: Apache DolphinScheduler is a distributed workflow scheduler
Group: Applications/System
License: Apache License 2.0
URL: https://dolphinscheduler.apache.org/
Source0: apache-%{ds_name}-%{ds_version}-src.tar.gz
Source1: do-component-build
Source2: install_%{ds_name}.sh

%description
Apache DolphinScheduler is a distributed and easy-to-expand visual workflow scheduler system,
which is dedicated to solving the complex dependencies in data processing,
making the scheduling system out of the box for data processing.

# 子包定义
%package server
Summary: Apache DolphinScheduler server components
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description server
This package contains the core server components of Apache DolphinScheduler,
including master server and worker server.

%package api
Summary: Apache DolphinScheduler API service
Group: Applications/System
Requires: %{name}-server = %{version}-%{release}
Requires: tomcat >= 8.5.63

%description api
This package contains the API service and web UI of Apache DolphinScheduler.

%package client
Summary: Apache DolphinScheduler command line client
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description client
This package provides command line tools for interacting with Apache DolphinScheduler.

%prep
%setup -q -n apache-%{ds_name}-%{ds_version}-src

# 构建阶段
%build
bash %{SOURCE1}

# 安装阶段
%install
rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
    --prefix=$RPM_BUILD_ROOT \
    --build-dir=`pwd`/build \
    --lib-dir=%{usr_lib_ds}

%pre
# 创建knox用户和组
getent group %{ds_user} >/dev/null || groupadd -r %{ds_user}
getent passwd %{ds_user} >/dev/null || useradd -c "DolphinScheduler" -s /sbin/nologin -g %{ds_group} -r -d %{usr_lib_ds} %{ds_name} 2>/dev/null || :


%post
install --owner %{ds_user} --group %{ds_group} --directory --mode=0755 %{np_var_log_ds}

%preun

%postun

# 文件列表 - 主包
%files
%defattr(-,dolphinscheduler,dolphinscheduler,755)
%{usr_lib_ds}
%{np_var_log_ds}
%{np_var_run_ds}
%{np_etc_ds}
