# INSTALLATION via repository
This git-repo contains the files needed to create accompanying RPM files for CentOS/RHEL8 (el8).

The compiled SElinux policy module should also work on Fedora, and maybe even earlier versions of CentOS.

A complete version of the resulting RPM file can be found in my technoholics-repo.
It can be found here: https://dev.techno.holics.at/technoholics-repo/

## Easy installation with technoholics-repo
* Download technoholics-repo-release-20210620-1.el8.noarch.rpm
* Install access to the techno.holics.at repository via
yum install https://dev.techno.holics.at/technoholics-repo/el8/technoholics-repo-release-20210620-1.el8.noarch.rpm
* If needed, the gpg key used for signing the RPM packages can be found here: https://dev.techno.holics.at/holics-repo/RPM-GPG-KEY-holicsrepo
* Now install the tf2server_selinux package with
yum install tf2server_selinux
* Now follow the following instructions under FIRST SETUP as needed.

# FIRST SETUP
This selinux policy module needs tf2server to be installed via the LinuxGSM installation scripts as can be found in https://linuxgsm.com/lgsm/tf2server/ .

Usually those scripts want to install into /home/tf2server/ (or a numbered version of this directory name).
For this SElinux policy module to work more securely, you have to install the tf2server into /opt/tf2server/ though.

If you do not want to do this and instead give successful attackers access to all user home directories (potentially),
you can set the following the sebool.

I didn't test tf2server installed under /home/tf2server(-[0-9]+)?/ , so you are on your own. It should work though.

## SystemD integration for tf2server
Example SystemD unit file:
<pre><code>
cat&lt;&lt;EOF > /etc/systemd/system/tf2server.service
[Unit]
Description=LinuxGSM TF2 Server
After=network-online.target opt.mount
Wants=network-online.target opt.mount

[Service]
Type=forking
User=tf2server
WorkingDirectory=/opt/tf2server
#Assume that the service is running after main process exits with code 0
RemainAfterExit=yes
ExecStart=/opt/tf2server/tf2server start
ExecStop=/opt/tf2server/tf2server stop
Restart=no

[Install]
WantedBy=multi-user.target

EOF
</code></pre>
Remember to adapt the WorkingDirectory and ExecStart parameter, if your tf2server is installed in ie. /opt/tf2server-2/ .

.. and activate the new SystemD unit file by reloading the daemon:
<pre><code>
 systemctl daemon-reload
</code></pre>
3. Reset SElinux contexts on the affected directories (can be used as debug, too, i.e. if something that should work doesn't work)
<pre><code>
 restorecon -vR /etc/ /home/ /opt/
</code></pre>
4. (Re)start tf2server
<pre><code>
 service tf2server restart
</code></pre>
5. Test your tf2server by looking at the log files in /opt/tf2server/log/server/ and use a game client to connect to your new tf2server instance.

__Congrats, you now should have a better secured Team Fortress 2 server instance running with SElinux!__

# Cheers!

