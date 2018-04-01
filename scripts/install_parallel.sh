#! /bin/bash

# read -p 'Directory for parallel install (suggested: "~"): ' pdir
# pdir=$pdir"/parallel"
echo '#########################'
echo '# Installing "parallel" #'
echo '#########################'
mkdir ~/parallel
mkdir ~/parallel/src # creates the installation directories within the home directory
cd ~/parallel/src
wget -q http://ftp.gnu.org/gnu/parallel/parallel-20180322.tar.bz2
# downloads the parallel source file
echo '"parallel" source file downloaded with wget'
tar -jxf parallel-20180322.tar.bz2 -C ~/parallel/ 
# unzips(bz2) and expands parallel source file
echo '"parallel" source file unziped and expanded with tar'
cd ~/parallel/parallel-20180322/
./configure --prefix=$(echo ~/parallel/) 
# configures parallel installation in the created directory
make -s
make -s install
echo '"parallel" Install Completed'
echo '"parallel" configured in: ~/parallel/'
echo 'Source file located in: ~/parallel/src'
echo 'export PATH=$PATH:$HOME/parallel/bin/' >> ~/.bashrc
echo ''
echo 'You should now "exec bash" to implement new path with parallel included.'
