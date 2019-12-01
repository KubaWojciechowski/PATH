for INP in *.tga
do
newname=`basename $INP .tga`
convert $INP $newname.png
done
echo ” process ended, please check your graphical files”
