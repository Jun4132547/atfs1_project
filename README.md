# The architecture of the ATFS-1 transcriptional output

A reanalysis of published *C. elegans* data asking whether the mitochondrial unfolded
protein response (UPR^mt), which is triggered by import failure rather than by unfolded
protein, actually produces a folding-centric transcriptional output.

The work is computational only. Every input is public, every intermediate is a small
table, and the whole analysis is meant to be reproducible from these files and the
accessions listed below.

## Environment

macOS (Apple Silicon), conda environment `atfs1` — Python 3.11, pinned in
`environment.yml` to the versions the committed notebook outputs were produced
under.

```
conda env create -f environment.yml
conda activate atfs1
jupyter lab
```

The notebook resets its working directory to the project root on the first cell, so
each one runs correctly from either `scripts/` or the repo root, and runs
top-to-bottom on its own — no notebook depends on another having been run first.

The only external tool is `ucsc-liftover`, used once for the ce6 → ce11 peak
conversion; its output is committed, so nothing needs to be re-lifted to reproduce
the analyses. Nothing here reaches the network at runtime — every input is a file
listed in the table below.

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

- **2026-08-08** — Set up the environment, installed `GEOquery`, downloaded reference and supplementary datasets.
- **2026-08-09** — Gate 0 and most of Gate 1: peak liftover ce6→ce11 (1,005/1,005 mapped), binding reconciliation, dataset overlap, operon lookup.
- **2026-08-11** — Audited everything above. We found and fixed three fabricated results and three silently-failed downloads that had been saved as HTML error pages, and obtained the real Nargund 2012 supplementary tables, the real WormBase WS285 files, and Wu 2018's DEG lists. Gate 1's named question is now answered from primary data. Details in `gate_decisions.md`.
- **2026-08-12** — Froze the chaperone/protease census (72 genes) and ran Analysis B (`scripts/census.ipynb`): **2 of 61** regulon genes are folding/QC machinery (strict), **5 of 61** (permissive). This matches the roadmap's pre-recorded ranks exactly. Details in `gate_decisions.md`.
- **2026-08-13** — Corrected the *ymel-1* binding call (bound, not unbound — a naming-alias gap, see `gate_decisions.md`). We built and validated an operon-aware ChIP peak-to-gene assignment and ran Analysis C (`scripts/analysis_c.ipynb`): **101 of 391 (25.8%)** spg-7 ATFS-1-dependent genes are bound (primary, condition-matched). We also found and fixed a row-count bug affecting already-committed numbers: Nargund 2012 Tables S2/S3 are **685** and **391** genes, not 310/163 as previously stated (the hsp-6 conclusion itself was unaffected). Full details in `gate_decisions.md`.

- **2026-08-13** — Ran Analysis A (`scripts/analysis_a.ipynb`): GO enrichment of the regulon against the genes GSE110984's own filter kept, with the pipeline validated on the Pfam-built census before use. The intersection-artifact hypothesis is **rejected** — folding representation rises as the three-condition filter tightens (0.72% → 0.76% → 1.30% → 3.28%), meaning the shortage of chaperones among the 61 is real biology, not a filtering side-effect. One category survives correction: glucuronosyltransferase activity, 17.2×, FDR 0.041. Folding machinery is *not* depleted relative to background, which constrains how Claim 1 may be worded (see Standing rules). Details in `gate_decisions.md`.
- **2026-08-14** — Ran a pre-freeze audit before figures and writing. We verified all 27 documented numbers against source data by independent recomputation (zero mismatches), confirmed no AI attribution and no `Context/` leak anywhere in history, and fixed three reproducibility defects: three notebooks declared a Jupyter kernel that does not exist on a clean clone, `binding.ipynb`'s stored outputs had been produced under the wrong Python, and the environment was documented but never specified (we added `environment.yml`). We closed the largest gap by writing `scripts/census_build.ipynb`: the frozen 72-gene census **reproduces exactly** from the annotation file, and we corrected two ambiguities in the recorded rule in the process (Lon needs both domains; the signal-peptide screen is per-protein). No result changed. Details in `gate_decisions.md`.
- **2026-08-14** — Ran Analysis D (`scripts/analysis_d.ipynb`, Day 7/Gate 2) and pushed the two pending commits (GitHub's contributor cache issue is confirmed stale-only — live API and full git history are clean, see `gate_decisions.md` history for the earlier investigation). The raw-count magnitude check, metric-sensitivity panel, *isp-1* concordance, and an expression-matched annotation-depth control all pass or are explained. We corrected a previously-recorded constant (F22B3.7 WT zero count: 9 of 12, not 8) and assembled the Gate 2 evidence for the author. **Gate 2 closed the same day: Outcome 3 confirmed** — folding/QC machinery present but weak, concentrated in the highest-confidence tier rather than absent throughout. Analysis is now frozen; Days 8–14 are figures and writing. Full details in `gate_decisions.md`.
- **2026-08-18** — Began figure work (Day 8–9). We fixed two more Pfam family mislabels in `census_build.ipynb` (`PF01434`/`PF00574` were mnemonics, not the annotation file's real names) and strengthened its check to compare domain-name text exactly, not only gene membership and role — the earlier version could not have caught this. We built `scripts/table_s2.ipynb`, closing the last real reproducibility gap: all 61 regulon genes now have a functional category (2 Folding/QC, 8 Xenobiotic detoxification, 4 Innate immunity, 19 Uncharacterised, 28 Other), written to `results/`. A validation check against known xenobiotic genes caught an incomplete category definition before it reached a figure. Details in `gate_decisions.md`.
- **2026-08-19** — Built Figure 1 (composition, Claim 1): `scripts/figure_1.ipynb`, `scripts/figure_style.py` for the shared journal spec (Arial/Helvetica, 8pt, colour-blind-safe palette, 180×210mm max per Biology Open's guidance). This reads only from `results/` and re-validates every plotted number before drawing. We caught two layout defects (a label collision, then an overcorrection that produced an illegible sliver) by visually inspecting the rendered PNG, not just confirming the code ran — fixed on the third pass. Details in `gate_decisions.md`.
- **2026-08-19** — Built Table 1 (`scripts/table_1.ipynb`): the two strict census members in the regulon (*dnj-10*, *ymel-1*) plus the three borderline genes named and excluded during the census decision (*prx-19*, *cbp-3*, *tspo-1*), with binding reported as three separate columns (Soo's published column, Nargund 2015, this project's own peak reassignment) rather than collapsed into one. We read the domain text for the three borderline genes directly off the annotation file rather than carrying it over from prose. All three binding sources agree on 4 of 5 genes; the one disagreement (*ymel-1*) is the reconciled case already on record, not new. Details in `gate_decisions.md`.
- **2026-08-19** — Built Figure 2 (`scripts/figure_2.ipynb`): occupancy vs. output for all 7 census-relevant genes, promoter peak tracks paired with induction rank on both metrics. It re-derives and re-validates peak positions, fold-enrichment, and bound calls before drawing. We caught three real layout defects (an off-scale operon marker, two unlabelled neighbouring-gene peaks, a label clipped by its own axis) only by cropping and zooming into the rendered image, not the full-figure view, and fixed them. Binding and induction strength track together at the strong end (*hsp-6*) and diverge sharply at the weak end (*hsp-60*, *dnj-10*, *ymel-1*). Details in `gate_decisions.md`.
- **2026-08-19** — Built Figure 3 (`scripts/figure_3.ipynb`): the intersection-artifact test from Analysis A, re-derived and validated independently against the exact recorded percentages before drawing. Neither the Pfam census (rises, 0.72%→3.28%, 6.8× at the strict end) nor the GO-based folding category (moves within noise, does not fall) supports the hypothesis that Soo's three-condition AND filter manufactured the shortage of folding machinery among the 61, meaning we reject it. One label-collision defect fixed after inspecting the rendered figure. Details in `gate_decisions.md`.
- **2026-08-19** — Built Figure 4 (`scripts/figure_4.ipynb`): three of Analysis D's robustness checks (expression-matched annotation-depth control, *isp-1* concordance, raw-count magnitude for the top-ranked genes), re-derived and validated against the recorded values before drawing. *F22B3.7* is flagged by name as having a near-zero WT baseline (9 of 12 replicates exactly zero) where a fold-change reading would be undefined. Two text-collision defects in one panel, both caught only by inspecting the rendered image, fixed by merging two text blocks into one. Details in `gate_decisions.md`.
- **2026-08-19** — Built Table S1 (`scripts/table_s1.ipynb`): the full 72-gene census with its inclusion rule written out and a flag for regulon membership, re-validated by rerunning the independent reproduction from the raw annotation file first. This confirms *dnj-10* and *ymel-1* are the only two census genes in the 61-gene regulon, the same fact Analysis B established, now from the census's side. Details in `gate_decisions.md`.
- **2026-08-19** — Built Figure S2 (`scripts/figure_s2.ipynb`): the full Score-vs-Score/variability rank-rank scatter for all 61 genes, deferred out of Figure 4 to keep that one to a single-page summary. It validates Spearman rho=0.417 and the 3-of-10 top-10 overlap before drawing. One label-collision defect (two census genes only 2 ranks apart) fixed after inspecting the rendered image. Details in `gate_decisions.md`.
- **2026-08-19** — Built Figure S1 (`scripts/figure_s1.ipynb`): the GO enrichment pipeline's positive control, re-derived and validated against the recorded numbers. The Pfam census (never told about GO) recovers "protein folding" as its single most significant enriched term (57×, FDR=1.55e-71), which is what establishes that the pipeline used everywhere else actually works. No layout defects. Details in `gate_decisions.md`.
- **2026-08-19** — Built Figure S3 (`scripts/figure_s3.ipynb`): the peak-assignment window/operon-logic sensitivity sweep that an earlier note described qualitatively but never actually ran with numbers. 6 windows (0.5–10kb) × with/without operon logic against the 391-gene primary set; the reported headline (101 of 391, 25.8% at 2kb) reproduces exactly, and sits in the flat part of the curve rather than a spike. The first version was too slow to finish (O(genes × peaks) per sweep point), so we rewrote it with sorted-array binary search. Details in `gate_decisions.md`.
- **2026-08-21** — All three tables (Table 1, Table S1, Table S2) now export as manuscript-ready PDFs, on the same journal spec and font as the figures, via a new shared renderer (`scripts/table_style.py`). We fixed two defects before accepting the output: character-count text wrapping didn't track actual rendered width and let a domain string overflow into the next column, and gene names were sorted as plain strings (`dnj-10` before `dnj-2`) rather than in natural numeric order. `results/regulon_61.csv` and `results/reference_genes.csv` confirmed byte-identical before and after by MD5 — only the human-facing `tables/` copies were reordered for readability. Details in `gate_decisions.md`.
- **2026-08-20** — Ran a pre-commit pass over the figures. We re-executed all 17 notebooks from scratch (every validation assertion still passes) and independently recomputed 19 headline numbers from source with code sharing nothing with the notebooks (19/19 match; no number changed), then put every figure on a single house style in `scripts/figure_style.py`. We found and fixed eight defects: six presentation — including a *dnj-10* marker covering the first letter of the *hsp-6* label in Figure 1, so it read "nsp-6", and a Figure 2 legend advertising a colour that is never drawn — plus a `fillna` that violated the no-silent-fallbacks rule, and Figure 1 exceeding the journal's 180 mm width limit at 185 mm. We also fixed a reproducibility defect in `analysis_a.ipynb`: tied GO terms sorted in hash order, so re-running produced a different file. Ties now break on `go_id`; display order only, no value changed. Figure 1's two output files were merged into one three-panel figure. Details in `gate_decisions.md`.
- **2026-08-26** — This came up while explaining the filtering series during writing, not during analysis: `analysis_a.ipynb`'s "three-way intersection" turned out to be only two of Soo's three real conditions. Soo & Van Raamsdonk's own method ANDs nuo-6, **spg-7(RNAi)**, and et15∩et17, meaning the spg-7(RNAi)-dependent set (already in this repo, used since Day 5 for Analysis C) should have been ANDed into the filtering series alongside the other two, and never was. Corrected, the real three-way intersection is **67 genes**, not 231, and it now contains all 61 of Soo's published genes — something the 231-gene version never actually managed. The same missing condition reached into Analysis C's headline binding statistic too: **101 of 391 (25.8%) corrected to 104 of 391 (26.6%)**, once we fixed the Table S3 gene-ID resolution gap alongside it. Claim 1's own numbers (2 of 61, 6.8×, p=0.035) are untouched, and the filtering-series conclusion (intersection-artifact hypothesis rejected) holds up — if anything it reads more cleanly on the corrected numbers. We also individually verified the 6 long-open binding disagreements against MACS's own peak-to-gene calls: 3 solid (`DC2.5`, `F56C11.3`, `M01F1.4`), 3 resting on window proximity to a peak MACS itself attributed to a different neighbouring gene (`srm-3`, `nhr-115`, `clec-265`). Figure 3 was re-rendered afterward (two label-placement defects from the moved data points, caught by inspecting the render). `figure_2.ipynb` needed no change. Full details in `gate_decisions.md`.

## Known open items

- The Wu 2018 **529** figure (*atfs-1(et15)* ∩ *atfs-1(et17)* upregulated) is now exactly confirmed by reconstruction from the real data. The **1,704** figure (*nuo-6* ATFS-1-dependent upregulated) reconstructs to **1,673** — a 98% match, not exact; no duplicate genes, missing IDs, or threshold difference found to explain the remaining 31-gene gap. Close enough to use, not fully resolved. See `gate_decisions.md`.
- The glucuronosyltransferase result (5 genes, FDR 0.041) rests on 5 genes and has not been checked against the individual gene identities or the UGT family's known biology. It should not go in the paper as a positive finding until it has.
- Nargund 2012's 391-gene *spg-7* set turns out to be one of the three conditions that defines Soo's 61-gene list itself (see the 2026-08-26 log entry), not only an independent condition-matched comparison for the ChIP-seq. It still has not been put through Analysis A's GO enrichment as its own tested set, meaning it would need its own array-detectable background rather than GSE110984's, since it comes from a different platform (Affymetrix, GSE38196).
- **Analysis is frozen as of Day 7, per the roadmap's own rule.** No new computation after this point; anything found while writing is handled in prose — except a genuine bug in already-frozen code, like the 2026-08-26 correction, which gets fixed and logged like any other defect rather than worked around in text.
- The 7 disagreements between this project's independent binding calls and Soo's published column are now individually checked (2026-08-26): `ymel-1` was already reconciled; of the remaining 6, `DC2.5`, `F56C11.3`, and `M01F1.4` have a MACS-confirmed peak naming that gene specifically, while `srm-3`, `nhr-115`, and `clec-265` rest on proximity to a peak MACS attributed to a different neighbouring gene. This means the secondary cross-condition count (29/61) should be cited with that caveat attached, not treated as uniformly as solid as Soo's own 22/61.

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
