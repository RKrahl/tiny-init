%if 0%{?centos_version} || 0%{?rhel_version}
%global python3_pkgversion 36
%else
%global python3_pkgversion 3
%if 0%{?sle_version} && 0%{?sle_version} < 150000
%global __python3 /usr/bin/python3
%endif
%endif


Name:		tiny-init
Version:	0.6
Release:	1
Summary:	Minimal implementation of an init process
License:	Apache-2.0
Group:		System/Base
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel
Requires:	python%{python3_pkgversion}-psutil >= 2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
The init process is the parent of all other processes.  This package
provides a Python script as a rather minimal implementation.  It takes
a command as argument and spawns a sub process.  Then it waits for
child processes, propagates signals to them, and reaps those that are
terminated.  If the last child process is gone, it terminates itself.


%prep
%setup -q


%build
%__python3 setup.py build


%install
%__python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --install-scripts=%{_sbindir}
%__mv %{buildroot}%{_sbindir}/init.py %{buildroot}%{_sbindir}/tiny-init


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%exclude %{python3_sitelib}/*
%{_sbindir}/tiny-init


%changelog
