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

%define knox_username knox
%define knox_name knox
%define knox_pkg_name knox%{pkg_name_suffix}
%define hadoop_pkg_name hadoop%{pkg_name_suffix}

# 目录定义
%define initd_dir /etc/rc.d/init.d

%define usr_lib_knox %{parent_dir}/%{knox_name}
%define etc_knox %{parent_dir}/%{knox_name}/etc
%define var_lib_knox %{parent_dir}/%{knox_name}
%define var_log_knox /var/log/%{knox_name}
%define var_run_knox /var/run/%{knox_name}
%define np_etc_knox /etc/%{knox_name}

# 构建与服务相关定义
%define knox_dist build/dist
%define knox_services knox-gateway
%define alternatives_cmd alternatives

Name: %{knox_pkg_name}
Version: %{knox_version}
Release: %{knox_release}
Summary: Apache Knox is a secure gateway for Hadoop ecosystem
License: ASL 2.0
URL: http://knox.apache.org/
Group: System/Daemons
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
BuildArch: noarch
Source0: apache-%{knox_name}-%{knox_base_version}-src.tar.gz
Source1: do-component-build  # 编译脚本
Source2: install_knox.sh     # 安装脚本
Source3: init.d.tmpl         # 服务初始化模板
Source4: knox-gateway.default  # 服务默认配置
Source5: knox-gateway.svc    # 服务定义
Source6: gateway-site.xml    # 核心配置文件
Source7: knox.1              # man文档

# 依赖
Requires: %{hadoop_pkg_name}-client, bigtop-utils >= 0.7, openssl
Requires: /lib/lsb/init-functions  # 初始化脚本依赖

%description
Apache Knox provides a single point of authentication and access for Apache Hadoop services.
It acts as a reverse proxy, simplifying secure access to Hadoop clusters by consolidating
authentication, authorization, and audit capabilities. Knox supports multiple authentication
mechanisms (LDAP, Kerberos, etc.) and provides a centralized gateway for HDFS, YARN, Hive,
HBase, and other Hadoop services.


%package server
Summary: Apache Knox gateway server
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}

%description server
This package contains the Apache Knox gateway server, including init scripts and service configuration.
It provides the core reverse proxy functionality for secure Hadoop ecosystem access.


%prep
%setup -q -n apache-%{knox_name}-%{knox_base_version}-src
# 应用补丁（如有）
#BIGTOP_PATCH_COMMANDS


%build
# 编译Knox（使用Maven）
env \
  DO_MAVEN_DEPLOY=%{?do_maven_deploy} \
  MAVEN_REPO_URI=%{?maven_repo_uri} \
bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT

# 执行安装脚本
/bin/bash %{SOURCE2} \
  --build-dir=%{knox_dist} \
  --prefix=$RPM_BUILD_ROOT \
  --knox-dir=%{usr_lib_knox} \
  --etc-knox=%{etc_knox} \
  --var-lib-knox=%{var_lib_knox} \
  --log-dir=%{var_log_knox} \
  --knox-version=%{knox_base_version}

# 安装初始化脚本和配置文件
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/
%__install -d -m 0755 $RPM_BUILD_ROOT/%{etc_default}/
%__install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT/%{etc_default}/%{knox_name}-gateway

# 生成服务脚本
for service in %{knox_services}; do
    init_file=$RPM_BUILD_ROOT/%{initd_dir}/${service}
    bash %{SOURCE3} %{SOURCE5} rpm $init_file
done

# 创建日志/运行目录
%__install -d -m 0755 $RPM_BUILD_ROOT/%{var_log_knox}
%__install -d -m 0755 $RPM_BUILD_ROOT/%{var_run_knox}


%pre
# 创建knox用户和组
getent group knox >/dev/null || groupadd -r knox
getent passwd knox >/dev/null || useradd -c "Knox Gateway" -s /sbin/nologin -g knox -r -d %{var_lib_knox} knox 2>/dev/null || :


%post
# 配置 alternatives（多版本切换）
%{alternatives_cmd} --install %{np_etc_knox}/conf %{knox_name}-conf %{etc_knox}/conf.dist 30

# 升级处理（如有旧版本配置迁移）
if [ "$1" -gt 1 ]; then
  # 迁移旧拓扑文件到新目录
  [ -d /etc/knox/topologies ] && mv /etc/knox/topologies %{etc_knox}/conf.dist/topologies || :
fi


%preun
if [ "$1" = 0 ]; then
  # 卸载时移除alternatives
  %{alternatives_cmd} --remove %{knox_name}-conf %{etc_knox}/conf.dist || :
fi


# 服务器子包脚本
%post server
# 注册服务并设置自启动
chkconfig --add %{knox_name}-gateway
service %{knox_name}-gateway start >/dev/null 2>&1 || :

%preun server
if [ "$1" = 0 ]; then
  # 卸载时停止服务
  service %{knox_name}-gateway stop >/dev/null 2>&1
  chkconfig --del %{knox_name}-gateway
fi

%postun server
if [ $1 -ge 1 ]; then
  # 升级时重启服务
  service %{knox_name}-gateway condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,755)
%config(noreplace) %{etc_knox}/conf.dist  # 核心配置
%{usr_lib_knox}/bin                      # 二进制脚本
%{usr_lib_knox}/lib                      # 依赖库
%{usr_lib_knox}/templates                # 拓扑模板
%attr(0755,%{knox_username},%{knox_username}) %dir %{var_lib_knox}
%attr(0755,%{knox_username},%{knox_username}) %dir %{var_log_knox}
%attr(0755,%{knox_username},%{knox_username}) %dir %{var_run_knox}
%doc %{usr_lib_knox}/doc                 # 文档
%{usr_lib_knox}/man/man1/knox.1*         # man文档

%files server
%attr(0755,root,root) %{initd_dir}/%{knox_name}-gateway  # 服务脚本
%config(noreplace) %{etc_default}/%{knox_name}-gateway    # 服务默认配置
