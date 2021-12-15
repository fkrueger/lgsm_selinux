# vim: sw=4:ts=4:et

%define selinux_policyver 3.14.3-1
%define selinux_ppname tf2server
%define selinux_porttype tf2server_port_t
%define selinux_ports_tcp 27005-27024
%define selinux_ports_udp 27005-27024
%define selinux_dirs /opt/tf2server/ /home/tf2server/

Name:   tf2server_selinux
Version:	1.0
Release:	5%{?dist}
Summary:	SELinux policy module for tf2server (lgsm based)
BuildRequires: policycoreutils, selinux-policy-devel

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/fkrueger/tf2server_selinux
Source0:	tf2server.te
Source1:	tf2server.fc
Source2:	tf2server.if
Source3:	tf2server_selinux.8
Source4:	tf2server_selinux-readme.md

Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the SELinux policy security module for tf2server.

%install
%{__mkdir_p} %{buildroot}%{_defaultdocdir}/%{name}-%{version} %{buildroot}%{_datadir}/selinux/devel/include/contrib %{buildroot}%{_datadir}/selinux/packages %{buildroot}%{_mandir}/man8 %{buildroot}/etc/selinux/targeted/contexts/users
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -m 600 %{SOURCE3} %{buildroot}%{_mandir}/man8/tf2server_selinux.8
install -m 644 %{SOURCE4} %{buildroot}%{_defaultdocdir}/%{name}-%{version}/readme.md
install -m 644 %{_builddir}/%{name}-%{version}-%{release}.%{_arch}/%{selinux_ppname}.pp %{buildroot}%{_datadir}/selinux/packages

%build
TMPB="%{_builddir}/%{name}-%{version}-%{release}.%{_arch}/"
mkdir -p "$TMPB"
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} "$TMPB"
cd "$TMPB"
make -f /usr/share/selinux/devel/Makefile

%post
# install policy modules
## generic part
semodule -n -i %{_datadir}/selinux/packages/%{selinux_ppname}.pp
# then add port definitions and context mirroring from /home/foo/.steam/ and .local - stuff for /opt/tf2server/
for i in %{selinux_ports_tcp} XXX; do
    [ "x$i" != "xXXX" ] && semanage port -a -t %{selinux_porttype} -p tcp $i ||:
done
for i in %{selinux_ports_udp} XXX; do
    [ "x$i" != "xXXX" ] && semanage port -a -t %{selinux_porttype} -p udp $i ||:
done
## custom part
semanage fcontext -a -e '/opt/tf2server(-[0-9]+)?/.local/share/Steam(/.*?)' '/home/tf2server(-[0-9]+)?/.local/share/Steam(/.*)?' || .
semanage fcontext -a -e '/opt/tf2server(-[0-9]+)?/.steam(/.*)?' '/home/tf2server(-[0-9]+)?/.steam(/.*)?' || .
# setup
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    restorecon -R %{selinux_dirs} ||:
fi
if [ "x$1" == "x0" ]; then
  echo "-> ONLY for first install: Remember to restart your tf2server, so it gets run securely under this newly installed SELinux policy!"
  echo ""
fi
exit 0

%postun
if [ $1 -eq 0 ]; then
    # try to remove all port definitions and context-mirroring.
    # generic part
    for i in %{selinux_ports_tcp} XXX; do
        [ "x$i" != "xXXX" ] && semanage port -d -t %{selinux_porttype} -p tcp $i ||:
    done
    for i in %{selinux_ports_udp} XXX; do
        [ "x$i" != "xXXX" ] && semanage port -d -t %{selinux_porttype} -p udp $i ||:
    done
    ## custom part
    semanage fcontext -d '/home/tf2server(-[0-9]+)?/.local/share/Steam(/.*)?' || .
    semanage fcontext -d '/home/tf2server(-[0-9]+)?/.steam(/.*)?' || .
    # then try to remove the policy module
    semodule -n -r tf2server
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       /usr/sbin/restorecon -R %{selinux_dirs} ||:
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/%{selinux_ppname}.pp
%{_datadir}/selinux/devel/include/contrib/tf2server.if
%{_mandir}/man8/tf2server_selinux.8.*
%doc %{_defaultdocdir}/%{name}-%{version}/readme.md


%changelog
* Tue Dec 7 2021 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-5
- added support for lgsm_func_t execution via cronjob

* Sat Sep 25 2021 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-4
- added support for running the tf2server update via cronjob

* Sat Sep 25 2021 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-3
- added better support for talking to tf2server_port_t to be accessed by the lgsm updater script

* Mon Aug 30 2021 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-2
- Added dontaudit for our seboolean, allowed logrotate_t and system_cronjob_t to access our files

* Mon Jul 12 2021 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-1
- Initial version

