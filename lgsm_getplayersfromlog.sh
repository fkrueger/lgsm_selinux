#!/bin/bash

## defaults:
SVCNAME="tf2server"
SVCUSER="tf2server"
SVCDIR="/opt/$SVCNAME"

SVCLOGDIR="$SVCDIR/log/server"

PLAYERSEARCHIE="entered the game"
PLAYERSERVERLOGS="l*.log"
PLAYERFAKENAMES="(BLU|config_bot|ThePyroOverlord|<BOT>)"
PLAYERLOGFILE="$SVCLOGDIR/${SVCNAME}_player.log"
PLAYERLASTLOGSEEN="$SVCLOGDIR/${SVCNAME}_player.lastlogfileseen.log"


usage() {
  echo "usage: $0 [servicename] <doit|showit>"
  echo ""
  echo "    get player-logins from server logfile, and write it into $PLAYERLOGFILE ."
  echo "    you can add [servicename] to load a custom env file from /etc/sysconfig, eg. supply tf2server-2 to load /etc/sysconfig/tf2server-2 ."
  echo ""
  echo "    add 'doit' do actually do something."
  echo "    add 'showit' to only show our current logfile $PLAYERLOGFILE ."
  echo ""
  exit -1
}


logme() {
  TS=`date +%Y%m%d_%H%M%S`
  if [ "x$DOIT" == "x1" ]; then
    echo "$TS: $*" >>$PLAYERLOGFILE
  else
    echo "$TS: $*"
  fi
}

DOIT=0
[ "x$1" == "xdoit" ] && DOIT=1
if [ "x$DOIT" == "x0" ]; then
  ENVFILE="/etc/sysconfig/$1"
  if [ -e "$ENVFILE" ]; then
    source $ENVFILE
    [ "x$2" == "xdoit" ] && DOIT=1
  else
    if [ "x$1" != "x" ] && [ "x$1" != "xdoit" ] && [ "x$1" != "xshowit" ]; then
      echo "!!! Problem loading env file $ENVFILE . Exitting."
      exit 1
    fi
  fi
fi

if [ "x$1" == "-h" ] || [ "x$1" == "--help" ]; then
  usage
fi

if [ "x$2" == "xshowit" ]; then
  cat $PLAYERLOGFILE | sort -u
  exit 0
fi



logme ""
logme "----------------------------------------------------------------------------"
logme "# date: $TS"
logme "# loaded env file $ENVFILE"

if [ "x$DOIT" == "x0" ]; then
  logme "# DOIT=$DOIT: Not doing anything, dry mode."
  logme "# DOIT=$DOIT: Would be using this logfile in doit-mode: $PLAYERLOGFILE"
fi


lastlogfound="0"

[ ! -e "$PLAYERLASTLOGSEEN" ] && touch "$PLAYERLASTLOGSEEN"
LASTLOGSEEN=`cat $PLAYERLASTLOGSEEN`
if [ "x$LASTLOGSEEN" == "x" ]; then
  logme "# lastlogseen: none; parsing all logfiles available."
  lastlogfound="1"
else
  LASTLOGSEEN="${LASTLOGSEEN##*/}"
  logme "# lastlogseen: $LASTLOGSEEN. Starting there."
fi


###
### main
###

[ "x$DOIT" == "x0" ] && PLAYERLOGFILE="/dev/stdout"
logme "# grabbing player names: grep \"$PLAYERSEARCHIE\" $SVCLOGDIR/$PLAYERSERVERLOGS |grep -vP "$PLAYERFAKENAMES" | sort -u"
for fn in $SVCLOGDIR/$PLAYERSERVERLOGS; do
  fn="${fn##*/}"
  if [ "x$lastlogfound" == "x0" ]; then
    if [ "x$LASTLOGSEEN" == "x$fn" ]; then
      lastlogfound="1"
    else
      echo "## skipping old log $fn"
    fi
  fi

  if [ "x$lastlogfound" == "x1" ]; then
    echo ">> parsing log $fn:"
    grep "$PLAYERSEARCHIE" $SVCLOGDIR/$fn |grep -vP "$PLAYERFAKENAMES" | sort -u >>$PLAYERLOGFILE
  fi
done

[ "x$DOIT" == "x1" ] && echo "$fn" >$PLAYERLASTLOGSEEN

logme "#fin"
