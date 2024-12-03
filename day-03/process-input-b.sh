#/usr/bin/bash

grep -oE '(mul\([0-9]+,[0-9]+\))|(do(n'"'"'t)?\(\))' <input >processed-input-b
