#!/bin/tcsh
#------------------------------------------------------------------------------
echo -n "What is the limit on your rabbit population: "
@ RabbitLimit = $<

set Fibonaccis = (0 1)
@ Epochs = 2
while ($Fibonaccis[$Epochs] < $RabbitLimit) 
    @ Epochs++
    @ Epochs1 = $Epochs - 1
    @ Epochs2 = $Epochs - 2
    @ NextFibonacci = $Fibonaccis[$Epochs1] + $Fibonaccis[$Epochs2]
    set Fibonaccis = ($Fibonaccis $NextFibonacci)
end

echo "After $Epochs epochs there are $Fibonaccis[$Epochs] rabbits"

echo -n "Enter the first epoch of interest: "
@ First = $<
echo -n "Enter the last epoch of interest: "
@ Last = $<
echo "Rabbit populations were ..."
echo "   $Fibonaccis[$First-$Last]"
#---------------------------------------------------------------------------
