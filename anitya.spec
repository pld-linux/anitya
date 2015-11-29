#
# Conditional build:
## Running the tests would require having flask >= 0.10
%bcond_with	tests	# do not perform "make test"

Summary:	Monitor upstream releases and announce them on fedmsg
Name:		anitya
Version:	0.1.14
Release:	0.1
License:	GPL v2+
Group:		Applications/WWW
Source0:	https://fedorahosted.org/releases/a/n/anitya/%{name}-%{version}.tar.gz
# Source0-md5:	4e97c1b372778f86bf7a9055bbcad53c
URL:		http://fedorahosted.org/anitya/
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	python-SQLAlchemy >= 0.7.4
BuildRequires:	python-bunch
BuildRequires:	python-flask-openid
BuildRequires:	python-flask-wtf
%if %{with tests}
BuildRequires:	fedmsg
BuildRequires:	python-dateutil
BuildRequires:	python-devel
BuildRequires:	python-docutils
BuildRequires:	python-flask
BuildRequires:	python-markupsafe
BuildRequires:	python-openid
BuildRequires:	python-setuptools
BuildRequires:	python-straight-plugin
BuildRequires:	python-wtforms
%endif
#Requires:	apache-mod_wsgi
Requires:	fedmsg
Requires:	python-SQLAlchemy >= 0.7.4
Requires:	python-bunch
Requires:	python-dateutil
Requires:	python-docutils
Requires:	python-flask
Requires:	python-flask-openid
Requires:	python-flask-wtf
Requires:	python-markupsafe
Requires:	python-openid
Requires:	python-setuptools
Requires:	python-straight-plugin
Requires:	python-wtforms
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
We monitor upstream releases and broadcast them on fedmsg, the
FEDerated MeSsaGe (fedmsg) bus.

%prep
%setup -q

%build
%py_build

%if %{with tests}
./runtests.sh
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%py_postclean

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_datadir}/%{name}}

# Install apache configuration file
cp -p files/anitya.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/httpd.conf

# Install configuration file
cp -p files/anitya.cfg.sample $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/anitya.cfg

# Install WSGI file
cp -p files/anitya.wsgi $RPM_BUILD_ROOT%{_datadir}/%{name}/anitya.wsgi

# Install the createdb script
cp -p createdb.py $RPM_BUILD_ROOT%{_datadir}/%{name}/anitya_createdb.py

# Install the migrate_wiki script
cp -p files/migrate_wiki.py $RPM_BUILD_ROOT%{_datadir}/%{name}/anitya_migrate_wiki.py

# Install the cron script
cp -p files/anitya_cron.py $RPM_BUILD_ROOT%{_datadir}/%{name}/anitya_cron.py

# Install the alembic files
#cp -r alembic $RPM_BUILD_ROOT%{_datadir}/%{name}
#install -m 644 files/alembic.ini $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/alembic.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/anitya.cfg
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/alembic.ini
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/httpd.conf
%attr(755,root,root) %{_bindir}/anitya_cron.py
%{_datadir}/%{name}
%{py_sitescriptdir}/anitya
%{py_sitescriptdir}/anitya-%{version}-py*.egg-info
