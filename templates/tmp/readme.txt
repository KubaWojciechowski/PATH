Procedure of template preparation:
1. Remove everything except protein from pdb
    - getProt.sh
2. Change chain numeration
    - chnum.py structure.pdb -> structure_tmp.pdb
3. Translate structure according to crystalographical data, to form fibril
    - any automation?
    - make sure that there are 6 layers of peptides
4. Copy to ../programe/templates/ 
