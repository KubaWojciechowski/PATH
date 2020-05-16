# PATH
PATH - Prediction of Amyloidogenicity by Threading and Machine Learning
## Requirements
PATH is a computational pipeline for prediction of amyloidogenic fragments in proteins. It uses poular molecular modeling software, in oreder to use it you need to install:
* PyRosseta
* Modeller (tested with 9.23 but should work with other versions too. If you use it with other version open path1.1.py in text editor of choice and change version in line 81)
* Python3
As well as some Python packages:
* Numpy
* Pandas
* Biopython
## Input
PATH takes as an input protein sequences in fasta format.
## Running PATH
You can run PATH as any other Python script by typeing:
`python path1.1py -f <input_file> -o <output_directory>`
## PATH output
As PATH perform structural modeling which is computationaly expensive it might take a while to get your results. PATH output contains files containing energies and classification as well as directories for each protein fragment from input. Each of them have directories for molecular models for each of possible structural classes.
## How to cite?
If you use PATH in your research, please cite:
Wojciechowski, J.W., Kotulska, M. PATH - Prediction of Amyloidogenicity by Threading and Machine Learning. Sci Rep 10, 7721 (2020). https://doi.org/10.1038/s41598-020-64270-3

