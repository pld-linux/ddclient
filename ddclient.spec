%include	/usr/lib/rpm/macros.perl
Summary:	A dynamic IP address utility
Summary(pl.UTF-8):	Narzędzie do dynamicznych adresów IP
Summary(pt_BR.UTF-8):	Cliente para atualizar entradas DNS dinâmicas no DynDNS.org
Name:		ddclient
Version:	3.8.3
Release:	1
Epoch:		1
License:	GPL v2
Group:		Networking
Source0:	http://downloads.sourceforge.net/ddclient/%{name}-%{version}.tar.bz2
# Source0-md5:	3b426ae52d509e463b42eeb08fb89e0b
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.NetworkManager
Source4:	%{name}-tmpfiles.conf
Patch0:		config.patch
# https://github.com/wimpunk/ddclient
URL:		http://ddclient.sourceforge.net/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Provides:	group(ddclient)
Provides:	user(ddclient)
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
# for freedns: Digest::SHA1, IO::Socket::SSL
Suggests:	perl-Digest-SHA1
Suggests:	perl-IO-Socket-SSL
# for cloudflare JSON::Any
Suggests:	perl-JSON-Any
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cachedir	%{_localstatedir}/cache/ddclient
%define		rundir		%{_localstatedir}/run/ddclient

%description
DDclient is a small full featured client with FULL DynDNS NIC2
support, requiring only Perl and no additional modules. It runs under
most UNIX OSes and has been tested under Linux and FreeBSD. Supported
features include: operating as a daemon, manual and automatic updates,
static and dynamic updates, optimized updates for multiple addresses,
MX, wildcards, abuse avoidance, retrying failed updates, and sending
update status to syslog and through e-mail. This release may now
obtain your IP address from any interface, web based IP detection,
Watchguard's SOHO router, Netopia's R910 router, SMC's Barricade
broadband router, Netgear's RT3xx router, Linksys' broadband routers,
MaxGate's UGATE-3x00 routers, ELSA's LANCOM DSL/10 routers and now
provides Full support for DynDNS.org's NIC2 protocol. Support is also
included for other dynamic DNS services. Comes with sample scripts for
use with DHCP, PPP, and cron. See the README for more information.

%description -l pl.UTF-8
DDclient to mały, w pełni funkcjonalny klient z PEŁNĄ obsługą DynDNS
NIC2, wymagający tylko Perla bez żadnych dodatkowych modułów. Działa
pod większością systemów uniksowych, był testowany pod Linuksem i
FreeBSD. Jego możliwości to między innymi: praca jako demon, ręczne i
automatyczne uaktualnienia, statyczne i dynamiczne uaktualnienia,
uaktualnienia zoptymalizowane dla wielu adresów, MX-y, wildcardy,
zapobieganie nadużyciom, ponawianie nieudanych uaktualnień, wysyłanie
statusu uaktualnień do sysloga i pocztą. Ta wersja może pobrać adres
IP z dowolnego interfejsu, wykrywania przez WWW, routerów: Watchguard
SOGO, szerokopasmowych SMC Barricane, Netgear RT3xx, szerokopasmowych
Linksys, MaxGate UGATE-3x00, ELSA LANCOM DSL/10, a teraz także ma
pełną obsługę protokołu DynDNS NIC2. Ma także wsparcie dla innych
usług dynamicznego DNS. Zawiera przykładowe skrypty do używania z
DHCP, PPP i cronem. Więcej informacji w README.

%description -l pt_BR.UTF-8
O ddclient é um cliente perl usada para atualizar entradas DNS
dinâmicas em contas do serviço de DNS dinâmico gratuito. Veja
<http://www.dyndns.org> para obter detalhes sobre como obter uma conta
gratuita.

%prep
%setup -q
cp -p sample-etc_ddclient.conf %{name}.conf
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/{rc.d/init.d,sysconfig,NetworkManager/dispatcher.d}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{systemdtmpfilesdir},%{cachedir},%{rundir}}

cp -p %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -p %{name} $RPM_BUILD_ROOT%{_sbindir}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d/50-%{name}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
touch $RPM_BUILD_ROOT%{cachedir}/%{name}.cache

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 325 ddclient
%useradd -u 525 -d /var/run/%{name} -g ddclient -c "ddclient user" ddclient

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "%{name} daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove ddclient
	%groupremove ddclient
fi

%triggerpostun -- ddclient < 1:3.6.4
if [ -f /etc/ddclient.conf.rpmsave ]; then
	echo "Moving config to new location /etc/ddclient"
	mv -f /etc/ddclient/ddclient.conf /etc/ddclient/ddclient.conf.rpmnew
	mv -f /etc/ddclient.conf.rpmsave /etc/ddclient/ddclient.conf
	mv -f /etc/ddclient.cache /etc/ddclient.cache.rpmsave
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog Changelog.old README*
%attr(755,root,root) %{_sbindir}/ddclient
%dir %{_sysconfdir}/%{name}
# switch to %attr(640,root,ddclient) when this gets resolution: https://sourceforge.net/p/ddclient/bugs/77/
%attr(600,ddclient,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) /etc/NetworkManager/dispatcher.d/50-%{name}
%{systemdtmpfilesdir}/%{name}.conf

%dir %attr(770,root,ddclient) %{cachedir}
%ghost %attr(600,ddclient,ddclient) %ghost %{cachedir}/%{name}.cache
%dir %attr(770,root,ddclient) %{rundir}
