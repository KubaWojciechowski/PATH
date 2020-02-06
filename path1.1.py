import os
import argparse
import textwrap
import subprocess
import pickle
import concurrent.futures
import numpy as np
import pandas as pd
from Bio import SeqIO


def inParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fasta", help = "Input fasta file")
    parser.add_argument("-o", "--output", default='output' , help = "Output directory path")
    args = parser.parse_args()

    #if args.fasta:
    #    parser.error("Wrong operation")
    
    return(args)


def temlateSeq(fasta, template):

    record = SeqIO.parse(fasta, 'fasta')  

    for i in record:
        if template == i.name:
            return(str(i.seq))


def infile(sequence, structure, fasta):
    
    t_seq = temlateSeq(fasta, structure)
    
    print(t_seq)
    f = open('alignment.pir', 'w')

    print(">P1;template", file = f)
    print("Structure:%s:FIRST:A:LAST:L::-1.00:-1.00:" % structure, file = f)
    for i in range(1,12):
        print(textwrap.fill(t_seq, width = 80) + '/', file = f)
    print(textwrap.fill(t_seq, width = 80) + '*\n', file = f)

    print(">P1;sequence", file = f)
    print("sequence:target::::::-1.00:-1.00:", file = f)
    #print(textwrap.fill(t_seq, width = 80), file = f)
    for i in range(1,12):
        print(textwrap.fill(sequence, width = 80) + '/', file = f)
    print(textwrap.fill(sequence, width = 80) + '*\n', file = f)
    
    f.close()


def runScript(script):
    
    p = subprocess.Popen(script, stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()


def model(sequence, output_path):
    dir_path = output_path+'/'+sequence
            
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

        for template in ['class1', 'class2', 'class4', 'class5', 'class6', 'class7', 'class8']:

            models_path = output_path+'/'+sequence+'/'+template
            os.mkdir(models_path)

            template_path = './templates/'+template+'.pdb'
            os.link(template_path, models_path+'/'+template+'.pdb') 
            os.link('scripts/runMod.py', models_path+'/runMod.py') 
                    
            os.chdir(models_path)

            infile(sequence, template, template_fasta)
                    
            runScript("mod9.23 runMod.py")

            os.chdir('../../../')


if __name__ == '__main__':
  
    args = inParser()

    input_path = args.fasta
    output_path = args.output
           
    # Modeling
    os.mkdir(output_path)

    fasta = SeqIO.parse(input_path,'fasta')

    template_fasta = '../../../templates.fasta'

    proteins = []
    prot_names = []
    for record in fasta:
        sequences = str(record.seq)
        if len(sequences) > 6:
            subseqs = [sequences[i:i+6] for i in range(len(sequences)-5)]
            tmp = []
            sequences = [tmp.append(subseqs[i]) for i in range(len(subseqs))]
            sequences = tmp
        else:
            sequences = list(sequences)
        
        prot_names.append(record.id)
        proteins.append(sequences)
        
        #Add multiprocessing

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for s in sequences:
                future = executor.submit(model,s,output_path)
        
    # Scoring
    os.chdir(output_path)
    
    os.link('../scripts/data.sh', 'data.sh') 
    os.link('../scripts/score2.py', 'score2.py')
    
    runScript("bash data.sh > results.csv")
    runScript("python score2.py")
    
    # Analysis
    
    infile = open("../trained_models/waltz/LR", 'rb')
    clf = pickle.load(infile)
    infile.close()

    infile = open("../trained_models/waltz/scaler", 'rb')
    scaler = pickle.load(infile)
    infile.close() 
    
    modeller = pd.read_csv("results.csv")
    rosetta = pd.read_csv("pyrosetta.csv")

    data = pd.merge(modeller, rosetta, on=['seq','class','model'])
    min_e = data.loc[data.groupby('seq')['dope'].idxmin()]

    min_inputs = min_e.values[:,3:]
    inputs = scaler.transform(min_inputs)
    seq = min_e.values[:,0]

    prediction = clf.predict(inputs)

    results = pd.DataFrame(seq, columns=['seq'])
    results['path'] = prediction

    results.to_csv('hexapeptides.csv', index=False)

    pred_d = {seq[i]:prediction[i] for i in range(len(seq))}
    print("Amylodogenic fragments:")

    for p in range(len(prot_names)):
        print(prot_names[p])
        for hexapeptide in proteins[p]:
            if pred_d[hexapeptide] == 1:
                print(hexapeptide)