import sys
import os
import glob
from Bio import SeqIO
import shutil
import argparse
import tarfile

def select_taxa(taxalist):
## Open Taxa list for new DB
	infile = open(taxalist)
	lines = infile.read()
	infile.close

	lines = lines.split('\n')
	lines=[line for line in lines if line.strip() !=""] 

	return lines

#Make output directories
def outputs(masterout):
	outdir = masterout + "/new_database"
	orthooutdir = outdir + "/orthologs"
	paraoutdir = outdir + "/paralogs"
	protoutdir = outdir + "/proteomes"
	try:
		os.mkdir(masterout)
		print(masterout + " created")
	except OSError as error:
		print(masterout + " already exists")
		pass
	try:
		os.mkdir(outdir)
		print(outdir + " created")
	except OSError as error:
		print(outdir + " already exists")
		pass
	try:
		os.mkdir(orthooutdir)
		print(orthooutdir + " created")
	except OSError as error:
		print(orthooutdir + " already exists")
		pass
	try:
		os.mkdir(paraoutdir)
		print(paraoutdir + " created")
	except OSError as error:
		print(paraoutdir + " already exists")
		pass
	try:
		os.mkdir(protoutdir)
		print(protoutdir + " created")
	except OSError as error:
		print(protoutdir + " already exists")
		pass
		
	return outdir, orthooutdir, paraoutdir, protoutdir

## Make new ortholog fastas from selected taxa
def make_new_orthos(masterdbpath, orthooutdir, lines):
	orthopath = masterdbpath + "/orthologs/"
	orthofastas = (glob.glob(orthopath +"/*.fas"))
	for i in orthofastas:
		keep = []
		fasta = SeqIO.parse(open(i), 'fasta')
		fname = i.split('/')[-1]
		print(fname)
		with open(orthooutdir + "/" + fname, "w") as outfasta:
			for record in fasta:
				for line in lines:
					if line == record.id:
						keep.append(record)
						SeqIO.write(record, outfasta, "fasta")
					else:
						pass

## Make new paralog fastas from selected taxa
def make_new_paras(masterdbpath, paraoutdir, lines):
	parapath = masterdbpath + "/paralogs/"
	parafastas = (glob.glob(parapath +"/*.fas"))
	for i in parafastas:
		keep = []
		fasta = SeqIO.parse(open(i), 'fasta')
		fname = i.split('/')[-1]
		print(fname)
		with open(paraoutdir + "/" + fname, "w") as outfasta:
			for record in fasta:
				for line in lines:
					if line == record.id:
						keep.append(record)
						SeqIO.write(record, outfasta, "fasta")
					else:
						pass

## Copy proteome files to new directory
def make_new_prots(masterdbpath, protoutdir, lines):
	protpath = masterdbpath + "/proteomes/"
	proteomes = (glob.glob(protpath +"/*.gz"))
	for line in lines:
		shutil.copy(protpath + line + ".faa.tar.gz", protoutdir, follow_symlinks=True)
		print(protpath + line + ".faa.tar.gz")

## Make new metadata file
def make_metadata(masterdbpath, outdir, lines):
	metain = open(masterdbpath + "/metadata.tsv")
	mlines = metain.read()
	metain.close
	
	mlines = mlines.split('\n')
	mlines=[line for line in mlines if line.strip() !=""]
	newmd = ['Unique ID\tLong Name\tHigher Taxonomy\tLower Taxonomy\tData Type\tSource']
	for mline in mlines:
		uniqid = mline.split('\t')[0]
		for line in lines:
			if line == uniqid:
				newmd.append(mline)
	with open(outdir + '/metadata.tsv', 'w') as metaout:
		for line in newmd:
			metaout.write(line + '\n')
	metaout.close

#Optional Compress Output
def compress(masterout):
	if args.compress == 'yes':
		tarout = masterout + ".tar.gz"
		tar = tarfile.open(tarout, "w:gz")
		tar.add(masterout)
		tar.close()
		shutil.rmtree(masterout)
	else:
		pass	
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Prepares files for new database creation from subset of main database taxa')
	required = parser.add_argument_group('required arguments')
	optional = parser.add_argument_group('optional arguments')
	required.add_argument('-t', '--taxa_list', type = str, help = 'List of taxa as unique IDs to include in new database', required=True)
	required.add_argument('-d', '--master_db', type = str, help = 'Path to master phylofisher database', required = True)
	required.add_argument('-o', '--out_dir', type = str, help = 'Path to location where output directory for new database files will be made', required = True)
	optional.add_argument('-z', '--compress', type = str, help = 'Create tar.gz compressed output instead of uncompressed', choices = ['yes', 'no'], default= 'no')

	args=parser.parse_args()

	taxalist = args.taxa_list
	masterdbpath = args.master_db
	masterout = args.out_dir

	lines = select_taxa(taxalist)
	outdir, orthooutdir, paraoutdir, protoutdir = outputs(masterout)
	make_new_orthos(masterdbpath, orthooutdir, lines)
	make_new_paras(masterdbpath, paraoutdir, lines)
	make_new_prots(masterdbpath, protoutdir, lines)
	make_metadata(masterdbpath, outdir, lines)
	compress(masterout)
