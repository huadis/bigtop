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
%define dolphin_name dolphinscheduler
%define dolphin_version %{dolphinscheduler_version}
%define dolphin_release %{dolphinscheduler_release}
%define dolphin_pkg_name %{dolphin_name}%{pkg_name_suffix}
%define etc_dolphin %{parent_dir}/etc/%{dolphin_name}
%define usr_lib_dolphin %{parent_dir}/%{dolphin_name}

%define dolphin_user %{dolphin_name}
%define dolphin_group %{dolphin_name}

%define np_var_log_dolphin /var/log/%{dolphin_name}
%define np_var_run_dolphin /var/run/%{dolphin_name}
%define np_etc_dolphin /etc/%{dolphin_name}

%define alternatives_cmd alternatives

Name: %{dolphin_pkg_name}
Version: %{dolphin_version}
Release: %{dolphin_release}
BuildArch: noarch
Summary: Apache DolphinScheduler is a distributed workflow scheduler
Group: Applications/System
License: Apache License 2.0
URL: https://dolphinscheduler.apache.org/
Source0: apache-%{dolphin_name}-%{dolphin_version}-src.tar.gz
Source1: do-component-build
Source2: install_%{dolphin_name}.sh

%description
Apache DolphinScheduler is the modern data workflow orchestration platform with powerful user interface,
dedicated to solving complex task dependencies in the data pipeline and providing various types of jobs available `out of the box`


%package        alert-server
Summary:        dolphinscheduler alert server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    alert-server
dolphinscheduler alert server

%package        api-server
Summary:        dolphinscheduler api server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    api-server
dolphinscheduler api server

%package        bin
Summary:        dolphinscheduler original bin
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    bin
dolphinscheduler original bin

%package        master-server
Summary:        dolphinscheduler master server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}, %{name}-ui = %{version}-%{release}, %{name}-api-server = %{version}-%{release}

%description    master-server
dolphinscheduler master server

%package        standalone-server
Summary:        dolphinscheduler standalone server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}, %{name}-ui = %{version}-%{release}

%description    standalone-server
dolphinscheduler standalone server

%package        tools
Summary:        dolphinscheduler tools
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}, %{name}-bin = %{version}-%{release}

%description    tools
dolphinscheduler tools

%package        ui
Summary:        dolphinscheduler ui
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    ui
dolphinscheduler ui

%package        worker-server
Summary:        dolphinscheduler worker server
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}

%description    worker-server
dolphinscheduler worker server

%prep
%setup -q -n apache-%{dolphin_name}-%{dolphin_version}-src

# 构建阶段
%build
bash %{SOURCE1}

# 安装阶段
%install
rm -rf $RPM_BUILD_ROOT
bash %{SOURCE2} \
    --prefix=$RPM_BUILD_ROOT \
    --build-dir=`pwd`/build \
    --etc-dolphin=%{usr_lib_dolphin} \
    --lib-dir=%{usr_lib_dolphin}

%pre
# 创建knox用户和组
getent group %{dolphin_user} >/dev/null || groupadd -r %{dolphin_user}
getent passwd %{dolphin_user} >/dev/null || useradd -c "DolphinScheduler" -s /sbin/nologin -g %{dolphin_group} -r -d %{usr_lib_dolphin} %{dolphin_name} 2>/dev/null || :


%post
install --owner %{dolphin_user} --group %{dolphin_group} --directory --mode=0755 %{np_var_log_dolphin}

%preun

%postun


%files
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}
%{np_var_log_dolphin}
%{np_var_run_dolphin}

%files alert-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}/alert-server

%files api-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}/api-server

%files bin
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}/bin

%files master-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}/master-server

%files standalone-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}/standalone-server

%files tools
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}/tools

%files ui
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}/ui

%files worker-server
%defattr(-,dolphinscheduler,dolphinscheduler,-)
%{usr_lib_dolphin}/worker-server
