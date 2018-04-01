#! /bin/bash

touch $1
cat /nethome/mct30/scripts/BSUB-pegasus-template.sh >> $1
emacs $1
