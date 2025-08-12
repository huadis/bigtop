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

# 基础变量定义（遵循 BigTop 命名规范）
%define streampark_name streampark
%define streampark_pkg_name %{streampark_name}%{pkg_name_suffix}
%define streampark_version %{version}
%define streampark_user %{streampark_name}
%define streampark_group %{streampark_name}

# 路径定义（符合 FHS 标准和 BigTop 目录规范）
%define parent_dir %{_prefix}
%define usr_lib_streampark %{parent_dir}/%{streampark_name}          # 主程序目录
%define etc_streampark %{parent_dir}/etc/%{streampark_name}          # 配置文件目录
%define var_lib_streampark %{parent_dir}/var/lib/%{streampark_name}  # 数据存储目录
%define var_log_streampark %{parent_dir}/var/log/%{streampark_name}  # 日志目录
%define var_run_streampark %{parent_dir}/var/run/%{streampark_name}  # 运行时目录（PID等）
%define bin_streampark %{usr_lib_streampark}/bin                      # 可执行脚本目录
%define conf_streampark %{usr_lib_streampark}/conf                    # 配置模板目录

# 系统标准路径映射（通过符号链接关联）
%define sys_etc_streampark /etc/%{streampark_name}
%define sys_var_log_streampark /var/log/%{streampark_name}
%define sys_var_run_streampark /var/run/%{streampark_name}

# 依赖管理配置
%define alternatives_cmd alternatives

# RPM 包基本信息
Name: %{streampark_pkg_name}
Version: 2.1.0
Release: 1%{?dist}
BuildArch: noarch
Summary: Apache StreamPark is a stream processing platform based on Flink
Group: Applications/System
License: Apache License 2.0
URL: https://streampark.apache.org/
Source0: %{streampark_name}-%{version}-src.tar.gz
Source1: do-component-build
Source2: install_streampark.sh
Source3: streampark-env.sh
Source4: streampark.service
Source5: application.yml

# 依赖项（基于 StreamPark 运行需求）
Requires: java-11-openjdk >= 11.0.20
Requires: bigtop-utils >= 0.14
Requires: flink >= 1.15.0
Requires: scala >= 2.12.15
Requires: mysql-connector-java >= 8.0.30
Requires: zookeeper >= 3.8.0
BuildRequires: maven >= 3.8.6, git, nodejs >= 14.0.0, npm >= 6.0.0, tar, gzip

%description
Apache StreamPark (incubating) is a one-stop stream processing platform based on Apache Flink,
which provides stream processing job development, deployment, operation, maintenance and
monitoring capabilities. It supports Flink SQL and DataStream, and integrates with various
data sources and sinks.

# 子包：server（核心服务组件）
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

# 子包：client（客户端工具）
%package client
Summary: Apache StreamPark command-line client
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description client
This package provides command-line tools for interacting with Apache StreamPark server,
enabling users to submit, manage and monitor Flink jobs.

# 准备阶段：解压源码包
%prep
%setup -q -n %{streampark_name}-%{version}

# 构建阶段：执行编译脚本
%build
bash %{SOURCE1}

# 安装阶段：执行安装脚本
%install
rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
    --prefix=$RPM_BUILD_ROOT \
    --source-dir=`pwd`/dist \
    --install-dir=%{usr_lib_streampark}

# 复制配置文件和环境变量模板
mkdir -p $RPM_BUILD_ROOT%{conf_streampark}
cp %{SOURCE3} $RPM_BUILD_ROOT%{conf_streampark}/streampark-env.sh
cp %{SOURCE5} $RPM_BUILD_ROOT%{conf_streampark}/application.yml

# 配置 systemd 服务
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/%{streampark_name}.service

# 创建符号链接（符合 FHS 标准）
mkdir -p $RPM_BUILD_ROOT%{sys_etc_streampark}
ln -s %{conf_streampark} $RPM_BUILD_ROOT%{sys_etc_streampark}/conf

# 预安装脚本：创建专用用户和组
%pre
# 创建 streampark 组
if ! getent group %{streampark_group} >/dev/null; then
    groupadd -r %{streampark_group}
fi
# 创建 streampark 用户（禁止登录，主目录为数据目录）
if ! getent passwd %{streampark_user} >/dev/null; then
    useradd -r -g %{streampark_group} -d %{var_lib_streampark} \
            -s /sbin/nologin -c "Apache StreamPark" %{streampark_user}
fi

# 安装后脚本：初始化目录和服务
%post
# 创建数据、日志、运行时目录
mkdir -p %{var_lib_streampark} %{var_log_streampark} %{var_run_streampark}
# 设置目录权限
chown -R %{streampark_user}:%{streampark_group} %{var_lib_streampark} %{var_log_streampark} %{var_run_streampark}
chmod -R 755 %{var_lib_streampark} %{var_log_streampark} %{var_run_streampark}

# 配置 systemd 服务
systemctl daemon-reload
if [ $1 -eq 1 ]; then
    # 首次安装时启用服务
    systemctl enable %{streampark_name}.service >/dev/null 2>&1 || :
fi

# 预卸载脚本：停止服务
%preun
if [ $1 -eq 0 ]; then
    # 完全卸载时停止并禁用服务
    systemctl stop %{streampark_name}.service >/dev/null 2>&1 || :
    systemctl disable %{streampark_name}.service >/dev/null 2>&1 || :
fi

# 卸载后脚本：清理残留文件
%postun
if [ $1 -eq 0 ]; then
    # 完全卸载时删除数据目录
    rm -rf %{var_lib_streampark}
    rm -rf %{sys_etc_streampark}
fi

# 主包文件列表
%files
%defattr(-,root,root)
%dir %{usr_lib_streampark}
%{usr_lib_streampark}/lib/
%{usr_lib_streampark}/static/
%{usr_lib_streampark}/licenses/
%config(noreplace) %{conf_streampark}/streampark-env.sh
%config(noreplace) %{conf_streampark}/application.yml
%attr(755,root,root) %{bin_streampark}/common.sh

# Server 子包文件列表
%files server
%defattr(-,root,root)
%{usr_lib_streampark}/server/
%attr(755,root,root) %{bin_streampark}/start-server.sh
%attr(755,root,root) %{bin_streampark}/stop-server.sh
%{_unitdir}/%{streampark_name}.service
%dir %attr(755,%{streampark_user},%{streampark_group}) %{var_lib_streampark}
%dir %attr(755,%{streampark_user},%{streampark_group}) %{var_log_streampark}
%dir %attr(755,%{streampark_user},%{streampark_group}) %{var_run_streampark}

# Client 子包文件列表
%files client
%defattr(-,root,root)
%attr(755,root,root) %{bin_streampark}/streampark-cli
%{usr_lib_streampark}/client/
%{sys_etc_streampark}/conf
