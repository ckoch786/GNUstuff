#/bin/sh
# 1. substitute any DOS type control characters with "\n"
# 2. remove any "~"
#
# The field separator is kept as "^".
#
# This puts the files in the correct state for the database.

> $1.mod1

tr -s "[\015\032]" "\n" < $1 | tr -d "~" >> $1.mod

mv $1.mod $1
