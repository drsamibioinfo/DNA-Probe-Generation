#!/usr/bin/env python
from __future__ import print_function
import os, sys
import argparse
from __builtin__ import property

from Bio.Data.CodonTable import standard_dna_table as dna


class Probe(object):
    def __init__(self, seq="", mismatch=0):
        self.seq = seq
        self.mismatch = mismatch

    @property
    def dna(self):
        current = [dna.back_table[a] for a in self.seq]
        return "".join(current)

    @property
    def affinity(self):
        l = len(self.dna)
        mb = l - self.mismatch
        return (mb / float(l)) * 100.0

    def __str__(self):
        return """
        AA Sequence : {0}
        DNA Sequence : {1}
        Hybridization Affinity : {2:2.2f}%
        Variable bases # : {3}
        """.format(self.seq, self.dna,self.affinity,self.mismatch)


def prepare_codon_table():
    codons = {}
    for k, v in dna.forward_table.items():
        if codons.has_key(v):
            codes = codons[v]
            codes.append(k)
        else:
            codons[v] = [k]

    return codons


def read_file(input):
    with open(input, mode="r") as file:
        lines = file.readlines()
        lines = lines[1:]
        return "".join(lines)


def get_aa_variation(codons, aa):
    # ['AAA','BBB','ABB']
    codes = codons.get(aa,None)
    if not codes:
        return 0
    variation = 0
    zipped_ = zip(*codes)
    for elem in zipped_:
        if not all(el == elem[0] for el in elem):
            variation += 1

    return variation


def get_probes(contents, size, top):
    l = len(contents)
    offset = 0
    codons = prepare_codon_table()
    memory = []
    while l - offset >= size:
        probe = contents[offset:offset + size]
        variation = sum([get_aa_variation(codons, aa) for aa in probe])
        memory.append(Probe(seq=probe, mismatch=variation))
        offset += 1
    sorted_list = sorted(memory, key=lambda x: x.mismatch)
    if top > len(sorted_list):
        top = 1
    return sorted_list[0:top]


def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("-f", "--fasta", help="Protein Fasta File")
    arg.add_argument("-s", "--size", help="required probe size/length in bases")
    arg.add_argument("-t", "--top", default=1, help="Return Top (N) of probes having the lowest variation in sequence")

    if len(sys.argv) <= 1:
        arg.print_help()
        return
    arguments = arg.parse_args()

    if not arguments.fasta:
        arg.error(
            "Protein Fasta File is required, Please use -f or --fasta switch to provide the input protein sequence in fasta format.")
        return
    if not arguments.size:
        arg.error(
            "Probe size/length is required, Please provide the length of probe in bases using -s or --size switch")
        return

    contents = read_file(arguments.fasta)
    contents = contents.replace('\n','').replace('\r','')
    probes = get_probes(contents, size=int(arguments.size)/3, top=int(arguments.top))

    if len(probes) <= 0:
        arg.error("Required probe can't be found from protein input fasta file")
        return

    for probe in probes:
        print(probe)



if __name__ == '__main__':
    main()
