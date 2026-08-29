# The architecture of the ATFS-1 transcriptional output

A reanalysis of published *C. elegans* data asking whether the mitochondrial unfolded
protein response (UPR^mt), which is triggered by import failure rather than by unfolded
protein, actually produces a folding-centric transcriptional output.

The work is computational only. Every input is public, every intermediate is a small
table, and the whole analysis is reproducible from the files and accessions below.

## Setup

macOS (Apple Silicon), conda environment `atfs1`, Python 3.11 (see `environment.yml`
for exact pinned versions).

```
conda env create -f environment.yml
conda activate atfs1
jupyter lab
```

Notebooks reset to the project root on their first cell and run independently of one
another — order doesn't matter, and none depends on another having been run first.
Nothing reaches the network at runtime. The only external tool is `ucsc-liftover`,
already run once for the ce6→ce11 peak conversion; its output is committed, so
nothing needs re-lifting.

`scripts/analysis_c.ipynb` needs the WS285 GFF3 annotation, and `analysis_a.ipynb`
needs `go-basic.obo`; both are gitignored for size and re-downloadable from the
sources in the data table below.

## Reproducing the analyses

| Notebook | What it produces |
|---|---|
| `scripts/census_build.ipynb` | Rebuilds the chaperone/protease census from Pfam domains and asserts it still matches the frozen CSV |
| `scripts/binding.ipynb` | Gate 0/1 — binding reconciliation, operon status, the *hsp-6* question |
| `scripts/census.ipynb` | Analysis B — chaperone/protease census vs. the regulon (2 of 61) |
| `scripts/analysis_c.ipynb` | Analysis C — operon-aware peak assignment, occupancy vs. output |
| `scripts/analysis_a.ipynb` | Analysis A — GO enrichment, expressed background, filtering-series walk |
| `scripts/analysis_d.ipynb` | Analysis D — robustness checks and the Gate 2 evidence summary |
| `scripts/wu2018_verification.ipynb` | Reconstruction of Wu 2018's published 1,704 / 529 counts |
| `scripts/table_s2.ipynb` | Functional category for all 61 regulon genes |
| `scripts/table_1.ipynb` | Table 1 — the five census-relevant genes, three binding sources kept separate |
| `scripts/figure_1.ipynb` | Figure 1 — composition (Claim 1), three panels in one file; reads only from `results/` |
| `scripts/figure_2.ipynb` | Figure 2 — occupancy vs. output (Claim 2); 7 genes, peak tracks + induction rank |
| `scripts/figure_3.ipynb` | Figure 3 — filtering-series test (Claim 3); rejects the intersection-artifact hypothesis |
| `scripts/figure_4.ipynb` | Figure 4 — robustness; annotation-depth control, *isp-1* concordance, raw-count magnitude |
| `scripts/table_s1.ipynb` | Table S1 — full 72-gene census with inclusion rule and regulon-membership flag |
| `scripts/figure_s2.ipynb` | Figure S2 — metric sensitivity; full Score vs. Score/variability rank-rank scatter |
| `scripts/figure_s1.ipynb` | Figure S1 — pipeline validation; GO positive control on the Pfam census |
| `scripts/figure_s3.ipynb` | Figure S3 — peak-assignment window sensitivity (0.5–10kb, with/without operon logic) |

## Data

| File | What it is | Source |
|---|---|---|
| `data/raw/ATFS1_targets_Soo.xlsx` | Soo & Van Raamsdonk high-confidence target table (61 genes, plus *hsp-6*/*hsp-60* as reference rows — see `gate_decisions.md`) with both ranking metrics and the ChIP-seq binding column | microPublication Biology, [10.17912/micropub.biology.000484](https://doi.org/10.17912/micropub.biology.000484) |
| `data/raw/nargund2015_TableS1-S2.xlsx` | Gene-level ATFS-1-bound list cited in Nargund 2015's prose | Mol Cell, [PMC4385436](https://pmc.ncbi.nlm.nih.gov/articles/PMC4385436/) |
| `data/raw/nargund2012_TableS2_spg7_upregulated.xlsx` | Genes up-regulated under *spg-7*(RNAi) (685 genes) | Science [10.1126/science.1223560](https://doi.org/10.1126/science.1223560), SOM. Retrieved 2026-08-11 |
| `data/raw/nargund2012_TableS3_spg7_ATFS1dependent.xlsx` | The ATFS-1-**dependent** subset of the above (391 genes) | Science [10.1126/science.1223560](https://doi.org/10.1126/science.1223560), SOM. Retrieved 2026-08-11 |
| `data/raw/wu2018_AdditionalFile2.xlsx` | Wu 2018 differentially expressed gene lists, seven sheets by genotype (*nuo-6*, *nuo-6;atfs-1*, *atfs-1(gk3094)*, *et15*, *et17*, *nuo-6;hif-1*, *hif-1*) | BMC Biology [10.1186/s12915-018-0615-3](https://doi.org/10.1186/s12915-018-0615-3), Additional file 2. Retrieved 2026-08-11 |
| `data/raw/GSE63803_peaks.txt.gz` | ATFS-1 ChIP-seq raw peaks, called on ce6 with MACS 1.4, in *spg-7*(RNAi) worms | GEO [GSE63803](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63803) |
| `data/raw/c_elegans.PRJNA13758.WS285.annotations.gff3.gz` | WS285 genome annotation. Supplies operon features for operon-aware peak assignment | WormBase WS285 (EBI mirror) |
| `ref_data/c_elegans.PRJNA13758.WS285.geneIDs.txt.gz` | WS285 gene ID / sequence name / public name mapping | WormBase WS285 (EBI mirror) |
| `ref_data/go/wb.gaf.gz` | *C. elegans* GO annotations, GAF 2.2 (release 2026-05-21) | [GO Consortium](http://current.geneontology.org/annotations/wb.gaf.gz). Retrieved 2026-08-13 |
| `ref_data/go/go-basic.obo` | GO ontology graph, needed to propagate annotations to ancestor terms (release 2026-07-26) | [GO Consortium](http://current.geneontology.org/ontology/go-basic.obo). Retrieved 2026-08-13 |
| `ref_data/GSE38196/` | Nargund 2012 raw Affymetrix microarrays — 12 samples, WT / *atfs-1(tm4525)* × control / *spg-7*(RNAi), 3 replicates | GEO [GSE38196](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE38196) |
| `ref_data/GSE110984/` | RNA-seq CPM tables (raw and normalised), 43 samples | GEO [GSE110984](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110984) |
| `data/liftover/` | ce6→ce11 chain file, the `liftOver` binary, and the lifted peak BEDs | UCSC |
| `data/chaperone_protease_census.csv` | Frozen 72-gene chaperone/QC-protease census (Pfam-domain based); inclusion rule and borderline cases documented in `gate_decisions.md` | Built by `scripts/census_build.ipynb` from WS285 |

WormBase and NCBI both refuse scripted downloads; the WormBase files here came from
the EBI mirror. Anything retrieved by hand is dated in the table above.

## Full analysis record

The day-by-day decision log, every verified constant, standing conventions (dual-metric
reporting, no silent fallbacks, absolute-vs-relative claim framing), corrections, and
known open items all live in `gate_decisions.md` — kept as the single source of truth
rather than duplicated here. Nothing in that history is overwritten; corrections are
logged alongside the original entries they correct, not silently edited in place.
