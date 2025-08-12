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
%define seatunnel_name seatunnel
%define seatunnel_pkg_name %{seatunnel_name}%{pkg_name_suffix}
%define seatunnel_version %{version}
%define seatunnel_user %{seatunnel_name}
%define seatunnel_group %{seatunnel_name}

# 路径定义（符合 FHS 标准和 BigTop 目录规范）
%define parent_dir %{_prefix}
%define usr_lib_seatunnel %{parent_dir}/%{seatunnel_name}          # 主程序目录
%define etc_seatunnel %{parent_dir}/etc/%{seatunnel_name}          # 配置文件目录
%define var_lib_seatunnel %{parent_dir}/var/lib/%{seatunnel_name}  # 数据存储目录（作业配置、插件）
%define var_log_seatunnel %{parent_dir}/var/log/%{seatunnel_name}  # 日志目录
%define var_run_seatunnel %{parent_dir}/var/run/%{seatunnel_name}  # 运行时目录（PID、临时文件）
%define bin_seatunnel %{usr_lib_seatunnel}/bin                      # 可执行脚本目录
%define conf_seatunnel %{usr_lib_seatunnel}/conf                    # 配置模板目录
%define plugins_seatunnel %{usr_lib_seatunnel}/plugins              # 插件目录

# 系统标准路径映射（通过符号链接关联）
%define sys_etc_seatunnel /etc/%{seatunnel_name}
%define sys_var_log_seatunnel /var/log/%{seatunnel_name}

# 依赖管理配置
%define alternatives_cmd alternatives

# RPM 包基本信息
Name: %{seatunnel_pkg_name}
Version: 2.3.3
Release: 1%{?dist}
BuildArch: noarch
Summary: Apache SeaTunnel is a distributed data integration platform
Group: Applications/System
License: Apache License 2.0
URL: https://seatunnel.apache.org/
Source0: %{seatunnel_name}-%{version}-src.tar.gz
Source1: do-component-build
Source2: install_seatunnel.sh
Source3: seatunnel-env.sh
Source4: seatunnel.service
Source5: seatunnel.yaml  # 核心配置模板

# 依赖项（基于 SeaTunnel 运行需求）
Requires: java-11-openjdk >= 11.0.20  # SeaTunnel 2.x 依赖 Java 11+
Requires: bigtop-utils >= 0.14
Requires: flink >= 1.17.0  # 若使用 Flink 引擎
Requires: spark >= 3.3.0   # 若使用 Spark 引擎（可选）
Requires: zookeeper >= 3.8.0  # 集群模式依赖
BuildRequires: maven >= 3.8.6, git, tar, gzip, unzip

%description
Apache SeaTunnel is an open-source distributed data integration platform that supports
batch and streaming data synchronization. It provides rich connectors for databases,
message queues, and data warehouses, enabling efficient data migration and transformation.

# 子包：server（集群服务组件）
%package server
Summary: Apache SeaTunnel cluster server component
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: hadoop-client >= 3.3.4  # 若集成 Hadoop 分布式文件系统

%description server
This package contains the cluster server components of Apache SeaTunnel, including
the coordinator and worker nodes. It supports distributed data synchronization jobs
with high availability and scalability.

# 子包：client（客户端工具）
%package client
Summary: Apache SeaTunnel command-line client
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description client
This package provides command-line tools for submitting and managing Apache SeaTunnel
data synchronization jobs, including seatunnel-cli and configuration utilities.

# 准备阶段：解压源码包
%prep
%setup -q -n %{seatunnel_name}-%{version}

# 构建阶段：执行编译脚本
%build
bash %{SOURCE1}

# 安装阶段：执行安装脚本
%install
rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
    --prefix=$RPM_BUILD_ROOT \
    --source-dir=`pwd`/dist \
    --install-dir=%{usr_lib_seatunnel}

# 复制配置文件和环境变量模板
mkdir -p $RPM_BUILD_ROOT%{conf_seatunnel}
cp %{SOURCE3} $RPM_BUILD_ROOT%{conf_seatunnel}/seatunnel-env.sh
cp %{SOURCE5} $RPM_BUILD_ROOT%{conf_seatunnel}/seatunnel.yaml

# 配置 systemd 服务（集群模式）
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/%{seatunnel_name}.service

# 创建符号链接（符合 FHS 标准）
mkdir -p $RPM_BUILD_ROOT%{sys_etc_seatunnel}
ln -s %{conf_seatunnel} $RPM_BUILD_ROOT%{sys_etc_seatunnel}/conf
ln -s %{plugins_seatunnel} $RPM_BUILD_ROOT%{sys_etc_seatunnel}/plugins  # 插件配置链接

# 预安装脚本：创建专用用户和组
%pre
# 创建 seatunnel 组
if ! getent group %{seatunnel_group} >/dev/null; then
    groupadd -r %{seatunnel_group}
fi
# 创建 seatunnel 用户（禁止登录，主目录为数据目录）
if ! getent passwd %{seatunnel_user} >/dev/null; then
    useradd -r -g %{seatunnel_group} -d %{var_lib_seatunnel} \
            -s /sbin/nologin -c "Apache SeaTunnel" %{seatunnel_user}
fi

# 安装后脚本：初始化目录和服务
%post
# 创建数据、日志、运行时目录
mkdir -p %{var_lib_seatunnel} %{var_log_seatunnel} %{var_run_seatunnel}
# 设置目录权限（服务用户可读写）
chown -R %{seatunnel_user}:%{seatunnel_group} %{var_lib_seatunnel} %{var_log_seatunnel} %{var_run_seatunnel}
chmod -R 755 %{var_lib_seatunnel} %{var_log_seatunnel} %{var_run_seatunnel}

# 配置 systemd 服务
systemctl daemon-reload
if [ $1 -eq 1 ]; then
    # 首次安装时启用服务
    systemctl enable %{seatunnel_name}.service >/dev/null 2>&1 || :
fi

# 预卸载脚本：停止服务
%preun
if [ $1 -eq 0 ]; then
    # 完全卸载时停止并禁用服务
    systemctl stop %{seatunnel_name}.service >/dev/null 2>&1 || :
    systemctl disable %{seatunnel_name}.service >/dev/null 2>&1 || :
fi

# 卸载后脚本：清理残留文件
%postun
if [ $1 -eq 0 ]; then
    # 完全卸载时删除数据目录（保留日志可选）
    rm -rf %{var_lib_seatunnel}
    rm -rf %{sys_etc_seatunnel}
fi

# 主包文件列表
%files
%defattr(-,root,root)
%dir %{usr_lib_seatunnel}
%{usr_lib_seatunnel}/lib/
%{usr_lib_seatunnel}/licenses/
%{plugins_seatunnel}/  # 数据连接器插件
%config(noreplace) %{conf_seatunnel}/seatunnel-env.sh
%config(noreplace) %{conf_seatunnel}/seatunnel.yaml
%attr(755,root,root) %{bin_seatunnel}/common.sh

# Server 子包文件列表
%files server
%defattr(-,root,root)
%{usr_lib_seatunnel}/server/  # 集群服务代码
%attr(755,root,root) %{bin_seatunnel}/start-server.sh
%attr(755,root,root) %{bin_seatunnel}/stop-server.sh
%{_unitdir}/%{seatunnel_name}.service
%dir %attr(755,%{seatunnel_user},%{seatunnel_group}) %{var_lib_seatunnel}
%dir %attr(755,%{seatunnel_user},%{seatunnel_group}) %{var_log_seatunnel}
%dir %attr(755,%{seatunnel_user},%{seatunnel_group}) %{var_run_seatunnel}

# Client 子包文件列表
%files client
%defattr(-,root,root)
%attr(755,root,root) %{bin_seatunnel}/seatunnel-cli
%attr(755,root,root) %{bin_seatunnel}/submit-job.sh  # 作业提交脚本
%{sys_etc_seatunnel}/conf
%{sys_etc_seatunnel}/plugins
