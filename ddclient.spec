%include	/usr/lib/rpm/macros.perl
Name:		ddclient
Epoch:		1
Version:	3.6.3
Release:	1
Summary:	A dynamic IP address utility
Summary(pt_BR):	Cliente para atualizar entradas DNS dinâmicas no DynDNS.org
Group:		Networking
License:	GPL
URL:		http://burry.ca:4141/ddclient/
Source0:	http://members.rogers.com/ddclient/pub/%{name}-%{version}.tar.gz
# Source0-md5:	1773aaf469a1faddd3f20d485a0fd6f2
Source1:	%{name}.init
BuildArch:	noarch
BuildRequires:	rpm-perlprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Features: FULL DynDNS NIC2 support and now Custom updates and an RPM!
DDclient is a small full featured client requiring only Perl and no
additional modules. It runs under most UNIX OSes and has been tested
under Linux and FreeBSD. Supported features include: operating as a
daemon, manual and automatic updates, static and dynamic updates,
optimized updates for multiple addresses, MX, wildcards, abuse
avoidance, retrying failed updates, and sending update status to
syslog and through e-mail. This release may now obtain your IP address
from any interface, web based IP detection, Watchguard's SOHO router,
Netopia's R910 router, SMC's Barricade broadband router, Netgear's
RT3xx router, Linksys' broadband routers, MaxGate's UGATE-3x00
routers, ELSA's LANCOM DSL/10 routers and now provides Full support
for DynDNS.org's NIC2 protocol. Support is also included for other
dynamic DNS services. Comes with sample scripts for use with DHCP,
PPP, and cron. See the README for more information.

%description -l pt_BR
O ddclient é um cliente perl usada para atualizar entradas DNS
dinâmicas em contas do serviço de DNS dinâmico gratuito. Veja
http://www.dyndns.org para obter detalhes sobre como obter uma conta
gratuita.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir}}

install sample-etc_ddclient.conf $RPM_BUILD_ROOT/etc/%{name}.conf
install %{name} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart >&2
else
        echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop >&2
        fi
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
