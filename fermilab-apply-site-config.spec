Name:		fermilab-apply-site-config
Version:	1.0
Release:	3%{?dist}

Summary:	Setup Fermilab On Site computing requirements

Group:		Fermilab
License:	GPL
URL:		https://github.com/fermilab-context-rpms/fermilab-apply-site-config

BuildArch:	noarch

# For RHEL8 and similar only
Requires:	base-module(platform:el8)

Requires(post):	rpm dnf coreutils util-linux

%description
This RPM will perform a number of installation tasks of other
RPMs on your behalf.  These installs happen invisibly but are
visable in the RPM transation logs.

This RPM will remove itself so that you can 'reinstall' it easily.


%prep

%build


%install
rm -rf %{buildroot}
mkdir %{buildroot}

%clean
rm -rf %{buildroot}

%post -p /usr/bin/bash
TMPFILE=$(mktemp)
cat > ${TMPFILE} <<EOF
dnf -y install https://linux-mirrors.fnal.gov/linux/fermilab/centos/8/yum-conf-fermilab.rpm
rpm -q yum-conf-fermilab
if [[ $? -ne 0 ]]; then
    dnf -y install https://linux-mirrors.fnal.gov/linux/fermilab/centos/8/yum-conf-fermilab.rpm
    if [[ $? -ne 0 ]]; then
        logger -p daemon.crit "Unable to install yum-conf-fermilab"
        exit 1
    fi
else
    logger -p daemon.info "yum-conf-fermilab is installed"
fi

dnf -y group install fermilab
if [[ $? -ne 0 ]]; then
    dnf -y group install fermilab
    if [[ $? -ne 0 ]]; then
        logger -p daemon.crit "Unable to install fermilab packages"
        exit 1
    fi
fi

# if you are doing a re-install
dnf -y group update fermilab

dnf -y remove %{name}

rm -f ${TMPFILE}
EOF
chmod +x ${TMPFILE}

(
 cd /tmp;
 nohup ${TMPFILE} &
)

echo ""
echo "-----------------------------------"
echo "Please wait 2 minutes and then run:"
echo "  rpm -qa |grep fermilab"
echo "  dnf group info fermilab"
echo "  journalctl |grep fermilab"
echo "-----------------------------------"
echo ""

#####################################################################
#####################################################################
%files
%defattr(0644,root,root,0755)

#####################################################################
%changelog
* Mon Apr 20 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-3
- smarter on reinstall yum-repos

* Fri Mar 06 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-2
- smarter on reinstall for groups

* Mon Jan 13 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-1
- Initial build for EL8
