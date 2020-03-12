## DNA Probe Generation
This repository contains a simple python executable script that allows analyzing a given protein sequence
to extract the most suitable low variability region which could possibly be converted into its cDNA oligonucleotides to provide the highest hybridization binding affinity and thus better accuracy.


### How to use
- After cloning the current repository or downloading a zipped archive of it, enter into the local downloaded repository directory `cd <Repository Directory>`
- convert the current script into an executable script using `chmod a+x probing.py`
- move or copy the executable script into your `/usr/bin` to be OS wide Available, `mv ./probing.py /usr/bin/probing`

- Afterwards, when you have your gene protein product, and you want to generate a cDNA oligonucleotides probe to specifically bind to your gene of interest in a cloning experiment, Please follow the following steps.

`probing --help`

```
usage: probing [-h] [-f FASTA] [-s SIZE] [-t TOP]

optional arguments:
  -h, --help            show this help message and exit
  -f FASTA, --fasta FASTA
                        Protein Fasta File
  -s SIZE, --size SIZE  required probe size/length in bases
  -t TOP, --top TOP     Return Top (N) of probes having the lowest variation
                        in sequence

```

