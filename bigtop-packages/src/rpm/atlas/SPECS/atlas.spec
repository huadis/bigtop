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

%define atlas_name atlas
%define atlas_pkg_name atlas%{pkg_name_suffix}

%define lib_atlas %{parent_dir}/%{atlas_name}
%define etc_atlas %{parent_dir}/%{atlas_name}
%define config_atlas %{parent_dir}/%{atlas_name}/conf

%define np_var_run_atlas /var/run/%{atlas_name}
%define np_var_log_atlas /var/log/%{atlas_name}
%define np_etc_atlas /etc/atlas

Name: %{atlas_pkg_name}
Version: %{atlas_version}
Release: %{atlas_release}
BuildArch:      noarch
Summary:        Atlas is a scalable and extensible set of core foundational governance services.
URL:            https://atlas.apache.org/
Group:          Applications/Internet
License:        Apache License 2.0
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
Source0:        apache-%{atlas_name}-%{atlas_base_version}-sources.tar.gz
Source1:        do-component-build
Source2:        install_atlas.sh
Requires: bigtop-utils >= 0.7

%description
Atlas is a scalable and extensible set of core foundational governance services –
enabling enterprises to effectively and efficiently meet their compliance requirements
within Hadoop and allows integration with the whole enterprise data ecosystem.

%prep
%setup -q -n apache-%{atlas_name}-sources-%{atlas_base_version}

%build
bash %{SOURCE1}


%install
%__rm -rf $RPM_BUILD_ROOT
bash -x %{SOURCE2} \
  --prefix=$RPM_BUILD_ROOT \
  --build-dir=`pwd`/build \
  --lib-dir=%{lib_atlas}

%pre
getent group atlas >/dev/null || groupadd -r atlas
getent passwd atlas >/dev/null || useradd -c "Atlas" -s /sbin/nologin -g atlas -r -d %{lib_atlas} atlas 2>/dev/null || :

%post
install --owner atlas --group atlas --directory --mode=0755 %{np_var_log_atlas}

%preun

%postun

%files
%defattr(644,atlas,atlas,755)
%{lib_atlas}
%{np_var_log_atlas}
%{np_var_run_atlas}
%{np_etc_atlas}
