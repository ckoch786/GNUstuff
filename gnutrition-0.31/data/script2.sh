#/bin/sh
# A small script that substitiutes any measures in measure.txt that
# start with "1 " to "".

> $1.mod

sed 's/^1 /^/' < $1 > $1.mod

mv $1.mod $1
