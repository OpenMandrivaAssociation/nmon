Summary:	Performance analysis tool
Name:		nmon
Version:	14g
Release:	2
License:	GPLv3
Group:		Monitoring
URL:		http://nmon.sourceforge.net/
Source0:	http://dl.sf.net/sourceforge/nmon/lmon%{version}.c
Source1:	http://dl.sf.net/sourceforge/nmon/makefile
Source2:	http://dl.sf.net/sourceforge/nmon/Documentation.txt
BuildRequires: ncurses-devel
#BuildRequires: /usr/include/linux/version.h

%description
nmon is designed for performance specialists to use for monitoring and
analyzing performance data.

%prep
%setup -c -T
%{__install} -p -m0644 %{SOURCE0} .
%{__install} -p -m0644 %{SOURCE1} .
%{__install} -p -m0644 %{SOURCE2} .

%{__cat} <<EOF >nmon-script.sysconfig
### The directory to store the nmon data files
NMONDIR="/var/log/nmon"

### Default options for nmon
OPTIONS="-f -t"

### Number of days to keep nmon data files
KEEPDAYS="31"
EOF

%{__cat} <<'EOF' >nmon-script.sh
#!/bin/bash

### Please make modifications to the options and path in /etc/sysconfig/nmon-script

### Default variables
SYSCONFIG="/etc/sysconfig/nmon-script"
NMONDIR="/var/log/nmon"
OPTIONS="-f -t"
KEEPDAYS="31"

### Read configuration
[ -r "$SYSCONFIG" ] && source "$SYSCONFIG"

### Kill the old process(es)
/usr/bin/pkill -x -f "/usr/bin/nmon $OPTIONS -m $NMONDIR"

### Remove old log files
/usr/bin/find $NMONDIR -ctime +$KEEPDAYS -daystart -type f | xargs rm -f

### Start the new process
exec /usr/bin/nmon $OPTIONS -m $NMONDIR
EOF

%{__cat} <<EOF >nmon-script.cron
0 0 * * * nobody /usr/bin/nmon-script
EOF

%build
%{__cc} %{optflags} -D GETUSER -D JFS -D LARGEMEM -lncurses lmon%{version}.c -o nmon

%install
install -Dp -m0755 nmon %{buildroot}%{_bindir}/nmon

install -d -m0755 %{buildroot}%{_localstatedir}/log/nmon/
install -Dp -m0755 nmon-script.sh %{buildroot}%{_bindir}/nmon-script
install -Dp -m0644 nmon-script.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/nmon-script
install -Dp -m0644 nmon-script.cron %{buildroot}%{_sysconfdir}/cron.d/nmon-script

%files
%doc Documentation.txt
%config(noreplace) %{_sysconfdir}/sysconfig/nmon-script
%config %{_sysconfdir}/cron.d/nmon-script
%{_bindir}/nmon
%{_bindir}/nmon-script

%defattr(-, nobody, nobody, 0755)
%{_localstatedir}/log/nmon/


%changelog
* Sat Dec 17 2011 Alexander Khrukin <akhrukin@mandriva.org> 14g-1
+ Revision: 743226
- imported package nmon

