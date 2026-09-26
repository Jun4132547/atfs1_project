# The architecture of the ATFS-1 transcriptional output

[![DOI](https://zenodo.org/badge/1334836842.svg)](https://doi.org/10.5281/zenodo.22944393)

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
| `scripts/table_1.ipynb` | Upstream only (not a standalone manuscript table — see Table S1): computes the five census-relevant genes' Pfam domains and three-source binding comparison, written to `results/table_1.csv` |
| `scripts/figure_1.ipynb` | Figure 1 — composition (Claim 1), three panels in one file; reads only from `results/` |
| `scripts/figure_2.ipynb` | Figure 2 — occupancy vs. output (Claim 2); 7 genes, peak tracks + induction rank |
| `scripts/figure_3.ipynb` | Figure 3 — filtering-series test (Claim 3) and the regulon's own GO-term enrichment profile; two independent analyses in one file |
| `scripts/figure_4.ipynb` | Figure 4 — robustness; annotation-depth control, *isp-1* concordance, raw-count magnitude |
| `scripts/figure_5.ipynb` | Figure 5 — revised-model schematic; conceptual only, draws from `results/` used by Figures 1 and 2, no new analysis |
| `scripts/table_s1.ipynb` | Table S1 — full 72-gene census with inclusion rule and regulon-membership flag, plus ATFS-1 binding status for the two overlapping census genes and three additional borderline genes considered but excluded (reads `table_1.ipynb`'s output rather than recomputing it) |
| `scripts/figure_s2.ipynb` | Figure S2 — metric sensitivity; full Score vs. Score/variability rank-rank scatter |
| `scripts/figure_s1.ipynb` | Figure S1 — pipeline validation; GO positive control on the Pfam census |
| `scripts/figure_s3.ipynb` | Figure S3 — peak-assignment window sensitivity (0.5–10kb, with/without operon logic) |

## Data

| File | What it is | Source |
|---|---|---|
| `data/raw/ATFS1_targets_Soo.xlsx` | Soo & Van Raamsdonk high-confidence target table (61 genes, plus *hsp-6*/*hsp-60* as reference rows, not regulon members) with both ranking metrics and the ChIP-seq binding column | microPublication Biology, [10.17912/micropub.biology.000484](https://doi.org/10.17912/micropub.biology.000484) |
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
| `data/chaperone_protease_census.csv` | Frozen 72-gene chaperone/QC-protease census (Pfam-domain based); full inclusion rule and borderline-case decisions kept in the author's private working log, available on request | Built by `scripts/census_build.ipynb` from WS285 |

WormBase and NCBI both refuse scripted downloads; the WormBase files here came from
the EBI mirror. Anything retrieved by hand is dated in the table above.

## Full analysis record

The day-by-day decision log, every verified constant, standing conventions (dual-metric
reporting, no silent fallbacks, absolute-vs-relative claim framing), and known open
items are kept in a private working log (`gate_decisions.md`, not tracked in this
repo) available from the author on request. Nothing in that history has ever been
overwritten; corrections are logged alongside the original entries they correct, not
silently edited in place — see Corrections below for the headline list.

## Corrections

A short, dated list of headline corrections to previously stated facts or numbers in
this project. Full detail, reasoning, and verification for each is kept in the private
working log referenced above.

- **2026-08-11** — Three early results (an operon-membership check for two anchor
  genes, and a gene-list lookup for *hsp-6*) were found to be silently fabricated by
  error-handling code that printed a plausible answer on failure rather than raising.
  All three were re-derived from real source data.
- **2026-08-12** — The *ymel-1* ATFS-1 binding call corrected from "not bound" to
  "bound" — a gene-naming alias (*yme-1*) had caused it to be missed in Nargund et al.
  (2015)'s table.
- **2026-08-13** — Nargund et al. (2012)'s Table S2/S3 gene counts corrected from
  310/163 to the real 685/391 (a row-counting bug); this did not affect the *hsp-6*
  conclusion drawn from that table.
- **2026-08-14** — F22B3.7's wild-type zero-replicate count corrected from 8 of 12 to
  the real 9 of 12.
- **2026-08-14** — The chaperone/protease census's candidate gene count corrected from
  83 to the real 85; the final 72-gene census itself was unaffected.
- **2026-08-26** — A missing third condition in the three-way gene-set intersection
  underlying the filtering series was found and fixed: corrected from 231 genes to 67.
  The same gap corrected Claim 2's headline binding statistic from 101 of 391 (25.8%)
  to 104 of 391 (26.6%).
- **2026-09-05** — A follow-up review found this project's own account of the
  2026-08-26 correction had overstated it: the earlier 231-gene set did in fact
  contain all 61 regulon genes, just less tightly than the corrected 67-gene set.
  Wording corrected accordingly.
