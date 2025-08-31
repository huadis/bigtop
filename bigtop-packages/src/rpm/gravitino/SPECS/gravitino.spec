# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional additional information regarding copyright ownership.
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
%define gravitino_name gravitino
%define gravitino_pkg_name %{gravitino_name}%{pkg_name_suffix}
%define gravitino_version %{version}
%define gravitino_user %{gravitino_name}
%define gravitino_group %{gravitino_name}

# 路径定义（符合 FHS 标准和 BigTop 目录规范）
%define parent_dir %{_prefix}
%define usr_lib_gravitino %{parent_dir}/%{gravitino_name}          # 主程序目录
%define etc_gravitino %{parent_dir}/etc/%{gravitino_name}          # 配置文件目录
%define var_lib_gravitino %{parent_dir}/var/lib/%{gravitino_name}  # 数据存储目录
%define var_log_gravitino %{parent_dir}/var/log/%{gravitino_name}  # 日志目录
%define var_run_gravitino %{parent_dir}/var/run/%{gravitino_name}  # 运行时目录（PID等）
%define bin_gravitino %{usr_lib_gravitino}/bin                      # 可执行脚本目录
%define conf_gravitino %{usr_lib_gravitino}/conf                    # 配置模板目录

# 系统标准路径映射（通过符号链接关联）
%define sys_etc_gravitino /etc/%{gravitino_name}
%define sys_var_log_gravitino /var/log/%{gravitino_name}
%define sys_var_run_gravitino /var/run/%{gravitino_name}

# 依赖管理配置
%define alternatives_cmd alternatives

# RPM 包基本信息
Name: %{gravitino_pkg_name}
Version: %{gravitino_version}
Release: %{gravitino_release}
BuildArch: noarch
Summary: Apache Gravitino is a metadata lake management system
Group: Applications/System
License: Apache License 2.0
URL: https://gravitino.apache.org/
Source0: %{gravitino_name}-%{version}-src.tar.gz
Source1: do-component-build
Source2: install_gravitino.sh
Requires: bigtop-utils >= 0.14

%description
Apache Gravitino is an open-source metadata lake management system that provides
a unified metadata management service for data lakes. It supports multiple
metadata types (catalogs, schemas, tables, etc.) and integrates with various
data processing engines such as Spark, Flink, and Trino.

# 子包：server（核心服务组件）
%package server
Summary: Apache Gravitino server component
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: hadoop-client >= 3.3.4

%description server
This package contains the core server components of Apache Gravitino, including
the metadata service, API service, and coordination modules. It handles metadata
storage, retrieval, and synchronization across distributed systems.

# 子包：client（客户端工具）
%package client
Summary: Apache Gravitino command-line client
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description client
This package provides command-line tools and libraries for interacting with
Apache Gravitino server, enabling users to manage metadata objects such as
catalogs, schemas, and tables.

# 准备阶段：解压源码包
%prep
%setup -q -n %{gravitino_name}-%{version}-src

# 构建阶段：执行编译脚本
%build
bash %{SOURCE1}

# 安装阶段：执行安装脚本
%install
rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
    --prefix=$RPM_BUILD_ROOT \
    --source-dir=`pwd`/dist \
    --install-dir=%{usr_lib_gravitino}

# 复制配置文件和环境变量模板
mkdir -p $RPM_BUILD_ROOT%{conf_gravitino}
cp %{SOURCE3} $RPM_BUILD_ROOT%{conf_gravitino}/gravitino-env.sh
cp %{SOURCE5} $RPM_BUILD_ROOT%{conf_gravitino}/gravitino-server.conf

# 配置 systemd 服务
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/%{gravitino_name}.service

# 创建符号链接（符合 FHS 标准）
mkdir -p $RPM_BUILD_ROOT%{sys_etc_gravitino}
ln -s %{conf_gravitino} $RPM_BUILD_ROOT%{sys_etc_gravitino}/conf

# 预安装脚本：创建专用用户和组
%pre
# 创建 gravitino 组
if ! getent group %{gravitino_group} >/dev/null; then
    groupadd -r %{gravitino_group}
fi
# 创建 gravitino 用户（禁止登录，主目录为数据目录）
if ! getent passwd %{gravitino_user} >/dev/null; then
    useradd -r -g %{gravitino_group} -d %{var_lib_gravitino} \
            -s /sbin/nologin -c "Apache Gravitino" %{gravitino_user}
fi

# 安装后脚本：初始化目录和服务
%post
# 创建数据、日志、运行时目录
mkdir -p %{var_lib_gravitino} %{var_log_gravitino} %{var_run_gravitino}
# 设置目录权限
chown -R %{gravitino_user}:%{gravitino_group} %{var_lib_gravitino} %{var_log_gravitino} %{var_run_gravitino}
chmod -R 755 %{var_lib_gravitino} %{var_log_gravitino} %{var_run_gravitino}

# 配置 systemd 服务
systemctl daemon-reload
if [ $1 -eq 1 ]; then
    # 首次安装时启用服务
    systemctl enable %{gravitino_name}.service >/dev/null 2>&1 || :
fi

# 预卸载脚本：停止服务
%preun
if [ $1 -eq 0 ]; then
    # 完全卸载时停止并禁用服务
    systemctl stop %{gravitino_name}.service >/dev/null 2>&1 || :
    systemctl disable %{gravitino_name}.service >/dev/null 2>&1 || :
fi

# 卸载后脚本：清理残留文件
%postun
if [ $1 -eq 0 ]; then
    # 完全卸载时删除数据目录
    rm -rf %{var_lib_gravitino}
    rm -rf %{sys_etc_gravitino}
fi

# 主包文件列表
%files
%defattr(-,root,root)
%dir %{usr_lib_gravitino}
%{usr_lib_gravitino}/lib/
%{usr_lib_gravitino}/licenses/
%config(noreplace) %{conf_gravitino}/gravitino-env.sh
%config(noreplace) %{conf_gravitino}/gravitino-server.conf
%attr(755,root,root) %{bin_gravitino}/common.sh

# Server 子包文件列表
%files server
%defattr(-,root,root)
%{usr_lib_gravitino}/server/
%attr(755,root,root) %{bin_gravitino}/start-server.sh
%attr(755,root,root) %{bin_gravitino}/stop-server.sh
%{_unitdir}/%{gravitino_name}.service
%dir %attr(755,%{gravitino_user},%{gravitino_group}) %{var_lib_gravitino}
%dir %attr(755,%{gravitino_user},%{gravitino_group}) %{var_log_gravitino}
%dir %attr(755,%{gravitino_user},%{gravitino_group}) %{var_run_gravitino}

# Client 子包文件列表
%files client
%defattr(-,root,root)
%attr(755,root,root) %{bin_gravitino}/gravitino-cli
%{usr_lib_gravitino}/client/
%{sys_etc_gravitino}/conf
