#!/bin/tcsh

(ls -l | wc) &
ls -l ; ls –a
set MyLS = `ls`
echo Listing is $MyLS
