# The architecture of the ATFS-1 transcriptional output

A reanalysis of published *C. elegans* data asking whether the mitochondrial unfolded
protein response (UPR^mt), which is triggered by import failure rather than by unfolded
protein, actually produces a folding-centric transcriptional output.

The work is computational only. Every input is public, every intermediate is a small
table, and the whole analysis is meant to be reproducible from these files and the
accessions listed below.

## Environment

Built and run on macOS (Apple Silicon), Python 3.11. The full specification is in
`environment.yml`, pinned to the versions the committed notebook outputs were
produced under.

```
conda env create -f environment.yml
conda activate atfs1
jupyter lab
```

Every notebook resets its working directory to the project root in the first cell, so
each runs correctly from either `scripts/` or the repo root, and each runs
top-to-bottom without depending on any other notebook having been run first.

The only external tool is `ucsc-liftover`, used once for the ce6 → ce11 peak
conversion; its output is committed, so nothing needs to be re-lifted to reproduce
the analyses. No step reaches the network at runtime — every input is a file listed
in the table below.

### Reproducing the analyses

| Notebook | What it produces |
|---|---|
| `scripts/census_build.ipynb` | Rebuilds the chaperone/protease census from Pfam domains and asserts it still matches the frozen CSV |
| `scripts/binding.ipynb` | Gate 0/1 — binding reconciliation, operon status, the *hsp-6* question |
| `scripts/census.ipynb` | Analysis B — chaperone/protease census vs. the regulon (2 of 61) |
| `scripts/analysis_c.ipynb` | Analysis C — operon-aware peak assignment, occupancy vs. output |
| `scripts/analysis_a.ipynb` | Analysis A — GO enrichment, expressed background, filtering-series walk |
| `scripts/analysis_d.ipynb` | Analysis D — robustness checks and the Gate 2 evidence summary |
| `scripts/wu2018_verification.ipynb` | Reconstruction of Wu 2018's published 1,704 / 529 counts |

`scripts/analysis_c.ipynb` needs the WS285 GFF3 annotation, and `analysis_a.ipynb`
needs `go-basic.obo`; both are gitignored for size and are re-downloadable from the
sources in the data table.

## Data

| File | What it is | Source |
|---|---|---|
| `data/raw/ATFS1_targets_Soo.xlsx` | Soo & Van Raamsdonk high-confidence target table (61 genes) with both ranking metrics and the ChIP-seq binding column | microPublication Biology, [10.17912/micropub.biology.000484](https://doi.org/10.17912/micropub.biology.000484) |
| `data/raw/nargund2015_TableS1-S2.xlsx` | Gene-level ATFS-1-bound list cited in Nargund 2015's prose | Mol Cell, [PMC4385436](https://pmc.ncbi.nlm.nih.gov/articles/PMC4385436/) |
| `data/raw/nargund2012_TableS2_spg7_upregulated.xlsx` | Genes up-regulated under *spg-7*(RNAi) (685 genes) | Science [10.1126/science.1223560](https://doi.org/10.1126/science.1223560), SOM. Retrieved 2026-08-11 |
| `data/raw/nargund2012_TableS3_spg7_ATFS1dependent.xlsx` | The ATFS-1-**dependent** subset of the above (391 genes) — the table Gate 1 turns on | Science [10.1126/science.1223560](https://doi.org/10.1126/science.1223560), SOM. Retrieved 2026-08-11 |
| `data/raw/wu2018_AdditionalFile2.xlsx` | Wu 2018 differentially expressed gene lists, seven sheets by genotype (*nuo-6*, *nuo-6;atfs-1*, *atfs-1(gk3094)*, *et15*, *et17*, *nuo-6;hif-1*, *hif-1*) | BMC Biology [10.1186/s12915-018-0615-3](https://doi.org/10.1186/s12915-018-0615-3), Additional file 2. Retrieved 2026-08-11 |
| `data/raw/GSE63803_peaks.txt.gz` | ATFS-1 ChIP-seq raw peaks, called on ce6 with MACS 1.4, in *spg-7*(RNAi) worms | GEO [GSE63803](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63803) |
| `data/raw/c_elegans.PRJNA13758.WS285.annotations.gff3.gz` | WS285 genome annotation. Supplies operon features for operon-aware peak assignment | WormBase WS285 (EBI mirror) |
| `ref_data/c_elegans.PRJNA13758.WS285.geneIDs.txt.gz` | WS285 gene ID / sequence name / public name mapping | WormBase WS285 (EBI mirror) |
| `ref_data/go/wb.gaf.gz` | *C. elegans* GO annotations, GAF 2.2 (release 2026-05-21) | [GO Consortium](http://current.geneontology.org/annotations/wb.gaf.gz). Retrieved 2026-08-13 |
| `ref_data/go/go-basic.obo` | GO ontology graph, needed to propagate annotations to ancestor terms (release 2026-07-26) | [GO Consortium](http://current.geneontology.org/ontology/go-basic.obo). Retrieved 2026-08-13 |
| `ref_data/GSE38196/` | Nargund 2012 raw Affymetrix microarrays — 12 samples, WT / *atfs-1(tm4525)* × control / *spg-7*(RNAi), 3 replicates | GEO [GSE38196](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE38196) |
| `ref_data/GSE110984/` | RNA-seq CPM tables (raw and normalised), 43 samples | GEO [GSE110984](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110984) |
| `data/liftover/` | ce6→ce11 chain file, the `liftOver` binary, and the lifted peak BEDs | UCSC |

WormBase and NCBI both refuse scripted downloads; the WormBase files here came from
the EBI mirror. Anything retrieved by hand is dated in the table above.

## Verified constants

Checked against the source file and primary text — usable without re-deriving.

- 61 genes; **28 of 61 (45.9%)** carry no gene symbol
- **22 of 61 (36%)** flagged ATFS-1-bound in Soo's column
- **57 of 61** upregulated in *isp-1*; the exceptions are F49H12.4, Y51B9A.9, H34I24.2, tag-234
- Score = `nuo-6% + et15% + et17% − 3 × (nuo-6;atfs-1%)`, exact to rounding
- Genes above *hsp-6*: **42** on Score, **27–28** on Score/variability (boundary gene Y73F8A.27, 0.4% below the cut)
- Folding/QC in the 61, strict rule: *dnj-10* (Score rank 45, corrected 23) and *ymel-1* (61, 58). Permissive rule adds *prx-19* (54, 20)
- *hsp-6* inserted: rank **43 of 62** on Score, **29 of 62** corrected
- WT baseline zeros: C07G1.7 in 2 of 12 WT replicates; F22B3.7 in **9** of 12 (corrected 2026-08-14, was recorded as 8 — see `gate_decisions.md`)
- 38 replicate columns: WT 12, *atfs-1* 6, *nuo-6* 6, *nuo-6;atfs-1* 3, *et15* 5, *et17* 6

## Standing rules

**Dual-metric reporting.** The source file carries two ranking metrics in adjacent
columns — Score (uncorrected) and Score/variability (Soo's own correction for
near-zero denominators). They disagree, and on several genes they invert. Every rank
or magnitude claim is reported on both, in the same sentence, with the more
conservative number first. A claim that survives only on the uncorrected Score does
not go in the paper.

**Binding is not binary.** State the evidence class behind every binding assignment.
GSE63803 is a single antibody sample against a single no-antibody mock, with no input
and no biological replicate. Absence of a called peak is reported as absence of a
called peak, never as absence of binding.

**No silent fallbacks.** If a source cannot be reached, the code raises. It does not
print a plausible answer. Three separate results in this repo were once produced by
`except` branches that printed hardcoded conclusions; see `gate_decisions.md`.

**Claim 1 is an absolute claim, never a relative one.** Folding machinery is a trace
*component* of the ATFS-1 output — 2 of 61. It is not depleted, not
under-represented, and not "unenriched": against the expressed background 2 of 61 is
6.8× the 0.30 expected by chance. Analysis A establishes this directly, so any of
those three phrasings would be contradicted by our own results.

## Log

- **2026-08-08** — Environment set up, `GEOquery` installed, reference and supplementary datasets downloaded.
- **2026-08-09** — Gate 0 and most of Gate 1: peak liftover ce6→ce11 (1,005/1,005 mapped), binding reconciliation, dataset overlap, operon lookup.
- **2026-08-11** — Audit of everything above. Found and fixed three fabricated results and three silently-failed downloads that had been saved as HTML error pages; obtained the real Nargund 2012 supplementary tables, the real WormBase WS285 files, and Wu 2018's DEG lists. Gate 1's named question is now answered from primary data. Details in `gate_decisions.md`.
- **2026-08-12** — Froze the chaperone/protease census (72 genes) and ran Analysis B (`scripts/census.ipynb`): **2 of 61** regulon genes are folding/QC machinery (strict), **5 of 61** (permissive). Matches the roadmap's pre-recorded ranks exactly. Details in `gate_decisions.md`.
- **2026-08-13** — Corrected the *ymel-1* binding call (bound, not unbound - a naming-alias gap, see `gate_decisions.md`). Built and validated an operon-aware ChIP peak-to-gene assignment and ran Analysis C (`scripts/analysis_c.ipynb`): **101 of 391 (25.8%)** spg-7 ATFS-1-dependent genes are bound (primary, condition-matched). Also found and fixed a row-count bug affecting already-committed numbers: Nargund 2012 Tables S2/S3 are **685** and **391** genes, not 310/163 as previously stated (the hsp-6 conclusion itself was unaffected). Full details in `gate_decisions.md`.

- **2026-08-13** — Ran Analysis A (`scripts/analysis_a.ipynb`): GO enrichment of the regulon against the genes GSE110984's own filter kept, with the pipeline validated on the Pfam-built census before use. The intersection-artifact hypothesis is **rejected** — folding representation rises as the three-condition filter tightens (0.72% → 0.76% → 1.30% → 3.28%), so the shortage of chaperones among the 61 is real biology, not a filtering side-effect. One category survives correction: glucuronosyltransferase activity, 17.2×, FDR 0.041. Folding machinery is *not* depleted relative to background, which constrains how Claim 1 may be worded (see Standing rules). Details in `gate_decisions.md`.
- **2026-08-14** — Pre-freeze audit before figures and writing. Verified all 27 documented numbers against source data by independent recomputation (zero mismatches), confirmed no AI attribution and no `Context/` leak anywhere in history, and fixed three reproducibility defects: three notebooks declared a Jupyter kernel that does not exist on a clean clone, `binding.ipynb`'s stored outputs had been produced under the wrong Python, and the environment was documented but never specified (added `environment.yml`). Closed the largest gap by writing `scripts/census_build.ipynb`: the frozen 72-gene census **reproduces exactly** from the annotation file, and two ambiguities in the recorded rule were corrected in the process (Lon needs both domains; the signal-peptide screen is per-protein). No result changed. Details in `gate_decisions.md`.
- **2026-08-14** — Ran Analysis D (`scripts/analysis_d.ipynb`, Day 7/Gate 2) and pushed the two pending commits (GitHub's contributor cache issue is confirmed stale-only — live API and full git history are clean, see `gate_decisions.md` history for the earlier investigation). Raw-count magnitude check, metric-sensitivity panel, *isp-1* concordance, and an expression-matched annotation-depth control all pass or are explained. Corrected a previously-recorded constant (F22B3.7 WT zero count: 9 of 12, not 8). Gate 2 evidence assembled and laid out for the author. **Gate 2 closed the same day: Outcome 3 confirmed** — folding/QC machinery present but weak, concentrated in the highest-confidence tier rather than absent throughout. Analysis is now frozen; Days 8–14 are figures and writing. Full details in `gate_decisions.md`.

## Known open items

- The Wu 2018 **529** figure (*atfs-1(et15)* ∩ *atfs-1(et17)* upregulated) is now exactly confirmed by reconstruction from the real data. The **1,704** figure (*nuo-6* ATFS-1-dependent upregulated) reconstructs to **1,673** — a 98% match, not exact; no duplicate genes, missing IDs, or threshold difference found to explain the remaining 31-gene gap. Close enough to use, not fully resolved. See `gate_decisions.md`.
- No master gene table yet: only the two anchor genes have been annotated, not all 61.
- The glucuronosyltransferase result (5 genes, FDR 0.041) rests on 5 genes and has not been checked against the individual gene identities or the UGT family's known biology. It should not go in the paper as a positive finding until it has.
- Nargund 2012's 391-gene *spg-7* set was not put through Analysis A. It comes from a different platform (Affymetrix, GSE38196) and would need its own array-detectable background rather than GSE110984's; using the expressed background from a different experiment would be exactly the error Analysis A is built to avoid.
- **Analysis is frozen as of Day 7, per the roadmap's own rule.** No new computation after this point; anything found while writing is handled in prose.
- 6 of the 7 disagreements between this project's independent binding calls and Soo's published column (`srm-3`, `nhr-115`, `DC2.5`, `F56C11.3`, `clec-265`, `M01F1.4`) are not yet individually verified the way *ymel-1* and *tspo-1* were. The secondary cross-condition count (29/61) should not be cited as more authoritative than Soo's 22/61 until they are.

## Chaperone/protease census

`data/chaperone_protease_census.csv` — 72 genes (65 chaperones, 7 QC proteases),
frozen before any comparison against ATFS-1 target data. `scripts/census_build.ipynb`
rebuilds it from the annotation file and raises if the result no longer matches the
frozen CSV, so the rule stays checkable rather than only described; it verifies and
never overwrites. Built from real Pfam protein-domain
annotations (WS285), not gene-name pattern matching, with signal-peptide screening to
exclude ER-targeted genes (out of scope — this paper is about the mitochondrial UPR,
not the separate ER-UPR pathway) and manual review of a few domain matches that turned
out to be secondary features of unrelated proteins (a lipid kinase, a vulval-development
gene, an endosomal trafficking protein). Full inclusion rule, exclusions, and the
roadmap's named borderline cases (*prx-19*, *cbp-3*, *tspo-1* — checked, not included)
are documented in `gate_decisions.md`.

## A note on hsp-6 and hsp-60

`ATFS1_targets_Soo.xlsx` loads to 63 gene rows, not 61. **61 is correct** — checked
against Soo & Van Raamsdonk 2021 directly, which states neither *hsp-6* nor *hsp-60*
are among the 61 high-confidence genes. They're included in the sheet as reference
rows for comparison against the field-standard reporter genes, scored with the same
formula but not census members. `binding.ipynb` splits these out explicitly and
asserts the census count is 61. See `gate_decisions.md` for the full citation.
