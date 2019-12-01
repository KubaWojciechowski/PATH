# Parse log files
# iterate over sequences
echo "seq,class,model,molpdf,dope,ga341"
for seq in */;
do
    #echo '>'$seq
    cd $seq
    #iterate over classes    
    for class in */;
    do
        #echo $class
        cd $class
        energy=`awk '/^sequence/{print substr($1, length($1)-6, 3)+0 "," $2 "," $3 "," $4}' runMod.log`
        
        for i in $energy;
        do 
             echo ${seq::-1}','${class:5:-1}','$i
        done
        cd ../
    done

    cd ../
done
