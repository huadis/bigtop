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

%define kyuubi_name kyuubi
%define kyuubi_pkg_name kyuubi%{pkg_name_suffix}
%define lib_kyuubi %{parent_dir}/%{kyuubi_name}
%define etc_kyuubi %{parent_dir}/%{kyuubi_name}
%define config_kyuubi %{parent_dir}/%{kyuubi_name}/conf
%define kyuubi_services server
%define var_lib_kyuubi /var/lib/%{kyuubi_name}
%define var_run_kyuubi /var/run/%{kyuubi_name}
%define var_log_kyuubi /var/log/%{kyuubi_name}

Name: %{livy_pkg_name}
Version: %{livy_version}
Release: %{livy_release}
BuildArch:      noarch
Summary:        Apache Kyuubi is a distributed and multi-tenant gateway to provide SQL service over various computing frameworks.
Group:          Applications/Internet
License:        Apache License 2.0
URL:            https://kyuubi.apache.org/
Source0:        apache-kyuubi-%{version}-source.tgz
Source1:        install_kyuubi.sh
Source2:        kyuubi.service
Source3:        kyuubi-env.sh
BuildRequires:  java-1.8.0-openjdk-devel
BuildRequires:  bigtop-utils
Requires:       java-1.8.0-openjdk
Requires:       hadoop >= 3.0.0
Requires:       spark >= 3.0.0
Requires(pre):  shadow-utils

%description
Apache Kyuubi is a distributed and multi-tenant gateway to provide SQL service over various computing frameworks.
It aims to make the Data Lakehouse accessible via SQL based tools, and decouple the computing and storage.

%prep
%setup -q -n apache-kyuubi-%{version}-bin

%build
# 构建过程在 do-component-build 中完成，此处仅做准备
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%install
# 创建临时安装目录
mkdir -p %{buildroot}/usr/lib/kyuubi
mkdir -p %{buildroot}/etc/kyuubi/conf
mkdir -p %{buildroot}/var/log/kyuubi
mkdir -p %{buildroot}/var/run/kyuubi
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/etc/profile.d

# 复制 Kyuubi 文件
cp -r * %{buildroot}/usr/lib/kyuubi/

# 移动配置文件
mv %{buildroot}/usr/lib/kyuubi/conf/* %{buildroot}/etc/kyuubi/conf/
ln -s /etc/kyuubi/conf %{buildroot}/usr/lib/kyuubi/conf

# 安装 systemd 服务文件
install -m 0644 kyuubi.service %{buildroot}/usr/lib/systemd/system/

# 安装环境变量配置
install -m 0644 kyuubi-env.sh %{buildroot}/etc/profile.d/

# 安装启动脚本
install -m 0755 bin/kyuubi %{buildroot}/usr/bin/
install -m 0755 bin/kyuubi-daemon.sh %{buildroot}/usr/bin/

%pre
# 创建用户和组
getent group kyuubi >/dev/null || groupadd -r kyuubi
getent passwd kyuubi >/dev/null || \
    useradd -r -g kyuubi -d /usr/lib/kyuubi -s /sbin/nologin \
    -c "Apache Kyuubi" kyuubi
exit 0

%post
# 启用并启动服务
systemctl daemon-reload
if [ $1 -eq 1 ]; then
    # 首次安装
    systemctl enable kyuubi
    systemctl start kyuubi
else
    # 升级
    systemctl restart kyuubi
fi

%preun
if [ $1 -eq 0 ]; then
    # 完全卸载
    systemctl stop kyuubi
    systemctl disable kyuubi
fi

%files
%defattr(-,kyuubi,hadoop,-)
/usr/lib/kyuubi/
/etc/kyuubi/
/var/log/kyuubi/
/var/run/kyuubi/
/usr/bin/kyuubi
/usr/bin/kyuubi-daemon.sh
/usr/lib/systemd/system/kyuubi.service
/etc/profile.d/kyuubi-env.sh
%doc LICENSE NOTICE README.md

%changelog
* Thu Aug 14 2025 Your Name <your.email@example.com> - %{version}-1
- Initial RPM package for Apache Kyuubi following BigTop specifications
