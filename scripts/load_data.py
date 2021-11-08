#!/usr/bin/python

from sqlalchemy import create_engine
import sys
rootDir = "/Users/eloyvallina/Documents/Dropbox/phd/Projects/genomescreening/"
sys.path.append(rootDir + "enaCDS/utils")
from utils import load_ncbi_data

def load(df):
    engine = create_engine('sqlite:///db.sqlite3', echo=False)
    df.to_sql('Props', con = engine, if_exists = "replace")
    data = engine.execute("SELECT * FROM Props").fetchall()
    return data


if __name__ == '__main__':
    ncbiAll = load_ncbi_data()
    ncbiAll["Name"] = ncbiAll.AssemblyID
    ncbiAll.drop(["species", "AssemblyID"], axis='columns', inplace=True)
    data = load(ncbiAll)
    print( f"DataFrame length: {ncbiAll.shape[0]}" )
    print( f"Loaded data length: {len(data)}" )
