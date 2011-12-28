# Generated automatically from gnutrition.spec.in by configure.
Summary: Nutrition analysis for GNOME
Name: gnutrition
Version: 0.4
Release: 1
Vendor: Edgar Denny (e.denny@ic.ac.uk)
Source: http://download.sourceforge.net/gnutrition/gnutrition-%{version}.tar.gz
URL: http://gnutrition.sourceforge.net/
Copyright: GPL, see file COPYING for details
Group: Applications/Databases
Requires: libglade, pygnome >= 1.0.50, pygtk >= 0.6.3, mysql-server
BuildRoot: /tmp/%name-%{version}

%description
gnutrition is a recipe and food analysis program written in Python, using
GTK+ and GNOME as the user interface, and MySQL as the database server.
It can be used to create and analyze the nutrient content of recipes,
keep track of the nutrient composition of your daily food intake, and
determine the nutrient level of individual foods.

The food nutrient data used in gnutrition is the USDA Nutrient Database[1].
It is in the public domain, and has no copyright.

[1] U.S. Department of Agriculture, Agricultural Research Service. 1999.
    USDA Nutrient Database for Standard Reference, Release 13.
    http://www.nal.usda.gov/fnic/foodcomp

%prep
echo $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT

%setup

%build
./configure --prefix=/usr
make

%install
echo $PWD
make prefix="$RPM_BUILD_ROOT/usr" nopycompile=YES install

%clean
rm -rf $RPM_BUILD_ROOT

%files -f rpm/files.list

%defattr(-,root,root)
%doc INSTALL README COPYING Changelog
