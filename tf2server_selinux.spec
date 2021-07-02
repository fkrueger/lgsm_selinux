# vim: sw=4:ts=4:et

%define relabel_files() \
A=`getenforce` \
setenforce 0 \
restorecon -R /home/tf2server* /opt/tf2server* \
setenforce $A

%define selinux_policyver 3.14.3-54

Name:   tf2server_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for tf2server (lgsm based)
BuildRequires: policycoreutils, selinux-policy-devel

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	tf2server.te
Source1:	tf2server.fc
Source2:	tf2server.if
Source3:	tf2server_selinux.8


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the SELinux policy security module for tf2server.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{_builddir}/%{name}-%{version}-%{release}.%{_arch}/tf2server.pp %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 600 %{SOURCE3} %{buildroot}%{_mandir}/man8/tf2server_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/

%build
TMPB="%{_builddir}/%{name}-%{version}-%{release}.%{_arch}/"
mkdir -p "$TMPB"
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} "$TMPB"
cd "$TMPB"
make -f /usr/share/selinux/devel/Makefile

%post
# install policy modules
semodule -n -i %{_datadir}/selinux/packages/tf2server.pp
# then add port definitions and context mirroring from /home/foo/.steam/ and .local - stuff for /opt/tf2server/
semanage port -a -t tf2server_port_t -p udp 27005-27024 || .
semanage fcontext -a -e '/opt/tf2server(-[0-9]+)?/.local/share/Steam(/.*?)' '/home/tf2server(-[0-9]+)?/.local/share/Steam(/.*)?' || .
semanage fcontext -a -e '/opt/tf2server(-[0-9]+)?/.steam(/.*)?' '/home/tf2server(-[0-9]+)?/.steam(/.*)?' || .

if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    # try to remove all port definitions and context-mirroring.
    semanage port -d -p udp 27005-27024 || .
    semanage fcontext -d '/home/tf2server(-[0-9]+)?/.local/share/Steam(/.*)?' || .
    semanage fcontext -d '/home/tf2server(-[0-9]+)?/.steam(/.*)?' || .
    # then try to remove the policy module
    semodule -n -r tf2server
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/tf2server.pp
%{_datadir}/selinux/devel/include/contrib/tf2server.if
%{_mandir}/man8/tf2server_selinux.8.*


%changelog
* Mon Apr 19 2021 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-1
- Initial version

