#! /bin/bash

# could log date and status of each pacman and yaourt update

## date >> ~/Documents/update_log.txt

echo "pacman: " ##  >> ~/Documents/update_log.txt
sudo pacman -Syu ##  >> ~/Documents/update_log.txt
echo "yaourt: " ##  >> ~/Documents/update_log.txt
yaourt -Syu --aur ## --devel ## >> ~/Documents/update_log.txt

## echo "Logged"
