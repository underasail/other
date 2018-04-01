#! /bin/bash

# read -p 'Directory for parallel install (suggested: "~"): ' pdir
# pdir=$pdir"/parallel"
echo '#########################'
echo '# Installing "bcftools" #'
echo '#########################'
mkdir ~/bcftools
mkdir ~/bcftools/src # creates the installation directories within the home directory
cd ~/bcftools/src
wget -q https://github.com/samtools/bcftools/releases/download/1.7/bcftools-1.7.tar.bz2
# downloads the parallel source file
echo '"bcftools" source file downloaded with wget'
tar -jxf bcftools-1.7.tar.bz2 -C ~/bcftools/ 
# unzips(bz2) and expands parallel source file
echo '"bcftools" source file unziped and expanded with tar'
cd ~/bcftools/bcftools-1.7/
./configure --prefix=$(echo ~/bcftools/) 
# configures parallel installation in the created directory
make
make install
echo '"bcftools" Install Completed'
echo '"bcftools" configured in: ~/bcftools/'
echo 'Source file located in: ~/bcftools/src'
echo 'export PATH=$PATH:$HOME/bcftools/bin' >> ~/.bashrc
echo ''
echo 'You should now "exec bash" to implement new path with bcftools included.'
