#!/bin/bash

TF2LOGDIR="/opt/tf2server/serverfiles/tf/logs"
TF2_PLAYERLOG="/opt/tf2server/serverfiles/tf/logs/tf2server_player.log"


TS=`date +%Y%m%d_%H%M%S`

logme() {
  echo "$*" >>$TF2_PLAYERLOG
}

logme ""
logme "----------------------------------------------------------------------------"
logme "# date: $TS"
grep "entered the game" $TF2LOGDIR/l*.log |grep -vP '(BLU|config_bot|ThePyroOverlord|<BOT>)' | grep -v Hispeeday | sort -u >>$TF2_PLAYERLOG

