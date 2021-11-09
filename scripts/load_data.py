#!/usr/bin/python

import pandas as pd
from sqlalchemy import create_engine
import sys
rootDir = "/Users/eloyvallina/Documents/Dropbox/phd/Projects/genomescreening/"
sys.path.append(rootDir + "enaCDS/utils")
sys.path.append(rootDir + "uniprot/september_2021/analysis/utils")
from utils import load_ncbi_data
from data import load_uniprot_data

def load(df):
    engine = create_engine('sqlite:///db.sqlite3', echo=False)
    df.to_sql('Props', con = engine, if_exists = "replace")
    data = engine.execute("SELECT * FROM Props").fetchall()
    return data

def load_double():
    up = load_uniprot_data()
    ncbi = load_ncbi_data()
    up.loc[:, "dataset"] = "uniprot"
    ncbi.loc[:, "dataset"] = "ncbi"
    data = pd.concat([ncbi, up], axis = 0)
    data["Name"] = data.AssemblyID
    data.drop(["Species", "protein_count", "GC_calc", "AssemblyID"], axis = "columns", inplace = True)
    data.reset_index(inplace=True, drop=True)
    data["id"] = data.index
    loaded = load(data)
    print( f"DataFrame length: {data.shape[0]}" )
    print( f"Loaded data length: {len(loaded)}" )



if __name__ == '__main__':
    load_double()
