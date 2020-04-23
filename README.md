# liftCNV
Wrapper for CrossMap to Lift Over CNVs between human genome builds.  CNV file must have first column in format chr:start-end (PennCNV format).

**Usage**
`python3 liftOverCNV.py [chain_file] [cnv_file] [output_file]`


### Installation Requirements
**Download Chain files**
Add any additiona chain file download locations to the file: chain_files/chain_file_downloads.txt.  The links to most common chain files are already included.
 
Run command to download the chain files.  
`wget -P chain_files/ -i chain_files/chain_file_downloads.txt`

**Example**
Run the following example which should now work:
`python3 liftOverCNV.py chain_files/hg19ToHg38.over.chain.gz test_files/CNVs_hg18.txt "CNVs_hg38_lifted.txt"`

