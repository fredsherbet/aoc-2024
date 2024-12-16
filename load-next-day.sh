mkdir "day-$(date '+%d')"
cd "day-$(date '+%d')"
pbpaste >input
FF="day-$(date '+%d')-a.py"
cat >$FF <<EOF


with open('input') as input:
EOF
vim $FF
