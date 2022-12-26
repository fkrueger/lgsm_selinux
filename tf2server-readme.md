# NAME

tf2server\_selinux - Security Enhanced Linux Policy for the tf2server
processes

# LINKS

Finished RPMs for CentOS 8 (Stream) and maybe even Fedora can be found here: **https://dev.techno.holics.at/technoholics-repo/

Simply do the usual dance with

  yum install https://dev.techno.holics.at/technoholics-repo/el8/technoholics-repo-release-20210620-1.el8.noarch.rpm

And go on from there.

Enjoy!


# DESCRIPTION

Security-Enhanced Linux secures the tf2server processes via flexible
mandatory access control.

The tf2server processes execute with the tf2server\_t SELinux type. You
can check if you have these processes running by executing the **ps**
command with the **-Z** qualifier.

For example:

**ps -eZ | grep tf2server\_t**

# IMPORTANT

The selinux policy only works if the tf2server is managed by lgsm (
https://linuxgsm.com/ ) and the files are installed under
/opt/tf2server\*/ \!

# TODO

Extend policy to include more granular control for the lgsm scripts as
well.

Extend policy to include more of the lgsm servers (ie. support more than
just tf2server).

Create better documentation (add managed files \<-\> context overview
automatically).

# ENTRYPOINTS

The tf2server\_t SELinux type can be entered via the
**tf2server\_exec\_t** file type.

The default entrypoint paths for the tf2server\_t domain are the
following:

/opt/tf2server.\*/tf2server

# PROCESS TYPES

SELinux defines process types (domains) for each process running on the
system

You can see the context of a process using the **-Z** option to **psP**

Policy governs the access confined processes have to files. SELinux
tf2server policy is very flexible allowing users to setup their
tf2server processes in as secure a method as possible.

The following process types are defined for tf2server:

    tf2server_t

Note: **semanage permissive -a tf2server\_t** can be used to make the
process type tf2server\_t permissive. SELinux does not deny access to
permissive process types, but the AVC (SELinux denials) messages are
still generated.

# BOOLEANS

SELinux policy is customizable based on least access required. tf2server
policy is extremely flexible and has several booleans that allow you to
manipulate the policy and run tf2server with the tightest access
possible.

If you want to allow the tf2server processes to write core-dumps into
/tmp/dumps/, you can turn on the tf2server\_allow\_coredumps\_in\_tmp
boolean. Disabled by default.

    setsebool -P tf2server_allow_coredumps_in_tmp 1

# MANAGED FILES

The SELinux process type tf2server\_t can manage files labeled with the
following file types. The paths listed are the default paths for these
file types. Note the processes UID still need to have DAC permissions.

  
**tf2server\_\*\_t**

TODO add those later, in the meantime look in the source code in
tf2server.fc OR use ls -alR /opt/tf2server/

/some/path  

# FILE CONTEXTS

SELinux requires files to have an extended attribute to define the file
type.

You can see the context of a file using the **-Z option to lsP**

Policy governs the access confined processes have to these files.
SELinux tf2server policy is very flexible allowing users to setup their
tf2server processes in as secure a method as possible.

*The following file types are defined for tf2server:*

``` 

tf2server_exec_t
```

\- Set files with the tf2server\_exec\_t type, if you want to transition
an executable to the tf2server\_t domain.

  

  - Paths:  
    /opt/tf2server\*/tf2server

Note: File context can be temporarily modified with the chcon command.
If you want to permanently change the file context you need to use the
**semanage fcontext** command. This will modify the SELinux labeling
database. You will need to use **restorecon** to apply the labels.

# COMMANDS

**semanage fcontext** can also be used to manipulate default file
context mappings.

**semanage permissive** can also be used to manipulate whether or not a
process type is permissive.

**semanage module** can also be used to enable/disable/install/remove
policy modules.

**semanage boolean** can also be used to manipulate the booleans

**system-config-selinux** is a GUI tool available to customize SELinux
policy settings.

# AUTHOR

This manual page was auto-generated using **sepolicy manpage .**

# SEE ALSO

selinux(8), semanage(8), restorecon(8), chcon(1), sepolicy(8),
setsebool(8)

