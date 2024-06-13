"""
Name: <Mohammad Abbas>
Section: <A>
"""

def is_stop(codon):
    """
    Checks if a string is a stop codon
    
    Args:
        codon: string of 3 characters
    Returns:
        True if is stop codon, False if not
    """
    string_codon = str(codon)
    Valid_Codon = ['TAA','TAG','TGA']

    while string_codon in Valid_Codon:
        return True
    else:
        return False

def orf_sequence(DNA):
    """
    Finds and returns ORF from a string that starts with a
    start codon without stop codon
    
    Args:
        DNA: string
    Returns:
        ORF from start codon to just before the stop codon
    """
    string_dna = str(DNA)
    position = 0
    for i in range(0, len(string_dna),3):
        position += 3
        if is_stop(string_dna[i:i+3]) == True:
            return ((string_dna[0:position-3]))
    return (string_dna)

def find_orfs(DNA):
    """
    Finds and returns ORFs from DNA of codons of 3 bases
    
    Args:
        DNA: String of bases
    Returns:
        list of ORFs from start codon until stop codon
    """   
    start_codon = 'ATG'
    orfs = []
    i = 0
    while i < len(DNA):
        codon = DNA[i:i+3]
        if len(codon) == 3 and codon in start_codon:
            orf = orf_sequence(DNA[i:])
            orfs.append(orf)
            i += len(orf)+3
        else:
            i += 3
    return orfs

def reverse_complement(DNA):
    """
    Reverse a DNA string by switching the bases with their
    complemetary ones
    
    Args:
        DNA: String of bases
    Returns:
        Reversed DNA with switched bases
    """    
    strand_length = len(DNA)
    reverse_strand = DNA[strand_length::-1] 
    complement_bases = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    list_strand = list(reverse_strand)
    list_strand = [complement_bases[i] for i in list_strand] 
    final_strand = ''.join(list_strand)
    return final_strand

def gene_finder(DNA):
    """
    Finds and returns specific genes from a DNA sequence
    using potential frames and reversed ones
    
    Args:
        DNA: String of bases
    Returns:
        List with all the potential genes in every frame,
        including reversed ones
    """    
    orf_list=[]
    for i in range (3):
     DNA1=DNA[i:]
     if (find_orfs(DNA1))!=[]:
      orf_list+=find_orfs(DNA1)
      
    reverse_DNA=reverse_complement(DNA)
    for i in range(3):
        reverse_DNA1=reverse_DNA[i:]
        if (find_orfs(reverse_DNA1))!=[]:
         orf_list+=find_orfs(reverse_DNA1)
    return orf_list

def read_fasta(filename):
    """
    Read a single DNA sequence from a FASTA-formatted file
    
    For example, to read the sequence from a file named "X73525.fasta.txt"
    >>> sequence = read_fasta("X73525.fasta.txt")
    
    Args:
        filename: Filename as a string
        
    Returns: Upper case DNA sequence as a string
    """
    with open(filename, "r") as file:
        # Read (and ignore) header line
        header = file.readline()
        # Read sequence lines
        sequence = ""
        for line in file:
            sequence += line.strip()
        return sequence.upper()


def filter_orfs(orfs, min_length):
    """
    Filter ORFs to have a minimum length
    
    Args:
        orfs: List of candidate ORF sequences
        min_length: Minimum length for an ORF
    
    Returns:
        A new list containing only ORF strings longer than min_length bases
    """
    filtered_orfs = []
    for orf in orfs:
        if len(orf) > min_length:
            filtered_orfs.append(orf)
    return filtered_orfs


def write_fasta(filename, orfs):
    """
    Write list of ORFs to a FASTA formatted text file.
    
    For example, to save a list of orfs assigned to the variable my_orfs to a
    file named "genes.txt"
    >>> write_fasta("genes.txt", my_orfs)
    
    Args:
        filename: Filename as a string. Note that any existing file with this name
            will be overwritten.
        orfs: List of ORF sequences to write to the file
    """
    with open(filename, "w") as file:
        for i in range(len(orfs)):
            # A FASTA entry is a header line that begins with a '>', and then the sequence on the next line(s)
            print(">seq" + str(i), file=file)
            print(orfs[i], file=file)

           
if __name__ == "__main__":
    sequence = read_fasta("X73525.fasta.txt") #(you could change the data file for yours)
    orfs = gene_finder(sequence)
    filtered_orfs = filter_orfs(orfs, 690)
    write_fasta("genes.txt", filtered_orfs)
