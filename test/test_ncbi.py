"""
Tests for fred/src/ncbi_search.py - search taxons, genes and genomes with NCBI Datasets
"""
import sys
import os
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import fred.src.ncbi_datasets as ncbi_search


# ---------------------------------------------------------------------------
# Minimal taxonomy data for tests
# ---------------------------------------------------------------------------

COW_TAXON = {"common_name":"cow", "scientific_name":"Bos taurus", "tax_id":"9913"}
ECOLI_TAXON = {"common_name":"ecoli", "scientific_name":"Escherichia coli K-12", "tax_id":"83333"}
BadTaxID = "12"

# ---------------------------------------------------------------------------
# get_taxonomy — unit tests
# ---------------------------------------------------------------------------

def test_common_name_match():
    try:
        taxonomy = ncbi_search.get_taxonomy(COW_TAXON["common_name"])
    except Exception as e:
        result = e.stderr
    taxon_id = str(taxonomy["tax_id"])
    organism_name = taxonomy["classification"]["species"]["name"]
    result = organism_name+", "+taxon_id
    tax_str = COW_TAXON["scientific_name"]+", "+COW_TAXON["tax_id"]
    assert (result == tax_str) is True
    
def test_scientific_name_match():
    try:
        taxonomy = ncbi_search.get_taxonomy(ECOLI_TAXON["scientific_name"])
    except Exception as e:
        result = e.stderr
    taxon_id = str(taxonomy["tax_id"])
    organism_name = taxonomy["classification"]["species"]["name"]
    result = organism_name+", "+taxon_id
    tax_str = ECOLI_TAXON["scientific_name"]+", "+ECOLI_TAXON["tax_id"]
    assert (result == tax_str) is True

def test_name_ambiguous():
    try:
        result = ncbi_search.get_taxonomy(ECOLI_TAXON["common_name"])
    except Exception as e:
        result = e.stderr
    assert ("The taxonomy name '"+ECOLI_TAXON['common_name']+"' is not exact." in result) is True
    
def test_name_no_match():
    try:
        result = ncbi_search.get_taxonomy("")
    except Exception as e:
        result = e.stderr
    assert ("The taxonomy name '' is not recognized." in result) is True
    
# ---------------------------------------------------------------------------
# get_genes — unit tests
# ---------------------------------------------------------------------------

def test_genes_taxon_match():
    try:
        result = ncbi_search.get_genes_ensemble(COW_TAXON["tax_id"])
    except Exception as e:
        result = e.stderr
    assert ("NA NA" not in result["whitelist"]) is True
    
def test_genes_taxon_no_match(): #TODO: revisar error y función
    try:
        result = ncbi_search.get_genes_ensemble(BadTaxID)
    except Exception as e:
        result = e.stderr
    assert ("NA NA" in result["whitelist"]) is True
    
# ---------------------------------------------------------------------------
# get_genomes — unit tests
# ---------------------------------------------------------------------------

def test_refgenome_taxon_match():
    try:
        result = ncbi_search.get_genomes(COW_TAXON["tax_id"])
    except Exception as e:
        result = e.stderr
    assert ("bosTau9" in result[COW_TAXON["scientific_name"]]) is True
    
def test_refgenome_taxon_no_match():
    try:
        result = ncbi_search.get_genomes(BadTaxID)
    except Exception as e:
        result = e.stderr
    assert (result == {}) is True
    