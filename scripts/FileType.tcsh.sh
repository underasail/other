#!/bin/tcsh

#----Ask the user for the file extension if none provided
if ($#argv < 1) then
    echo -n "What file type : "
    set FileType=$<
else
    set FileType = $1
endif

echo "Looking through $FileType files"

#----Look in each file of that type
foreach File (*.$FileType)
    echo -n "Searching $File ... "
#----Count the number of lines containing "int"
    set IntCount = `grep -c "int" $File`
    echo "It has $IntCount lines containing int”
end
