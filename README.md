# PF Accsessories
Informal phylofisher related scripts
  
### prep_new_db.py  
```
$ prep_new_db.py -h
usage: prep_new_db.py [-h] -t TAXA_LIST -d MASTER_DB -o OUT_DIR

Prepares files for input for Phylofisher's build_database.py for the creation of a custom database from a subset of taxa in a larger Phylofisher database

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -t TAXA_LIST, --taxa_list TAXA_LIST
                        List of taxa as unique IDs to include in new database
  -d MASTER_DB, --master_db MASTER_DB
                        Path to master phylofisher database
  -o OUT_DIR, --out_dir OUT_DIR
                        Path to location where output directory for new
                        database files will be made
                        
  
optional arguments:
  -z {yes,no}, --compress {yes,no}
                        Create tar.gz compressed output instead of
                        uncompressed
```
