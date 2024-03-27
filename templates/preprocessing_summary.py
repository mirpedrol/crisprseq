#!/usr/bin/env python

############################
#### Summary of reads preprocessing
#### author: Júlia Mir @mirpedrol
#### Released under the MIT license. See git repository (https://github.com/nf-core/crisprseq) for full license text.
############################

import gzip

import Bio
from Bio import SeqIO

with gzip.open("${raw_reads[0]}", "rt") as handle:
    raw_reads_count = len(list(SeqIO.parse(handle, "fastq")))

if "$assembled_reads" == "":
    assembled_reads_count = 0
else:
    with gzip.open("$assembled_reads", "rt") as handle:
        assembled_reads_count = len(
            list(SeqIO.parse(handle, "fastq"))
        )  # Merged reads R1+R2

with gzip.open("$trimmed_reads", "rt") as handle:
    trimmed_reads_count = len(list(SeqIO.parse(handle, "fastq")))  # Filtered reads

if "$trimmed_adapters" == "":
    adapters_count = 0
    adapters_percentage = "(0.0%)"
else:
    with open("$trimmed_adapters", "r") as handle:
        for line in handle:
            if line.startswith("Reads with adapters"):
                for field in "".join(line.split(",")).split():
                    if field.isdigit():
                        adapters_count = field  # reads with adapters
                    if "%" in field:
                        adapters_percentage = (
                            field  # percentage of reads with adapters: ex. "(100.0%)"
                        )

if "$task.ext.prefix" != "null":
    prefix = "$task.ext.prefix"
else:
    prefix = "$meta.id"

with open(f"{prefix}_preprocessing_summary.csv", "w") as output_file:
    output_file.write("class, count\\n")
    output_file.write(f"raw-reads, {raw_reads_count} (100.0%)\\n")
    output_file.write(
        f"merged-reads, {assembled_reads_count} ({round(assembled_reads_count * 100 / raw_reads_count,1)}%)\\n"
    )
    output_file.write(f"reads-with-adapters, {adapters_count} {adapters_percentage}\\n")
    if "$assembled_reads" == "":
        output_file.write(
            f"quality-filtered-reads, {trimmed_reads_count} ({round(trimmed_reads_count * 100 / raw_reads_count,1)}%)\\n"
        )
    else:
        output_file.write(
            f"quality-filtered-reads, {trimmed_reads_count} ({round(trimmed_reads_count * 100 / assembled_reads_count,1)}%)\\n"
        )


with open("versions.yml", "w") as f:
    f.write('"${task.process}":\\n')
    f.write(f'  biopython: "{Bio.__version__}"\\n')
