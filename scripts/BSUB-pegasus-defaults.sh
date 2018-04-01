#! /bin/bash

bsub -J mct30_quick_job -e /nethome/mct30/err/%J.err -o /nethome/mct30/out/%J.out \
-n 1 -q general -W 24:00 -B -N -u mct30@miami.edu \
$1

# allows user to run a script as the second argument for 
# ~/scripts/BSUB-pegasus-defaults.sh
# uses a 24 hr wall time on one core with 1500MB RAM and %J as the jobname