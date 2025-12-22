import csv
import requests
from Bio import SeqIO

def query_uniprot(protein_id):
    """Query UniProt for gene name and UniProt ID."""
    url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        gene_name = data.get("genes", [{}])[0].get("geneName", {}).get("value", "")
        uniprot_id = data.get("primaryAccession", "")
        return gene_name, uniprot_id
    else:
        return "", ""

def process_fasta_to_csv(fasta_files, all_species, output_csv):
    """Process FASTA file and generate a CSV file."""
    with open(output_csv, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(["species", "gene_name", "uniprot_id", "fasta_accession", "notes", "", "sequence identity"])
        for fasta_file, species in zip(fasta_files, all_species):
            with open(fasta_file, "r") as f:
                # Parse FASTA file
                for ind, record in enumerate(SeqIO.parse(f, "fasta")):
                    protein_id = record.id.split("|")[0]  # Extract protein ID
                    gene_name, uniprot_id = query_uniprot(protein_id)
                    fasta_accession = record.id
                    sequence_identity = ""  # Placeholder, as sequence identity is not available

                    # Write row to CSV
                    csv_writer.writerow([species, gene_name, uniprot_id, fasta_accession, f"Files in cyp/{species}_{ind}", "", sequence_identity])

if __name__ == "__main__":
    fasta_files = ["dog_cyp_info.fasta", "mouse_cyp_info.fasta", "rat_cyp_info.fasta", "macaca_fascicularis_cyp_info.fasta", "macaca_mulatta_cyp_info.fasta"]
    species = ['dog', 'mouse', 'rat', 'macaca_fascicularis', 'macaca_mulatta']
    output_csv = "cyp_target_info.csv"
    process_fasta_to_csv(fasta_files, species, output_csv)
    print(f"Processed {fasta_files} and saved to {output_csv}")
