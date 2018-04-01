#! /bin/bash

#BSUB -J %J
#BSUB -e /nethome/mct30/err/%J.err
#BSUB -o /nethome/mct30/out/%J.out
#BSUB -n 1
#BSUB -q general
#BSUB -W 24:00
#BSUB -B
#BSUB -N
#BSUB -u mct30@miami.edu
#
# Job title, error output, standard output, number of cores,
# queue, run time limit, send email when jobs begins, 
# send email with stats when job finished, email,
# default RAM per core is 1500MB