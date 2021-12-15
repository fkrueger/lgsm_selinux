# vim: sw=4:ts=4:et

%define selinux_policyver 3.14.3-1
%define selinux_lgsm_ppname lgsm
%define selinux_lgsm_porttype nil
%define selinux_lgsm_ports_tcp nil
%define selinux_lgsm_ports_udp nil
%define selinux_lgsm_dirs /opt/ /etc/sysconfig/

%define selinux_tf2server_ppname tf2server
%define selinux_tf2server_porttype tf2server_port_t
%define selinux_tf2server_ports_tcp 27005-27024
%define selinux_tf2server_ports_udp 27005-27024
%define selinux_tf2server_dirs /opt/tf2server*/ /home/tf2server*/ /etc/sysconfig/

%define selinux_ut2k4server_ppname ut2k4server
%define selinux_ut2k4server_porttype ut2k4server_port_t
%define selinux_ut2k4server_ports_tcp 8075 8065
%define selinux_ut2k4server_ports_udp 7777-7778 7787-7788 10777 6777-6778 6787-6788 10677
%define selinux_ut2k4server_dirs /opt/ut2k4server*/ /etc/sysconfig/



Name: lgsm
Version: 1.0
Release: 6%{?dist}
Summary: SELinux base policy module for LGSM-based servers
BuildRequires: policycoreutils, selinux-policy-devel

Group: System Environment/Base		
License: GPLv2+	
URL: https://github.com/fkrueger/lgsm_selinux
Source0: lgsm.te
Source1: lgsm.fc
Source2: lgsm.if
Source10: tf2server.te
Source11: tf2server.fc
Source12: tf2server.if
Source13: tf2server_selinux.8
Source14: tf2server_selinux-readme.md
Source15: tf2server_selinux_rpm.sh
Source20: tf2server.cron
Source21: tf2server.env
Source22: tf2server.service
Source23: tf2server.sudoers
Source24: tf2server.xml
Source30: ut2k4server.te
Source31: ut2k4server.fc
Source32: ut2k4server.if
Source40: ut2k4server.cron
Source41: ut2k4server.env
Source42: ut2k4server.service
Source43: ut2k4server.sudoers
Source44: ut2k4server.xml
Source50: lgsm_getplayersfromlog.sh
Source51: lgsm_checkupdate.sh


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the SELinux base policy for LGSM-based servers.


%install

## lgsm_selinux
%{__mkdir_p} %{buildroot}%{_defaultdocdir}/%{name}-%{version} %{buildroot}%{_datadir}/selinux/devel/include/contrib %{buildroot}%{_datadir}/selinux/packages %{buildroot}%{_mandir}/man8 %{buildroot}/etc/selinux/targeted/contexts/users
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -m 644 %{_builddir}/%{name}-%{version}-%{release}.%{_arch}/%{selinux_lgsm_ppname}.pp %{buildroot}%{_datadir}/selinux/packages

## lgsm-tf2server_selinux
%{__mkdir_p} %{buildroot}%{_defaultdocdir}/%{name}-%{version} %{buildroot}%{_datadir}/selinux/devel/include/contrib %{buildroot}%{_datadir}/selinux/packages %{buildroot}%{_mandir}/man8 %{buildroot}/etc/selinux/targeted/contexts/users
install -m 644 %{SOURCE12} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -m 600 %{SOURCE13} %{buildroot}%{_mandir}/man8/tf2server_selinux.8
install -m 644 %{SOURCE14} %{buildroot}%{_defaultdocdir}/%{name}-%{version}/readme.md
install -m 644 %{SOURCE15} %{buildroot}%{_defaultdocdir}/%{name}-%{version}/
install -m 644 %{_builddir}/%{name}-%{version}-%{release}.%{_arch}/%{selinux_tf2server_ppname}.pp %{buildroot}%{_datadir}/selinux/packages

## lgsm-ut2k4server_selinux
## lgsm-utils
## lgsm-tf2server-utils
## lgsm-ut2k4server-utils


%build
## lgsm_selinux
## lgsm-tf2server_selinux
## lgsm-ut2k4server_selinux
TMPB="%{_builddir}/%{name}-%{version}-%{release}.%{_arch}/"
mkdir -p "$TMPB"
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE30} %{SOURCE31} %{SOURCE32} "$TMPB"
cd "$TMPB"
make -f /usr/share/selinux/devel/Makefile
## lgsm-utils
## lgsm-tf2server-utils
## lgsm-ut2k4server-utils



%post
# install policy modules
## generic part
semodule -n -i %{_datadir}/selinux/packages/%{selinux_lgsm_ppname}.pp
# then add port definitions and context mirroring from /home/foo/.steam/ and .local - stuff for /opt/lgsm/
for i in %{selinux_lgsm_ports_tcp} XXX; do
    [ "x$i" != "xXXX" ] && semanage port -a -t %{selinux_lgsm_porttype} -p tcp $i ||:
done
for i in %{selinux_lgsm_ports_udp} XXX; do
    [ "x$i" != "xXXX" ] && semanage port -a -t %{selinux_lgsm_porttype} -p udp $i ||:
done
# setup
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    restorecon -R %{selinux_lgsm_dirs} ||:
fi
if [ "x$1" == "x0" ]; then
  echo "-> ONLY for first install: Remember to restart your lgsm-based servers, so they get run securely under this newly installed SELinux policy!"
  echo ""
fi
exit 0

%postun
if [ $1 -eq 0 ]; then
    # try to remove all port definitions and context-mirroring.
    # generic part
    for i in %{selinux_lgsm_ports_tcp} XXX; do
        [ "x$i" != "xXXX" ] && semanage port -d -t %{selinux_lgsm_porttype} -p tcp $i ||:
    done
    for i in %{selinux_ports_udp} XXX; do
        [ "x$i" != "xXXX" ] && semanage port -d -t %{selinux_lgsm_porttype} -p udp $i ||:
    done
    # then try to remove the policy module
    semodule -n -r lgsm
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       /usr/sbin/restorecon -R %{selinux_lgsm_dirs} ||:
    fi;
fi;
exit 0


%files
%attr(0600,root,root) %{_datadir}/selinux/packages/%{selinux_lgsm_ppname}.pp
%{_datadir}/selinux/devel/include/contrib/lgsm.if



%package -n lgsm-tf2server_selinux
#Name: lgsm-tf2server_selinux
#Version: 1.0
#Release: 6%{?dist}
Summary: SELinux sub policy module for tf2server-support
BuildRequires: policycoreutils, selinux-policy-devel
Requires: lgsm_selinux

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/fkrueger/tf2server_selinux


%description -n lgsm-tf2server_selinux
This package installs and sets up the SELinux policy security module for tf2server.




%post tf2server_selinux
# install policy modules
## generic part
semodule -n -i %{_datadir}/selinux/packages/%{selinux_tf2server_ppname}.pp
# then add port definitions and context mirroring from /home/foo/.steam/ and .local - stuff for /opt/tf2server/
for i in %{selinux_tf2server_ports_tcp} XXX; do
    [ "x$i" != "xXXX" ] && semanage port -a -t %{selinux_tf2server_porttype} -p tcp $i ||:
done
for i in %{selinux_tf2server_ports_udp} XXX; do
    [ "x$i" != "xXXX" ] && semanage port -a -t %{selinux_tf2server_porttype} -p udp $i ||:
done
## custom part
semanage fcontext -a -e '/opt/tf2server(-[0-9]+)?/.local/share/Steam(/.*?)' '/home/tf2server(-[0-9]+)?/.local/share/Steam(/.*)?' || .
semanage fcontext -a -e '/opt/tf2server(-[0-9]+)?/.steam(/.*)?' '/home/tf2server(-[0-9]+)?/.steam(/.*)?' || .
# setup
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    restorecon -R %{selinux_tf2server_dirs} ||:
fi
if [ "x$1" == "x0" ]; then
  echo "-> ONLY for first install: Remember to restart your tf2server, so it gets run securely under this newly installed SELinux policy!"
  echo ""
fi
exit 0

%postun tf2server_selinux
if [ $1 -eq 0 ]; then
    # try to remove all port definitions and context-mirroring.
    # generic part
    for i in %{selinux_tf2server_ports_tcp} XXX; do
        [ "x$i" != "xXXX" ] && semanage port -d -t %{selinux_tf2server_porttype} -p tcp $i ||:
    done
    for i in %{selinux_ports_udp} XXX; do
        [ "x$i" != "xXXX" ] && semanage port -d -t %{selinux_tf2server_porttype} -p udp $i ||:
    done
    ## custom part
    semanage fcontext -d '/home/tf2server(-[0-9]+)?/.local/share/Steam(/.*)?' || .
    semanage fcontext -d '/home/tf2server(-[0-9]+)?/.steam(/.*)?' || .
    # then try to remove the policy module
    semodule -n -r tf2server
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       /usr/sbin/restorecon -R %{selinux_tf2server_dirs} ||:
    fi;
fi;
exit 0




%files tf2server_selinux
%attr(0600,root,root) %{_datadir}/selinux/packages/%{selinux_tf2server_ppname}.pp
%{_datadir}/selinux/devel/include/contrib/tf2server.if
%{_mandir}/man8/tf2server_selinux.8.*
%doc %{_defaultdocdir}/%{name}-%{version}/readme.md




%changelog
* Tue Dec 11 2021 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-6
- split up lgsm and tf2server policy
- added new ut2k4server policy

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

