%include	/usr/lib/rpm/macros.perl
Summary:	A dynamic IP address utility
Summary(pl):	Narz�dzie do dynamicznych adres�w IP
Summary(pt_BR):	Cliente para atualizar entradas DNS din�micas no DynDNS.org
Name:		ddclient
Epoch:		1
Version:	3.6.6
Release:	1
Group:		Networking
License:	GPL
Source0:	http://dl.sourceforge.net/ddclient/%{name}-%{version}.tar.bz2
# Source0-md5:	5fd0f82446fbed857c841a4deb83cdb9
Source1:	%{name}.init
URL:		http://ddclient.sourceforge.net/
BuildRequires:	rpm-perlprov
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl
DDclient to ma�y, w pe�ni funkcjonalny klient z PE�N� obs�ug� DynDNS
NIC2, wymagaj�cy tylko Perla bez �adnych dodatkowych modu��w. Dzia�a
pod wi�kszo�ci� system�w uniksowych, by� testowany pod Linuksem i
FreeBSD. Jego mo�liwo�ci to mi�dzy innymi: praca jako demon, r�czne
i automatyczne uaktualnienia, statyczne i dynamiczne uaktualnienia,
uaktualnienia zoptymalizowane dla wielu adres�w, MX-y, wildcardy,
zapobieganie nadu�yciom, ponawianie nieudanych uaktualnie�, wysy�anie
statusu uaktualnie� do sysloga i poczt�. Ta wersja mo�e pobra� adres
IP z dowolnego interfejsu, wykrywania przez WWW, router�w: Watchguard
SOGO, szerokopasmowych SMC Barricane, Netgear RT3xx, szerokopasmowych
Linksys, MaxGate UGATE-3x00, ELSA LANCOM DSL/10, a teraz tak�e ma
pe�n� obs�ug� protoko�u DynDNS NIC2. Ma tak�e wsparcie dla innych
us�ug dynamicznego DNS. Zawiera przyk�adowe skrypty do u�ywania z
DHCP, PPP i cronem. Wi�cej informacji w README.

%description -l pt_BR
O ddclient � um cliente perl usada para atualizar entradas DNS
din�micas em contas do servi�o de DNS din�mico gratuito. Veja
http://www.dyndns.org para obter detalhes sobre como obter uma conta
gratuita.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ddclient,/etc/rc.d/init.d,%{_sbindir}}

install sample-etc_ddclient.conf $RPM_BUILD_ROOT/etc/%{name}/%{name}.conf
install %{name} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
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

%triggerpostun -- ddclient < 1:3.6.4
if [ -f /etc/ddclient.conf.rpmsave ]; then
	echo "Moving config to new location /etc/ddclient"
	mv -f /etc/ddclient/ddclient.conf /etc/ddclient/ddclient.conf.rpmnew
	mv -f /etc/ddclient.conf.rpmsave /etc/ddclient/ddclient.conf
	mv -f /etc/ddclient.cache /etc/ddclient.cache.rpmsave
fi

%files
%defattr(644,root,root,755)
%doc README*
%attr(755,root,root) %{_sbindir}/*
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/%{name}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
