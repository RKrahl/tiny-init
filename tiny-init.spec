Name:		tiny-init
Version:	0.1
Release:	1
Summary:	Minimal implementation of an init process
License:	Apache-2.0
Group:		System/Base
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python-devel >= 2.6
Requires:	python-base >= 2.6
Requires:	python-psutil >= 2.0
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
python setup.py build


%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --install-scripts=%{_sbindir}
%__mv %{buildroot}%{_sbindir}/init.py %{buildroot}%{_sbindir}/init


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%exclude %{python_sitelib}/*
%{_sbindir}/init


%changelog
