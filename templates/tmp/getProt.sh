name=$1
sed -i '/TER   /d' ./$name
sed -i '/MODEL /d' ./$name
sed -i '/ENDMDL/d' ./$name
vmd $name -dispenv text -e getProt.tcl
