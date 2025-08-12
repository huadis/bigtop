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
%define ds_pkg_name %{ds_name}%{pkg_name_suffix}
%define ds_version 3.2.0
%define ds_user %{ds_name}
%define ds_group %{ds_name}

# 路径定义 (遵循 BigTop 目录规范)
%define parent_dir %{_prefix}
%define usr_lib_ds %{parent_dir}/%{ds_name}
%define etc_ds %{parent_dir}/etc/%{ds_name}
%define var_lib_ds %{parent_dir}/var/lib/%{ds_name}
%define var_log_ds /var/log/%{ds_name}
%define var_run_ds /var/run/%{ds_name}
%define bin_ds %{usr_lib_ds}/bin
%define conf_ds %{usr_lib_ds}/conf

# 系统路径映射
%define sys_etc_ds /etc/%{ds_name}

Name: %{ds_pkg_name}
Version: %{ds_version}
Release: 1%{?dist}
BuildArch: noarch
Summary: Apache DolphinScheduler is a distributed workflow scheduler
Group: Applications/System
License: Apache License 2.0
URL: https://dolphinscheduler.apache.org/
Source0: %{ds_name}-%{ds_version}-src.tar.gz
Source1: do-component-build
Source2: install_%{ds_name}.sh
Source3: %{ds_name}.service
Source4: %{ds_name}-env.sh

# 基础依赖
Requires: java-1.8.0-openjdk >= 1.8.0.302
Requires: mysql-connector-java >= 8.0.26
Requires: bigtop-utils >= 0.7
Requires: zookeeper >= 3.5.7
Requires: hadoop-client >= 2.7.3
BuildRequires: maven >= 3.6.3, git, tar, gzip

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

# 准备阶段
%prep
%setup -q -n %{ds_name}-%{ds_version}

# 构建阶段
%build
env DS_VERSION=%{ds_version} bash %{SOURCE1}

# 安装阶段
%install
rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
    --prefix=$RPM_BUILD_ROOT \
    --build-dir=`pwd`/target/%{ds_name}-%{ds_version} \
    --lib-dir=%{usr_lib_ds}

# 安装systemd服务
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/

# 配置环境变量
mkdir -p $RPM_BUILD_ROOT%{etc_ds}
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{etc_ds}/

# 创建符号链接
ln -s %{etc_ds} $RPM_BUILD_ROOT%{sys_etc_ds}

# 预安装脚本
%pre
# 创建用户和组
if ! getent group %{ds_group} >/dev/null; then
    groupadd -r %{ds_group}
fi
if ! getent passwd %{ds_user} >/dev/null; then
    useradd -r -g %{ds_group} -d %{var_lib_ds} \
            -s /sbin/nologin -c "Apache DolphinScheduler" %{ds_user}
fi

# 安装后脚本
%post
# 创建数据目录
mkdir -p %{var_lib_ds} %{var_log_ds} %{var_run_ds}
chown -R %{ds_user}:%{ds_group} %{var_lib_ds} %{var_log_ds} %{var_run_ds}

# 配置系统服务
systemctl daemon-reload
if [ $1 -eq 1 ]; then
    systemctl enable %{ds_name}.service >/dev/null 2>&1 || :
fi

# 初始化数据库（首次安装）
if [ $1 -eq 1 ]; then
    su -s /bin/sh -c "%{bin_ds}/tools/bin/upgrade-schema.sh" %{ds_user}
fi

# 预卸载脚本
%preun
if [ $1 -eq 0 ]; then
    # 完全卸载时停止服务
    systemctl stop %{ds_name}.service >/dev/null 2>&1 || :
    systemctl disable %{ds_name}.service >/dev/null 2>&1 || :
fi

# 卸载后脚本
%postun
if [ $1 -eq 0 ]; then
    # 清理残留文件
    rm -rf %{var_lib_ds}
    rm -rf %{sys_etc_ds}
fi

# 文件列表 - 主包
%files
%defattr(-,root,root)
%dir %{usr_lib_ds}
%{usr_lib_ds}/lib/
%{usr_lib_ds}/sql/
%{usr_lib_ds}/licenses/
%config(noreplace) %{conf_ds}/application.yaml
%config(noreplace) %{conf_ds}/logback.xml
%attr(755,root,root) %{bin_ds}/common.sh
%attr(755,root,root) %{bin_ds}/check-env.sh

# 文件列表 - server 子包
%files server
%defattr(-,root,root)
%{usr_lib_ds}/server/
%attr(755,root,root) %{bin_ds}/start-master.sh
%attr(755,root,root) %{bin_ds}/start-worker.sh
%attr(755,root,root) %{bin_ds}/stop-master.sh
%attr(755,root,root) %{bin_ds}/stop-worker.sh
%dir %attr(775,%{ds_user},%{ds_group}) %{var_lib_ds}
%dir %attr(775,%{ds_user},%{ds_group}) %{var_log_ds}

# 文件列表 - api 子包
%files api
%defattr(-,root,root)
%{usr_lib_ds}/api/
%{_unitdir}/%{ds_name}.service
%attr(755,root,root) %{bin_ds}/start-api.sh
%attr(755,root,root) %{bin_ds}/stop-api.sh
%dir %attr(775,%{ds_user},%{ds_group}) %{var_run_ds}

# 文件列表 - client 子包
%files client
%defattr(-,root,root)
%attr(755,root,root) %{bin_ds}/dsctl
%attr(755,root,root) %{bin_ds}/dolphinscheduler-daemon.sh
%{usr_lib_ds}/client/
%{sys_etc_ds}
%config(noreplace) %{etc_ds}/%{ds_name}-env.sh
