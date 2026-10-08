import subprocess
from subprocess import run
from collections import Counter
import json
import re 
import sys
import os

def get_genomes(tax_id):
    genome_dict = {}
    limit = 10000

    g_list=[]

    try:
        f=run("datasets summary genome taxon "+str(tax_id)+" --limit "+str(limit)+" --assembly-source RefSeq --assembly-version all",capture_output=True, shell=True, text=True)
        if f.returncode == 1:
            raise subprocess.CalledProcessError(1,cmd='datasets',stderr=f.stderr)
    except subprocess.CalledProcessError as e:
        raise e
    
    data = json.loads(f.stdout)
    for r in data["reports"]:
        organism_name = r["organism"]["organism_name"]
        s=r["assembly_info"].get("synonym") if r["assembly_info"].get("synonym") != None else None
        if s!=None:
            g_list.append(s)
        else:
            if r["organism"].get("infraspecific_names")!=None and r["organism"]["infraspecific_names"].get("isolate")!= None and r["organism"]["infraspecific_names"].get("isolate")!="None":
                g_list.append(r["organism"]["infraspecific_names"].get("isolate"))

    g_list = list(set(g_list))
    g_list.sort()

    if g_list:
        genome_dict[organism_name] = g_list

    return genome_dict

def get_taxonomy(taxon_name):

    try:
        f=run('datasets summary taxonomy taxon "'+str(taxon_name)+'"',capture_output=True, shell=True, text=True)
        if f.returncode == 1:
            raise subprocess.CalledProcessError(1,cmd='datasets',stderr=f.stderr)
        elif f.returncode == 127:
            print(f"The NCBI Datasets command-line tools could not be found in the PATH, please make sure they are installed in the working environment.\n")
            raise ValueError
    except subprocess.CalledProcessError as e:
        raise e
    
    data = json.loads(f.stdout)
    taxon = data["reports"][0]["taxonomy"]
    return taxon

def get_genes_ensemble(tax_id):

    names = []
    ensembles = []
    limitGenome = 200
    limit = 70000

    try:
        # TODO: Cambiarlo a summary taxonomy (sin limite) y coger report > taxonomy > children para sacar los genes
        # f=run("datasets summary genome taxon "+tax_id[0]+" --limit "+str(limitGenome)+" --assembly-source RefSeq --assembly-version all",capture_output=True, shell=True, text=True)
        f=run("datasets summary taxonomy taxon "+str(tax_id),capture_output=True, shell=True, text=True)
        if f.returncode == 1:
            raise subprocess.CalledProcessError(1,cmd='datasets',stderr=f.stderr)
    except subprocess.CalledProcessError as e:
        raise e
    
    data = json.loads(f.stdout)
    strains = [str(tax_id)]
    for r in data["reports"]:
        # strains.append(r["organism"]["tax_id"])
        strains.extend(r["taxonomy"].get("children",[]))

    strains = list(set(strains))
    for strain in strains:
        try:
            g=run("datasets summary gene taxon "+str(strain)+" --limit "+str(limit),capture_output=True, shell=True, text=True)
            if g.returncode == 1:
                continue
        except subprocess.CalledProcessError as e:
            raise e
        
        genes = json.loads(g.stdout)
        for gr in genes["reports"]:
            s0=gr['gene'].get('symbol')
            s1=gr['gene'].get('ensembl_gene_ids')[0] if gr['gene'].get('ensembl_gene_ids') != None else gr['gene'].get('locus_tag')
            s=[s0,s1]
            s[1] = s[0] if s[1] == None else s[1]
            s[0] = 'NA' if s[0] == None or s[0]==s[1] else s[0]
            if s[1]!=None:
                names.append(s[0])
                ensembles.append(s[0]+" "+s[1])

    counts = Counter(names)
    output = [value for value, count in counts.items() if count > 1]
    names = list(set(output))
    if ensembles == []:
        whitelist = {'whitelist_type':'plain','headers': 'gene_name ensembl_id', 'double': ['NA'], 'whitelist':['NA NA']}
    else:
        whitelist = {'whitelist_type':'plain','headers': 'gene_name ensembl_id', 'double': names, 'whitelist':ensembles}
    return whitelist

def ncbi_search(term, tax_id=None):
    if term == "organism":
        try:
            print(f"---\nWrite either the species name (Bos taurus) or common name (cow):\n")
            raw = input()
            taxonomy = get_taxonomy(raw)
            if taxonomy["rank"] not in ["SPECIES","STRAIN","SUBSPECIES"]:
                raise subprocess.CalledProcessError(1,cmd='datasets',stderr='The input must be at the SPECIES rank or below.')
            taxon_id = str(taxonomy["tax_id"])
            organism_name = taxonomy["classification"]["species"]["name"]
            value = organism_name+", "+taxon_id
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print(f"Multiple taxons match the taxon provided.\n")
            value=ncbi_search(term)
        print(f"Species found: {value}\n")
        return value
    elif term == "genes":
        whitelist = {'whitelist_type':'plain','headers': 'gene_name ensembl_id', 'double': ['NA'], 'whitelist':['NA NA']}
        try:
            print(f"---\nThe list of possible genes is being retrieved from the NCBI dataset.\n---\n")
            whitelist = get_genes_ensemble(tax_id)
        except subprocess.CalledProcessError as e:
            print(e.stderr)
        return whitelist
    elif term == "reference_genome":
        try:
            print(f"---\nThe list of reference genomes is being retrieved from the NCBI dataset.\n---\n")
            whitelist = get_genomes(tax_id)
        except subprocess.CalledProcessError as e:
            print(e.stderr)
        return whitelist
    else:
        return ""