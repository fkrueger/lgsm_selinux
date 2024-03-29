#!/bin/bash

## defaults:
SVCGAME="tf2server"
SVCNAME="tf2server"
SVCUSER="tf2server"
SVCDIR="/opt/$SVCNAME"

SVCLOGDIR="$SVCDIR/log/server"
GETPLAYERSLOGFILE="$SVCDIR/${SVCNAME}-lgsm_getplayersfromlog.log"

PLAYERSEARCHIE="(entered the game|disconnected)"
PLAYERSERVERLOGS="l*.log"
PLAYERFAKENAMES="(BLU|config_bot|ThePyroOverlord|<BOT>)"
PLAYERLOGFILE="$SVCLOGDIR/${SVCNAME}_player.log"
PLAYERLASTLOGSEEN="$SVCLOGDIR/${SVCNAME}_player.lastlogfileseen.log"



# automatically created
SYSDSVCNAME="$SVCGAME@$SVCNAME"


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
    echo "$TS: $*" >>$GETPLAYERSLOGFILE
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
    if [ "x$1" != "x" ] && [ "x$1" != "xdoit" ] && [ "x$1" != "xshowit" ]; then
      echo "!!! Problem loading env file $ENVFILE . Exitting."
      exit 1
    fi
  fi
fi

if [ "x$1" == "-h" ] || [ "x$1" == "--help" ]; then
  usage
fi

if [ "x$UID" == "x0" ]; then				# make sure our files are as server-username, so lgsm update doesnt fail to restart the server.
  chown $SVCUSER:$SVCUSER $GETPLAYERSLOGFILE $PLAYERLOGFILE $PLAYERLASTLOGSEEN >/dev/null 2>&1
fi

if [ "x$2" == "xshowit" ]; then
  cat $PLAYERLOGFILE | sed -E 's/^L ([0-9]+)\/([0-9]+)\/([0-9]+) /LOG \3-\1-\2 /g' | sort -u
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
logme "# grabbing player names: grep -P \"$PLAYERSEARCHIE\" $SVCLOGDIR/$PLAYERSERVERLOGS |grep -vP "$PLAYERFAKENAMES" | sort -u"
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
    grep -P "$PLAYERSEARCHIE" $SVCLOGDIR/$fn |grep -vP "$PLAYERFAKENAMES" | sort -u >>$PLAYERLOGFILE
  fi
done

[ "x$DOIT" == "x1" ] && echo "$fn" >$PLAYERLASTLOGSEEN


if [ "x$UID" == "x0" ]; then				# make sure our files are as server-username, so lgsm update doesnt fail to restart the server.
  chown $SVCUSER:$SVCUSER $PLAYERLOGFILE $PLAYERLASTLOGSEEN $PLAYERUPDPATELOGFILE >/dev/null 2>&1
fi


logme "#fin"
