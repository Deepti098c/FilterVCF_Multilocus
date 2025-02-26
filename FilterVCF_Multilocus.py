import gzip

def filter_large_vcf(VCFin, VCFout, Chr, POS, override=False):
    """
    Function to extract specific gene/ranges from a large VCF file.
    
    Parameters:
    VCFin (str): Input VCF file (should end with .vcf or .vcf.gz).
    VCFout (str or list): Output file(s) (should end with .vcf or .vcf.gz).
    Chr (str or list): Chromosome(s) to filter.
    POS (list of tuples): List of position ranges to extract (e.g., [(start1, end1), (start2, end2)]).
    override (bool): Whether to overwrite existing files.
    """
    
    if isinstance(VCFout, str):
        VCFout = [VCFout]
    if isinstance(Chr, str):
        Chr = [Chr]
    if isinstance(POS[0], tuple):
        POS = [POS]

    # Check if the output file already exists and whether to overwrite
    for out_file in VCFout:
        if not override and os.path.exists(out_file):
            print(f"Error: {out_file} already exists. Set 'override=True' to overwrite.")
            return

    # Open input VCF file (gzip handled)
    with gzip.open(VCFin, 'rt') if VCFin.endswith('.gz') else open(VCFin, 'r') as infile:
        # Loop over the regions to filter and write to the output VCF files
        for i, (chr_name, pos_range, out_file) in enumerate(zip(Chr, POS, VCFout)):
            with gzip.open(out_file, 'wt') if out_file.endswith('.gz') else open(out_file, 'w') as outfile:
                for line in infile:
                    # Skip header lines
                    if line.startswith('#'):
                        outfile.write(line)
                        continue
                    
                    # Extract chromosome and position from the VCF line
                    fields = line.split('\t')
                    chr_field = fields[0]
                    pos_field = int(fields[1])
                    
                    # Check if the chromosome and position are within the specified range
                    if chr_field == chr_name and pos_range[0] <= pos_field <= pos_range[1]:
                        outfile.write(line)

    print(f"VCF file filtering complete. Output saved to: {', '.join(VCFout)}")

# Example usage
# Extract a single gene/range from large VCF
filter_large_vcf(
    VCFin="Ori.vcf.gz",
    VCFout="filtered.vcf.gz",
    Chr="scaffold_8",
    POS=[19802, 24501],
    override=True
)

# Extract multi genes/ranges from large VCF
filter_large_vcf(
    VCFin="Ori.vcf.gz",
    VCFout=["filtered1.vcf.gz", "filtered2.vcf.gz", "filtered3.vcf.gz"],
    Chr=["scaffold_8", "scaffold_8", "scaffold_7"],
    POS=[[19802, 24501], [27341, 28949], [38469, 40344]],
    override=True
)


