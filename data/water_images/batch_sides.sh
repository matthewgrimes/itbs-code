#!/bin/bash
command1=`convert $1 -region 40x50 -fuzz 10% -fill 'rgb(58,19,78)' -opaque 'rgb(231,77,189)' +adjoin test.png`
print $command1
