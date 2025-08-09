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
BuildArch: noarch
Summary: Apache Knox is a secure gateway for Hadoop ecosystem
URL: http://knox.apache.org/
Group: Development/Libraries
License: ASL 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0: %{knox_name}-%{knox_base_version}-src.zip
Source1: do-component-build
Source2: install_%{knox_name}.sh
Source3: init.d.tmpl
Source4: knox-gateway.default
Source5: knox-gateway.svc
Source6: gateway-site.xml
Source7: knox.1

# 依赖
Requires: bigtop-utils >= 0.7, openssl
Requires(preun): /sbin/service

%if  %{?suse_version:1}0
%define alternatives_cmd update-alternatives
%else
%define alternatives_cmd alternatives
%endif

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

%clean
%__rm -rf $RPM_BUILD_ROOT

%prep
%setup -n %{knox_name}-%{version}
#BIGTOP_PATCH_COMMANDS

%build
bash %{SOURCE1}

%install
# Init.d scripts
%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/

bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=build \
  --knox-dir=%{usr_lib_knox} \
  --etc-knox=%{etc_knox} \
  --var-lib-knox=%{var_lib_knox} \
  --log-dir=%{var_log_knox} \
  --knox-version=%{knox_base_version}

%pre
# 创建knox用户和组
getent group knox >/dev/null || groupadd -r knox
getent passwd knox >/dev/null || useradd -c "Knox Gateway" -s /sbin/nologin -g knox -r -d %{var_lib_knox} knox 2>/dev/null || :

%post
install --owner knox --group knox --directory --mode=0755 %{var_log_knox}
for service in %{knox_services}; do
  chkconfig --add ${service}
done

%files
%defattr(-,root,root,755)
%config(noreplace) %{etc_knox}/conf.dist
%{usr_lib_knox}/bin
%{usr_lib_knox}/lib
%{usr_lib_knox}/templates
%attr(0755,%{knox_username},%{knox_username}) %dir %{var_lib_knox}
%attr(0755,%{knox_username},%{knox_username}) %dir %{var_log_knox}
%attr(0755,%{knox_username},%{knox_username}) %dir %{var_run_knox}
%doc %{usr_lib_knox}/doc
%{usr_lib_knox}/man/man1/knox.1*

%files server
%attr(0755,root,root) %{initd_dir}/%{knox_name}-gateway
%config(noreplace) %{etc_default}/%{knox_name}-gateway
