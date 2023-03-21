# vim: sw=4:ts=4:et

%define selinux_policyver 3.14.3-95
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
Release: 13%{?dist}
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
Source14: tf2server-readme.md
Source15: tf2server_selinux_rpm.sh
Source20: tf2server.cron
Source21: tf2server.env
Source23: tf2server.sudoers
Source24: tf2server.xml
Source25: tf2server@.service
Source30: ut2k4server.te
Source31: ut2k4server.fc
Source32: ut2k4server.if
Source40: ut2k4server.cron
Source41: ut2k4server.env
Source45: ut2k4server@.service
Source43: ut2k4server.sudoers
Source44: ut2k4server.xml
Source50: lgsm_getplayersfromlog.sh
Source51: lgsm_checkupdate.sh
Source52: lgsm_restart-when-needed.sh


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

Obsoletes: tf2server_selinux, ut2k4server_selinux
Conflicts: tf2server_selinux, ut2k4server_selinux

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
#install -m 644 %{SOURCE15} %{buildroot}%{_defaultdocdir}/%{name}-%{version}/
install -m 644 %{_builddir}/%{name}-%{version}-%{release}.%{_arch}/%{selinux_tf2server_ppname}.pp %{buildroot}%{_datadir}/selinux/packages

## lgsm-ut2k4server_selinux
%{__mkdir_p} %{buildroot}%{_defaultdocdir}/%{name}-%{version} %{buildroot}%{_datadir}/selinux/devel/include/contrib %{buildroot}%{_datadir}/selinux/packages %{buildroot}%{_mandir}/man8 %{buildroot}/etc/selinux/targeted/contexts/users
install -m 644 %{SOURCE32} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
#install -m 600 %{SOURCE33} %{buildroot}%{_mandir}/man8/ut2k4server_selinux.8
#install -m 644 %{SOURCE34} %{buildroot}%{_defaultdocdir}/%{name}-%{version}/readme.md
#install -m 644 %{SOURCE35} %{buildroot}%{_defaultdocdir}/%{name}-%{version}/
install -m 644 %{_builddir}/%{name}-%{version}-%{release}.%{_arch}/%{selinux_ut2k4server_ppname}.pp %{buildroot}%{_datadir}/selinux/packages

## lgsm-utils
%{__mkdir_p} %{buildroot}%{_defaultdocdir}/%{name}-%{version} %{buildroot}/usr/bin %{buildroot}/etc/sysconfig %{buildroot}/etc/cron.d %{buildroot}/etc/sudoers.d %{buildroot}/usr/lib/systemd/system %{buildroot}/usr/lib/firewalld/services
install -m 755 %{SOURCE50} %{buildroot}/usr/bin/
install -m 755 %{SOURCE51} %{buildroot}/usr/bin/
install -m 755 %{SOURCE52} %{buildroot}/usr/bin/

## lgsm-tf2server-utils
install -m 644 %{SOURCE20} %{buildroot}/etc/cron.d/tf2server
install -m 644 %{SOURCE23} %{buildroot}/etc/sudoers.d/tf2server
install -m 644 %{SOURCE21} %{buildroot}/etc/sysconfig/tf2server.env
install -m 644 %{SOURCE25} %{buildroot}/usr/lib/systemd/system/tf2server@.service
install -m 644 %{SOURCE24} %{buildroot}/usr/lib/firewalld/services/tf2server.xml

## lgsm-ut2k4server-utils
install -m 644 %{SOURCE40} %{buildroot}/etc/cron.d/ut2k4server
install -m 644 %{SOURCE43} %{buildroot}/etc/sudoers.d/ut2k4server
install -m 644 %{SOURCE41} %{buildroot}/etc/sysconfig/ut2k4server.env
install -m 644 %{SOURCE45} %{buildroot}/usr/lib/systemd/system/ut2k4server@.service
install -m 644 %{SOURCE44} %{buildroot}/usr/lib/firewalld/services/ut2k4server.xml


%build
## lgsm_selinux
## lgsm-tf2server_selinux
## lgsm-ut2k4server_selinux
TMPB="%{_builddir}/%{name}-%{version}-%{release}.%{_arch}/"
mkdir -p "$TMPB"
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE30} %{SOURCE31} %{SOURCE32} "$TMPB"
cd "$TMPB"
make -f /usr/share/selinux/devel/Makefile

## lgsm-utils -> nothing to do here
## lgsm-tf2server-utils -> nothing to do here
## lgsm-ut2k4server-utils -> nothing to do here



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
#Release: 9%{?dist}
Summary: SELinux sub policy module for tf2server-support
BuildRequires: policycoreutils, selinux-policy-devel
Requires: lgsm_selinux
Obsoletes: tf2server_selinux, ut2k4server_selinux
Conflicts: tf2server_selinux, ut2k4server_selinux

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/fkrueger/lgsm_selinux

%description -n lgsm-tf2server_selinux
This package installs and sets up the SELinux policy security module for tf2server.


%package -n lgsm-utils
#Name: lgsm-utils
Summary: Utility scripts for handling server tasks (tf2server, ut2k4 supported as of now)

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/fkrueger/lgsm_selinux

%description -n lgsm-utils
This package contains a set of bash scripts for easier handling of your tf2server/ut2k4servers and information gathering.


%package -n lgsm-tf2server-utils
#Name: lgsm-tf2server-utils
Summary: Configuration files for OS basics (firewalld, systemd-service, cron-tasks, sudoers, tf2server-specific env-file)
Requires: lgsm_utils

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/fkrueger/lgsm_selinux

%description -n lgsm-tf2server-utils
This package contains os-specific configuration files (firewalld, systemd-service, cron-tasks, sudoers, tf2server-specific env-file).


%package -n lgsm-ut2k4server-utils
#Name: lgsm-ut2k4server-utils
Summary: Configuration files for OS basics (firewalld, systemd-service, cron-tasks, sudoers, ut2k4server-specific env-file)
Requires: lgsm_utils

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/fkrueger/lgsm_selinux

%description -n lgsm-ut2k4server-utils
This package contains os-specific configuration files (firewalld, systemd-service, cron-tasks, sudoers, ut2k4server-specific env-file).



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
    for i in %{selinux_tf2server_ports_udp} XXX; do
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



%package -n lgsm-ut2k4server_selinux
Summary: SELinux sub policy module for ut2k4server-support
BuildRequires: policycoreutils, selinux-policy-devel
Requires: lgsm_selinux
Obsoletes: tf2server_selinux, ut2k4server_selinux
Conflicts: tf2server_selinux, ut2k4server_selinux

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/fkrueger/lgsm_selinux

%description -n lgsm-ut2k4server_selinux
This package installs and sets up the SELinux policy security module for ut2k4server.


%post ut2k4server_selinux
# install policy modules
## generic part
semodule -n -i %{_datadir}/selinux/packages/%{selinux_ut2k4server_ppname}.pp
# then add port definitions and context mirroring from /home/foo/.steam/ and .local - stuff for /opt/ut2k4server/
for i in %{selinux_ut2k4server_ports_tcp} XXX; do
    [ "x$i" != "xXXX" ] && semanage port -a -t %{selinux_ut2k4server_porttype} -p tcp $i ||:
done
for i in %{selinux_ut2k4server_ports_udp} XXX; do
    [ "x$i" != "xXXX" ] && semanage port -a -t %{selinux_ut2k4server_porttype} -p udp $i ||:
done
## custom part
semanage fcontext -a -e '/opt/ut2k4server(-[0-9]+)?/.local/share/Steam(/.*?)' '/home/ut2k4server(-[0-9]+)?/.local/share/Steam(/.*)?' || .
semanage fcontext -a -e '/opt/ut2k4server(-[0-9]+)?/.steam(/.*)?' '/home/ut2k4server(-[0-9]+)?/.steam(/.*)?' || .
# setup
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    restorecon -R %{selinux_ut2k4server_dirs} ||:
fi
if [ "x$1" == "x0" ]; then
  echo "-> ONLY for first install: Remember to restart your tf2server, so it gets run securely under this newly installed SELinux policy!"
  echo ""
fi
exit 0

%postun ut2k4server_selinux
if [ $1 -eq 0 ]; then
    # try to remove all port definitions and context-mirroring.
    # generic part
    for i in %{selinux_ut2k4server_ports_tcp} XXX; do
        [ "x$i" != "xXXX" ] && semanage port -d -t %{selinux_ut2k4server_porttype} -p tcp $i ||:
    done
    for i in %{selinux_ut2k4server_ports_udp} XXX; do
        [ "x$i" != "xXXX" ] && semanage port -d -t %{selinux_ut2k4server_porttype} -p udp $i ||:
    done
    ## custom part
    semanage fcontext -d '/home/ut2k4server(-[0-9]+)?/.local/share/Steam(/.*)?' || .
    semanage fcontext -d '/home/ut2k4server(-[0-9]+)?/.steam(/.*)?' || .
    # then try to remove the policy module
    semodule -n -r ut2k4server
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       /usr/sbin/restorecon -R %{selinux_ut2k4server_dirs} ||:
    fi;
fi;
exit 0


%files ut2k4server_selinux
%attr(0600,root,root) %{_datadir}/selinux/packages/%{selinux_ut2k4server_ppname}.pp
%{_datadir}/selinux/devel/include/contrib/ut2k4server.if
#% {_mandir}/man8/ut2k4server_selinux.8.*
%doc %{_defaultdocdir}/%{name}-%{version}/readme.md


%files utils
%attr(0755,root,root) /usr/bin/lgsm_checkupdate.sh
%attr(0755,root,root) /usr/bin/lgsm_getplayersfromlog.sh
%attr(0755,root,root) /usr/bin/lgsm_restart-when-needed.sh

%files tf2server-utils
%attr(0644,root,root) /etc/cron.d/tf2server
%attr(0644,root,root) /etc/sudoers.d/tf2server
%attr(0644,root,root) /etc/sysconfig/tf2server.env
%attr(0644,root,root) /usr/lib/firewalld/services/tf2server.xml
%attr(0644,root,root) /usr/lib/systemd/system/tf2server@.service

%files ut2k4server-utils
%attr(0644,root,root) /etc/cron.d/ut2k4server
%attr(0644,root,root) /etc/sudoers.d/ut2k4server
%attr(0644,root,root) /etc/sysconfig/ut2k4server.env
%attr(0644,root,root) /usr/lib/firewalld/services/ut2k4server.xml
%attr(0644,root,root) /usr/lib/systemd/system/ut2k4server@.service



%changelog
* Thu Mar 21 2023 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-13
- tf2server: a few new permissions were missing for executing steamsdk_t as system_cronjob_t and rpm_script_t
- ut2k4server: added tcp talking to masterservers support.. somehow this one only showed up once the selinux-testservers at ut2k4.holics.at stopped used an opensource master server. and yes, fu epic for disabling the masterservers. :-(

* Sat Jan 7 2023 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-12
- fixed lgsm_getplayersfromlog output format to be easily sortable

* Fri Jan 6 2023 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-11
- lgsm_getplayersfromlog.sh now does the sensible thing: show the log filtered through sort -u
- finally made lgsm_getupdate and lgsm_restart-when-needed work better with the new dynamic systemd service files (tf2server@.service and ut2k4server@.service) . Update your /etc/sysconfig/tf2server.env file(s)!
- fixed some SELinux weirdness regarding lgsm's steamcmd
- Happy new year!

* Mon Dec 26 2022 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-10
- fixed tf2server-specific problems during updating once again, including rpm_script_t, rpm-t and crond_t related troubles
- finally finished the utils packages (lgsm-utils, lgsm-tf2server-utils, lgsm-ut2k4server-utils)
- added lgsm_restart-when-needed.sh script to get around tf2 not restarting after an update, when it should have.

* Fri Apr 15 2022 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-9
- fixed tf2server-specific problems while updating with steamcmd (again), and rpm_t/crond_t related troubles preventing reboot (again)

* Sat Feb 12 2022 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-7
- fixed tf2server-specific problems with updating and console access via steamcmd (which prevented cron-controlled server rebooting)

* Sat Dec 11 2021 Frederic Krueger <fkrueger-dev-selinux_tf2server@holics.at> 1.0-6
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

