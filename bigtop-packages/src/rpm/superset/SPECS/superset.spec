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
%define superset_name superset
%define superset_pkg_name %{superset_name}%{pkg_name_suffix}
%define superset_version %{version}
%define superset_user %{superset_name}
%define superset_group %{superset_name}

# 路径定义（符合 FHS 标准和 BigTop 目录规范）
%define parent_dir %{_prefix}
%define usr_lib_superset %{parent_dir}/%{superset_name}          # 主程序目录
%define etc_superset %{parent_dir}/etc/%{superset_name}          # 配置文件目录
%define var_lib_superset %{parent_dir}/var/lib/%{superset_name}  # 数据存储目录
%define var_log_superset %{parent_dir}/var/log/%{superset_name}  # 日志目录
%define var_run_superset %{parent_dir}/var/run/%{superset_name}  # 运行时目录（PID等）
%define bin_superset %{usr_lib_superset}/bin                      # 可执行脚本目录
%define conf_superset %{usr_lib_superset}/conf                    # 配置模板目录

# 系统标准路径映射（通过符号链接关联）
%define sys_etc_superset /etc/%{superset_name}
%define sys_var_log_superset /var/log/%{superset_name}
%define sys_var_run_superset /var/run/%{superset_name}

# 依赖管理配置
%define alternatives_cmd alternatives

# RPM 包基本信息
Name: %{superset_pkg_name}
Version: 2.1.0
Release: 1%{?dist}
BuildArch: noarch
Summary: Apache Superset is a modern, enterprise-ready business intelligence web application
Group: Applications/System
License: Apache License 2.0
URL: https://superset.apache.org/
Source0: %{superset_name}-%{version}-src.tar.gz
Source1: do-component-build
Source2: install_superset.sh
Source3: superset-env.sh
Source4: superset.service
Source5: superset_config.py

# 依赖项（基于 Superset 运行需求）
Requires: python39 >= 3.9.0
Requires: python39-pip >= 21.0
Requires: python39-devel >= 3.9.0
Requires: gcc
Requires: gcc-c++
Requires: openssl-devel
Requires: libffi-devel
Requires: postgresql >= 12.0
Requires: postgresql-server >= 12.0
Requires: nodejs >= 16.0.0
Requires: npm >= 7.0.0
Requires: bigtop-utils >= 0.14
BuildRequires: git, tar, gzip, make

%description
Apache Superset is a modern, enterprise-ready business intelligence web application.
It is fast, lightweight, intuitive, and loaded with options that make it easy for
users of all skill sets to explore and visualize their data, from simple pie charts
to highly detailed deck.gl geospatial charts.

# 子包：server（核心服务组件）
%package server
Summary: Apache Superset server component
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: httpd >= 2.4.0
Requires: mod_wsgi >= 4.9.0

%description server
This package contains the core server components of Apache Superset, including
the web application, API service, and background workers. It provides the
business intelligence and data visualization capabilities.

# 子包：cli（命令行工具）
%package cli
Summary: Apache Superset command-line interface
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description cli
This package provides command-line tools for managing Apache Superset, including
database initialization, user management, and configuration commands.

# 准备阶段：解压源码包
%prep
%setup -q -n %{superset_name}-%{version}

# 构建阶段：执行编译脚本
%build
bash %{SOURCE1}

# 安装阶段：执行安装脚本
%install
rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
    --prefix=$RPM_BUILD_ROOT \
    --source-dir=`pwd`/dist \
    --install-dir=%{usr_lib_superset}

# 复制配置文件和环境变量模板
mkdir -p $RPM_BUILD_ROOT%{conf_superset}
cp %{SOURCE3} $RPM_BUILD_ROOT%{conf_superset}/superset-env.sh
cp %{SOURCE5} $RPM_BUILD_ROOT%{conf_superset}/superset_config.py

# 配置 systemd 服务
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/%{superset_name}.service

# 创建符号链接（符合 FHS 标准）
mkdir -p $RPM_BUILD_ROOT%{sys_etc_superset}
ln -s %{conf_superset} $RPM_BUILD_ROOT%{sys_etc_superset}/conf

# 预安装脚本：创建专用用户和组
%pre
# 创建 superset 组
if ! getent group %{superset_group} >/dev/null; then
    groupadd -r %{superset_group}
fi
# 创建 superset 用户（禁止登录，主目录为数据目录）
if ! getent passwd %{superset_user} >/dev/null; then
    useradd -r -g %{superset_group} -d %{var_lib_superset} \
            -s /sbin/nologin -c "Apache Superset" %{superset_user}
fi

# 数据库初始化准备
if ! getent passwd postgres >/dev/null; then
    useradd -r -d /var/lib/pgsql -s /bin/bash postgres
fi

# 安装后脚本：初始化目录和服务
%post
# 创建数据、日志、运行时目录
mkdir -p %{var_lib_superset} %{var_log_superset} %{var_run_superset}
mkdir -p %{var_lib_superset}/db %{var_lib_superset}/uploads
# 设置目录权限
chown -R %{superset_user}:%{superset_group} %{var_lib_superset} %{var_log_superset} %{var_run_superset}
chmod -R 755 %{var_lib_superset} %{var_log_superset} %{var_run_superset}

# 初始化数据库
if [ $1 -eq 1 ]; then
    su - %{superset_user} -s /bin/bash -c "%{bin_superset}/superset db upgrade"
    su - %{superset_user} -s /bin/bash -c "%{bin_superset}/superset init"
fi

# 配置 systemd 服务
systemctl daemon-reload
if [ $1 -eq 1 ]; then
    # 首次安装时启用服务
    systemctl enable %{superset_name}.service >/dev/null 2>&1 || :
fi

# 预卸载脚本：停止服务
%preun
if [ $1 -eq 0 ]; then
    # 完全卸载时停止并禁用服务
    systemctl stop %{superset_name}.service >/dev/null 2>&1 || :
    systemctl disable %{superset_name}.service >/dev/null 2>&1 || :
fi

# 卸载后脚本：清理残留文件
%postun
if [ $1 -eq 0 ]; then
    # 完全卸载时删除数据目录（保留数据库，用户需手动删除）
    rm -rf %{var_lib_superset}/uploads
    rm -rf %{sys_etc_superset}
fi

# 主包文件列表
%files
%defattr(-,root,root)
%dir %{usr_lib_superset}
%{usr_lib_superset}/app/
%{usr_lib_superset}/static/
%{usr_lib_superset}/templates/
%{usr_lib_superset}/requirements/
%{usr_lib_superset}/LICENSE
%{usr_lib_superset}/NOTICE
%config(noreplace) %{conf_superset}/superset-env.sh
%config(noreplace) %{conf_superset}/superset_config.py

# Server 子包文件列表
%files server
%defattr(-,root,root)
%{usr_lib_superset}/wsgi.py
%attr(755,root,root) %{bin_superset}/gunicorn_launcher.sh
%attr(755,root,root) %{bin_superset}/celery_worker.sh
%{_unitdir}/%{superset_name}.service
%dir %attr(755,%{superset_user},%{superset_group}) %{var_lib_superset}
%dir %attr(755,%{superset_user},%{superset_group}) %{var_log_superset}
%dir %attr(755,%{superset_user},%{superset_group}) %{var_run_superset}

# CLI 子包文件列表
%files cli
%defattr(-,root,root)
%attr(755,root,root) %{bin_superset}/superset
%attr(755,root,root) %{bin_superset}/superset-cli.sh
%{sys_etc_superset}/conf

