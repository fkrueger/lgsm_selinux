#!/bin/bash


# XXX 6000 days works well on 2021-12-08
whatiscustom_in_days="6000"

webhn="vm106"
webdir="/var/www/ut2004.holics.at/files/bw1.4"
ut2k4sysdir="/opt/ut2k4server/serverfiles/System"

OLDPWD=`pwd`
cd "$ut2k4sysdir"

echo "# Started at " `date +%Y%m%d_%H%M%S`
echo "## Clearing old ~/.ut2004/ & ~/.ut-tmp/ target dirs:"
rm -vrf ~/.ut2004/* ~/.ut-tmp/*

echo "## Compress all .u* files with ucc-bin compress (which end up in ~/.ut2004/ somehow):"
find /opt/ut2k4server/serverfiles/ -mtime "-$whatiscustom_in_days" | grep '\.u' | grep -vP '\.ucl$' | grep -v /Help | while read fn; do echo "> $fn"; /opt/ut2k4server/serverfiles/System/ucc-bin compress $fn; done

echo "## Find all .uz2 files in ~/.ut2004/ and collect these in one place for rsyncing:"
[ ! -d ~/.ut-tmp/ ] && mkdir ~/.ut-tmp
find ~/.ut2004/ -iname "*.uz2" -exec mv {} ~/.ut-tmp/ \;

echo "## rsync all .uz2 files in ~/.ut-tmp/ to target redirect webserver $webhn:$webdir/"
rsync -avuz --delete ~/.ut-tmp/ $webhn:$webdir/

echo "## Clearing up after us (locally):"
rm -vrf ~/.ut2004/* ~/.ut-tmp/*

cd "$OLDPWD"
echo "# Finished at " `date +%Y%m%d_%H%M%S`

