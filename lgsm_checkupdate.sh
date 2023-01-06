#!/bin/bash


SYSDCTL="/usr/bin/systemctl"
SELXGETENF="/usr/sbin/getenforce"
SELXRESTCON="/usr/sbin/restorecon"

## defaults:
SVCGAME="tf2server"
SVCNAME="tf2server"
SVCUSER="tf2server"
SVCDIR="/opt/$SVCNAME"

LGSMSERVERBIN="$SVCDIR/$SVCNAME"
UPDATELOGFILE="$SVCDIR/log/server/${SVCNAME}_checkupdate.log"



# automatically created
SYSDSVCNAME="$SVCGAME@$SVCNAME"


usage() {
  echo "usage: $0 [servicename] <doit>"
  echo ""
  echo "    do lgsm updating for lgsm, server ($SVCNAME) & common (installed) server mods update restart while handling systemd as well."
  echo "    you can add [servicename] to load a custom env file from /etc/sysconfig, eg. supply tf2server-2 to load /etc/sysconfig/tf2server-2 ."
  echo ""
  echo "    add 'doit' do actually do something."
  echo ""
  exit -1
}

logme() {
  TS=`date +%Y%m%d_%H%M%S`
  if [ "x$DOIT" == "x1" ]; then
    echo "$TS: $*" >>$UPDATELOGFILE
  else
    echo "$TS: $*"
  fi
}


DOIT=0
[ "x$1" == "xdoit" ] && DOIT=1
if [ "x$DOIT" == "x0" ]; then
  ENVFILE="/etc/sysconfig/$1.env"
  if [ -e "$ENVFILE" ]; then
    source $ENVFILE
    [ "x$2" == "xdoit" ] && DOIT=1
  else
    if [ "x$1" != "x" ]; then
      echo "!!! Problem loading env file $ENVFILE . Exitting."
      exit 1
    fi
  fi
fi

if [ "x$1" == "-h" ] || [ "x$1" == "--help" ]; then
  usage
fi


if [ "x$UID" == "x0" ]; then				# make sure our files are as server-username, so lgsm update doesnt fail to restart the server.
  chown $SVCUSER:$SVCUSER $UPDPATELOGFILE >/dev/null 2>&1
fi


logme ""
logme "====================================================================================================="
logme "# Started with \$*: $*"
logme "# loaded env file $ENVFILE"
if [ "x$DOIT" == "x0" ]; then
  logme "# DOIT=$DOIT: Not doing anything, dry mode."
  logme "# DOIT=$DOIT: Would be using this logfile in doit-mode: $UPDATELOGFILE"
fi


# XXX so the lgsm updater doesnt cry about not wherever you may be starting out.
OLDPWD=`pwd`
cd /tmp/

SELINUXMODE=`$SELXGETENF`
logme "# SELinux-Mode is '$SELINUXMODE'"
DORESTORECON=0
[ "x$SELINUXMODE" == "xEnforcing" ] && DORESTORECON=1
[ "x$SELINUXMODE" == "xPermissive" ] && DORESTORECON=1

# technically an else would be sufficient here:
logme "# starting.. by doing: $SYSDCTL stop $SYSDSVCNAME"
[ "x$DOIT" == "x1" ] && $SYSDCTL stop $SYSDSVCNAME >>$UPDATELOGFILE 2>&1
[ "x$DORESTORECON" == "x1" ] && logme "# cont'ing.. selinux seems to be active, thus doing: $SELXRESTCON -vR $SVCDIR" && $SELXRESTCON -vR $SVCDIR >>$UPDATELOGFILE 2>&1
logme "# cont'ing.. by doing: sudo -u $SVCUSER -- $LGSMSERVERBIN update-lgsm"
[ "x$DOIT" == "x1" ] && sudo -u $SVCUSER -- $LGSMSERVERBIN update-lgsm >>$UPDATELOGFILE 2>&1
logme "# cont'ing.. by doing: sudo -u $SVCUSER -- $LGSMSERVERBIN check-update && sudo -u $SVCUSER -- $LGSMSERVERBIN force-update"
[ "x$DOIT" == "x1" ] && sudo -u $SVCUSER -- $LGSMSERVERBIN check-update >>$UPDATELOGFILE 2>&1 && sudo -u $SVCUSER -- $LGSMSERVERBIN force-update >>$UPDATELOGFILE 2>&1
[ "x$DOIT" == "x1" ] && [ "x$DORESTORECON" == "x1" ] && logme "# cont'ing.. selinux seems to be active, thus doing: $SELXRESTCON -vR $SVCDIR" && $SELXRESTCON -vR $SVCDIR >>$UPDATELOGFILE 2>&1
logme "# cont'ing.. by doing: sudo -u $SVCUSER -- $LGSMSERVERBIN mods-update"
[ "x$DOIT" == "x1" ] &&  sudo -u $SVCUSER -- $LGSMSERVERBIN mods-update >>$UPDATELOGFILE 2>&1
logme "# cont'ing.. by doing: sudo -u $SVCUSER -- $LGSMSERVERBIN stop"
[ "x$DOIT" == "x1" ] &&  sudo -u $SVCUSER -- $LGSMSERVERBIN stop >>$UPDATELOGFILE 2>&1
logme "# finishing up.. by doing: $SYSDCTL start $SYSDSVCNAME"
[ "x$DOIT" == "x1" ] &&  $SYSDCTL start $SYSDSVCNAME >>$UPDATELOGFILE 2>&1
logme "# fin."

cd "$OLDPWD"

if [ "x$UID" == "x0" ]; then				# make sure our files are as server-username, so lgsm update doesnt fail to restart the server.
  chown $SVCUSER:$SVCUSER $UPDPATELOGFILE >/dev/null 2>&1
fi

exit 0

