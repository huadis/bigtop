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

%define kibana_name kibana
%define kibana_pkg_name kibana%{pkg_name_suffix}

%define lib_kibana %{parent_dir}/%{kibana_name}
%define etc_kibana /etc/%{kibana_name}

%define np_log_kibana /var/log/%{kibana_name}
%define np_run_kibana /var/run/%{kibana_name}

%define debug_package %{nil}

# disable repacking jars
%define __os_install_post %{nil}

Name: %{kibana_pkg_name}
Version: %{kibana_version}
Release: %{kibana_release}
Summary: Kibana is a browser-based analytics and search dashboard.
URL: https://www.elastic.co/kibana
Group: Application/Internet
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
License: ASL 2.0
Source0: kibana-%{kibana_base_version}.tar.gz
Source1: do-component-build
Source2: install_%{name}.sh
Requires: bigtop-utils >= 0.7
AutoProv: no
AutoReqProv: no

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: /lib/lsb/init-functions
Requires: initscripts
%endif

%description
Kibana is a free and open user interface that lets you visualize your Elasticsearch data
and navigate the Elastic Stack. Do anything from tracking query load to
understanding the way requests flow through your apps.

%prep
%setup -n kibana-%{kibana_base_version}

#BIGTOP_PATCH_COMMANDS
%build
env FULL_VERSION=%{kibana_base_version} bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
  --build-dir=`pwd` \
  --prefix=$RPM_BUILD_ROOT \
  --distro-dir=$RPM_SOURCE_DIR \
  --lib-dir=%{lib_kibana}

%pre
getent group kibana >/dev/null || groupadd -r kibana
getent passwd kibana > /dev/null || useradd -c "Kibana" -s /sbin/nologin -g kibana -r -d %{run_kibana} kibana 2> /dev/null || :

%post

%preun

#######################
#### FILES SECTION ####
#######################
%files
%defattr(-,kibana,kibana,755)
%{lib_kibana}
%{etc_kibana}
%{np_run_kibana}
%{np_log_kibana}
