#!/bin/bash

# This script will be run by Vagrant to
# set up everything necessary to use Zipline.

# Because this is intended be a disposable dev VM setup,
# no effort is made to use virtualenv/virtualenvwrapper

# It is assumed that you have "vagrant up"
# from the root of the zipline github checkout.
# This will put the zipline code in the
# /vagrant folder in the system.

VAGRANT_LOG="/home/vagrant/vagrant.log"

# Need to "hold" grub-pc so that it doesn't break
# the rest of the package installs (in case of a "apt-get upgrade")
# (grub-pc will complain that your boot device changed, probably
#  due to something that vagrant did, and break your console)

echo "Obstructing updates to grub-pc..."
apt-mark hold grub-pc 2>&1 >> "$VAGRANT_LOG"

# Run a full apt-get update first.
echo "Updating apt-get caches..."
apt-get -y update 2>&1 >> "$VAGRANT_LOG"

# Install required packages
echo "Installing required packages..."
apt-get -y install python-pip python-dev g++ make libfreetype6-dev libpng-dev libopenblas-dev liblapack-dev gfortran 2>&1 >> "$VAGRANT_LOG"

echo "Installing things Will likes..."
apt-get -y install ipython ipython-doc ipython-notebook python-matplotlib python-numpy python-zmq 2>&1 >> "$VAGRANT_LOG"

# Add ta-lib
echo "Installing ta-lib integration..."
wget http://switch.dl.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz 2>&1 "$VAGRANT_LOG"
tar -xvzf ta-lib-0.4.0-src.tar.gz 2>&1 >> "$VAGRANT_LOG"
cd ta-lib/
./configure --prefix=/usr 2>&1 >> "$VAGRANT_LOG"
make 2>&1 >> "$VAGRANT_LOG"
sudo make install 2>&1 >> "$VAGRANT_LOG"
cd ../

# Add Zipline python dependencies
echo "Installing python package dependencies..."
/vagrant/etc/ordered_pip.sh /vagrant/etc/requirements.txt 2>&1 >> "$VAGRANT_LOG"
# Add scipy next (if it's not done now, breaks installing of statsmodels for some reason ??)
echo "Installing scipy..."
pip install scipy==0.12.0 2>&1 >> "$VAGRANT_LOG"
echo "Installing zipline dev python dependencies..."
pip install -r /vagrant/etc/requirements_dev.txt 2>&1 >> "$VAGRANT_LOG"

echo "Start an iPython notebook server process..."
mkdir -p /home/vagrant/.ipython/profile_nbserver
cat > /home/vagrant/.ipython/profile_nbserver/ipython_notebook_config.py <<EOF
c = get_config()
c.IPKernelApp.pylab = 'inline'
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
# Password for this iPython notebook server is "Barnstable" (a town on Cape Cod)
c.NotebookApp.password = 'sha1:b9449d212ec8:40df17fae8e4e8d4da97c56e7fb8aecca1edfa9e'
EOF
chown -R vagrant:vagrant /home/vagrant

cat > /etc/init.d/ipython <<EOF
#!/bin/sh
echo "IPython Notebook \$1"
case \$1 in
    stop)
        kill -9 \$(ps ax | grep ipython | cut -c -6)
        ;;
    start)
        sudo -u vagrant ipython notebook --profile=nbserver &
        ;;
    restart)
        kill -9 \$(ps ax | grep ipython | cut -c -6)
        sleep 5
        sudo -u vagrant ipython notebook --profile=nbserver &
        ;;
    *)
        ;;
esac
EOF
chmod 755 /etc/init.d/ipython
(cd /etc/rc2.d; ln -s ../init.d/ipython S80ipython)
(cd /etc/rc3.d; ln -s ../init.d/ipython S80ipython)
(cd /etc/rc4.d; ln -s ../init.d/ipython S80ipython)
(cd /etc/rc5.d; ln -s ../init.d/ipython S80ipython)

echo "Finished!"
