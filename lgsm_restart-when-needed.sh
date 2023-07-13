#!/bin/bash


## defaults:
SVCGAME="tf2server"
SVCNAME="tf2server"
SVCUSER="tf2server"
SVCDIR="/opt/$SVCNAME"

LGSMLOGDIR="$SVCDIR/log"
SVCLOGDIR="$LGSMLOGDIR/server"
CONSLOGDIR="$LGSMLOGDIR/console"
CONSLOGFILE="$CONSLOGDIR/tf2server-console.log"

RESTARTSEARCHIE="non working searchie input for grep"
RESTARTLOGFILE="$CONSLOGFILE"



# automatically created
SYSDSVCNAME="$SVCGAME@$SVCNAME"


usage() {
  echo "usage: $0 [servicename] <doit|showit>"
  echo ""
  echo "    Checks the current console logfile for the default 'server needs to be restarted' message, and restarts the service (if seen)."
  echo ""
  echo "    you can add [servicename] to load a custom env file from /etc/sysconfig/[servicename].env, eg. supply tf2server-2 to load /etc/sysconfig/tf2server-2.env ."
  echo ""
  echo "    add 'doit' do actually do something."
  echo "    add 'showit' to only show our current console logfile $CONSLOGFILE ."
  echo ""
  echo ""
  echo "    cmd can be: -h, --help ."
  echo ""
  if [ "x$1" != "x" ]; then
    echo "!!! Error: $1"
    echo ""
    exit 99
  fi
  exit -1
}


logme() {
  TS=`date +%Y%m%d_%H%M%S`
  echo "$TS: $*"
}


DOIT=0
[ "x$1" == "xdoit" ] && DOIT=1
if [ "x$DOIT" == "x0" ]; then
  ENVFILE="/etc/sysconfig/$1.env"
  if [ -e "$ENVFILE" ] && [ ! -d "$ENVFILE" ]; then
    source $ENVFILE
    [ "x$2" == "xdoit" ] && DOIT=1
  else
    if [ "x$1" != "x" ] && [ "x$1" != "xdoit" ] && [ "x$1" != "xshowit" ]; then
      usage "Problem loading env file $ENVFILE . Exitting."
      exit 1
    fi
    ENVFILE=""
  fi
fi

if [ "x$1" == "-h" ] || [ "x$1" == "--help" ] || [ "x$1" == "xhelp" ]; then
  usage
fi

if [ "x$2" == "xshowit" ]; then
  cat $CONSLOGFILE
  exit 0
fi



logme ""
logme "----------------------------------------------------------------------------"
logme "# date: $TS"
[ "x$ENVFILE" != "x" ] && logme "# loaded env file $ENVFILE"

if [ "x$DOIT" == "x0" ]; then
  logme "# DOIT=$DOIT: Not doing anything, dry mode."
  logme "# DOIT=$DOIT: Would be using this logfile in doit-mode: $CONSLOGFILE"
fi


# defaults
if [ ! -d "$SVCDIR" ]; then
  usage "Instancename '$SVCNAME' doesn't have accompanying basedir '$SVCDIR'. Exitting."
fi



logme() {
  TS=`date +%Y%m%d_%H%M%S`
  echo "$TS: $*"
}



if [ "x$1" == "x--show" ]; then
  cat $CONSLOGFILE
  exit 0
fi


## the doit part:
RC=255
logme ""
logme "----------------------------------------------------------------------------"
logme "# Started."

grep "$RESTARTSEARCHIE" $RESTARTLOGFILE
if [ "x$?" == "x0" ]; then 			# if found: 
  logme ". tf2server instance with name '$SVCNAME' (in svcdir $SVCDIR): Found message 'server needs to be started'.. Trigger restart:"
  if [ -x "/usr/sbin/service" ]; then
    if [ "x$DOIT" == "x0" ]; then
      logme ".. Would now restart instance $SYSDSVCNAME via service, but DOIT=$DOIT .. Skipping."
    else
      logme ".. Stopping instance $SVCNAME via service:"
      /usr/sbin/service $SYSDSVCNAME stop
      logme ".. Starting instance $SVCNAME via service:"
      /usr/sbin/service $SYSDSVCNAME start
      RC=99
      /usr/sbin/service $SYSDSVCNAME status
      if [ "x$?" == "x0" ]; then
        logme ".. Service $SYSDSVCNAME seems to have been successfully restarted (according to service)"
        RC=0
      fi
    fi
  elif [ -x "/usr/bin/systemctl" ]; then
    if [ "x$DOIT" == "x0" ]; then
      logme ".. Would now restart instance $SVCNAME via systemctl, but DOIT=$DOIT .. Skipping."
    else
      logme ".. Stopping instance $SYSDSVCNAME via systemctl:"
      /usr/bin/systemctl stop $SYSDSVCNAME.service
      logme ".. Starting instance $SYSDSVCNAME via systemctl:"
      /usr/bin/systemctl start $SYSDSVCNAME.service
      RC=99
      /usr/bin/systemctl status $SYSDSVCNAME.service
      if [ "x$?" == "x0" ]; then
        logme ".. Service $SYSDSVCNAME seems to have been successfully restarted (according to systemctl)"
        RC=0
      fi
    fi
  elif [ -x "/etc/init.d/$SVCNAME" ]; then
    if [ "x$DOIT" == "x0" ]; then
      logme ".. Would now restart instance $SVCNAME via SysV /etc/init.d/$SVCNAME, but DOIT=$DOIT .. Skipping."
    else
      logme ".. Stopping instance $SVCNAME via SysV /etc/init.d/$SVCNAME:"
      /etc/init.d/$SVCNAME stop
      logme ".. Starting instance $SVCNAME via SysV /etc/init.d/$SVCNAME:"
      /etc/init.d/$SVCNAME start
      RC=99
      /etc/init.d/$SVCNAME status
      if [ "x$?" == "x0" ]; then
        logme ".. Instance $SVCNAME seems to have been successfully restarted (according to init.d)"
        RC=0
      fi
    fi
  else
    logme "!!! Unknown service control tool. Can't restart tf2server instance $SVCNAME. Exitting."
  fi
else
  logme ". tf2server instance with name '$SVCNAME' (in svcdir $SVCDIR): Nothing to do. Exitting."
fi

logme "# Finished."


exit $RC
#fin
