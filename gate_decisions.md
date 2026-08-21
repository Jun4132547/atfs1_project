# Gate decisions

One entry per decision. Each records what was decided, what it rests on, and what it
means for the claims. Corrections are kept visible rather than overwritten.

---

## Gate 0 · Dual-metric rule

**Date:** 2026-08-09
**Outcome:** Pre-committed — report both metrics, conservative first.

Every rank or magnitude claim is reported on both Score and Score/variability, in the
same sentence, with the more conservative number given first. A claim that survives
only on the uncorrected Score does not go in the paper. Recorded in full in the README
under Standing rules.

---

## Gate 0 · Operon status of the anchor genes

**Date:** 2026-08-09 · **corrected 2026-08-11**
**Outcome:** Withdrawn pending re-derivation. See below.

The original entry read "Confirmed independently promoted — queried WormBase official
API for C07G1.7 and F22B3.7. Neither gene is a downstream operon member."

That result is not supported. The notebook cell wrapped the API call in a bare
`except` that printed "Independently promoted (Not in an operon)" on *any* failure,
producing output identical to a genuine negative. The WormBase REST endpoint returns
403 to scripted requests — as the roadmap itself notes — so the call almost certainly
failed and the answer was manufactured by the error handler.

Re-derived offline against the WS285 GFF3, where operons are annotated features. The
replacement cell raises on any failure instead of defaulting. Both genes resolve
cleanly in the WS285 gene ID table (C07G1.7 → WBGene00015573, F22B3.7 →
WBGene00009038).

**Consequence:** the "induced, not bound" observation depends on this. If either gene
turns out to be a downstream operon member, its unbound status is an artefact of
nearest-TSS assignment and the observation is withdrawn for that gene.

---

## Gate 1 · Peak liftover, ce6 → ce11

**Date:** 2026-08-09
**Outcome:** Complete success.

1,005 of 1,005 peaks mapped to ce11 with UCSC `liftOver`. Zero unmapped
(`data/liftover/peaks_unmapped.bed` is empty).

---

## Gate 1 · Binding reconciliation

**Date:** 2026-08-09 · **corrected 2026-08-12**
**Outcome:** *ymel-1* is bound. 3 of 4 chaperone/QC genes agree between Soo's column and Nargund 2015; *ymel-1* is a genuine, evidenced disagreement, not a wash.

The original entry read "Nargund 2015 Table S1 and Soo's column L agree... *dnj-10*
and *ymel-1* unbound." That was a false negative caused by a naming gap, not a real
agreement: the Day 3 search for *ymel-1* only tried `"ymel-1"` and `"M03C11.5"`
against Nargund 2015's table, but the table predates WormBase's later nomenclature
cleanup and lists the gene under its 2015-era name, **`yme-1`** (after yeast *YME1*)
— row 125, described as *"i-AAA mitochondrial protease,"* sitting directly between
`spg-7` ("m-AAA protease in mitochondria") and `ppgn-1` ("ParaPleGiN AAA protease
family") in a clean block of mitochondrial QC genes. A search that never tries that
name will always return zero matches, regardless of whether the gene is really there.

This was checked, not just corrected by inference. This was found while building
Analysis C's operon-aware peak assignment (`scripts/analysis_c.ipynb`): the raw
GSE63803 peak file — the actual MACS output, independent
of any curated table — has a called peak (fold-enrichment 13.08, FDR 4%) sitting
almost exactly on *ymel-1*'s own TSS, and the depositors' own original gene-name
annotation for that peak reads `"yme-1"` too. *dnj-10* was checked the same way as a
control: no called peak anywhere within 5kb of its TSS, and no mention under any name
or alias anywhere in Nargund 2015's table — a clean, doubly-confirmed negative,
unlike *ymel-1*.

`binding.ipynb` Cells 0 and 1 now search known historical aliases, not just current
gene symbols, and both are re-run and passing: *hsp-6* bound, *hsp-60* bound,
*dnj-10* unbound, *ymel-1* bound — 3 of 4 genes agree between Soo and Nargund 2015;
only *dnj-10* is genuinely unbound by both sources.

**Consequence for Claim 2:** stronger than the restricted version, short of the
roadmap's "all four" scenario. ATFS-1 occupies *hsp-6*, *hsp-60*, and *ymel-1*'s
promoters (three of the four chaperone/QC genes under discussion) and does not drive
any of them into the top ranks of its own regulon — *ymel-1* ranks 61/58 of 61, the
weakest or near-weakest gene in the entire regulon on both metrics. *dnj-10* remains
the one occupancy-without-binding exception, not the rule. State the *dnj-10* vs.
*yme-1*/*ymel-1* naming issue explicitly in the paper's Methods, since a reviewer who
searches Nargund 2015 the same naive way will reach the wrong conclusion too.

---

## Gate 1 · Is *hsp-6* in Nargund 2012's ATFS-1-dependent *spg-7* set?

**Date:** 2026-08-09 · **corrected 2026-08-11** (fabricated) · **resolved 2026-08-11** (from source) · **row count corrected 2026-08-13**
**Outcome:** **No.** Per the roadmap's pre-registered consequence table, Claim 2 **strengthens**.

The original "Confirmed spg-7 dependent" was fabricated: the cell tried to open a file
that had never been downloaded and, on `FileNotFoundError`, printed a hardcoded
`True (Confirmed from Nargund et al. 2012 Science paper)`.

Resolved against the real source. The Nargund 2012 Supporting Online Material was
retrieved from science.org and its Supplementary Tables S2 and S3 added to
`data/raw/`. Table S3 is the paper's ATFS-1-dependent set, defined in its Materials
and Methods as genes whose up-regulation in *atfs-1(tm4525)* was ≤25% of the
up-regulation in wild-type, both under *spg-7*(RNAi) vs. control(RNAi).

*hsp-6* — checked by sequence name (C37H5.8), public name and alias (mthsp-70) — is
absent from Table S3 and from Table S2. The **row counts stated here were wrong and
have been corrected**: Table S3 is **391** genes, not 163; Table S2 is **685**, not
310. Both undercounts came from the same bug (`symbol.notna()` used as a row filter),
which silently drops every real gene that has no assigned public gene symbol — 229 of
Table S3's 391 real rows, including the paper's own anchor genes *C07G1.7* and
*F22B3.7* — while also miscounting the literal column-header row itself as a gene,
since `"Gene symbol"` is a non-null string. Found while building Analysis C, when an
unrelated match-rate check (123 of the stated 163 genes failing to resolve to a real
gene ID) turned out to mean the stated total was wrong, not the matching. Fixed with
a robust filter (real rows have a numeric fold-change value; header/title/divider
rows do not) in both `binding.ipynb` and `analysis_c.ipynb`. **The hsp-6 conclusion
itself is unchanged** — re-checked directly against the corrected, full 391-gene set
and still absent — only the stated denominator was wrong.

**Consequence for Claim 2:** *hsp-6* is not an ATFS-1-dependent target under
*spg-7*(RNAi) — the same condition GSE63803's ChIP-seq was performed in. This closes
the cross-condition confound in Analysis C, where binding data from *spg-7*(RNAi) was
being read against induction data from *nuo-6* and *atfs-1(et15/et17)*.
Occupancy-without-proportionate-output now holds within a single matched condition.
Write Claim 2 as strengthened: ATFS-1 occupies the *hsp-6* promoter but does not drive
it into its own ATFS-1-dependent set even under the condition its binding was measured
in. Do not narrow or drop it.

---

## Gate 1 · GSE110984 / GSE93724 overlap

**Date:** 2026-08-09 · **verified 2026-08-11**
**Outcome:** Overlap confirmed.

The GSE110984 summary states: *"Note that sequencing batch 2 was previously uploaded
as part of GSE93724."* The roadmap flagged this quote as carried forward without
independent confirmation, and the notebook cell asserted it as a hardcoded string
rather than checking anything. The wording has now been read off the live GEO record
directly and matches verbatim. The record also documents two samples removed
(nuo6hif1, atfs1et15) for clustering away from their genotypes; 43 samples remain.

**De-duplication rule:** use GSE110984 as the primary series so the shared batch-2
samples are not counted twice.

---

## Gate 1 · Census denominator: 61, not 63

**Date:** 2026-08-12
**Outcome:** Resolved. The high-confidence census is 61 genes; hsp-6 and hsp-60 are reference rows, not members.

`data/raw/ATFS1_targets_Soo.xlsx` loads to 63 gene rows under the notebook's existing
filter (rows 0-63, one blank separator dropped). Every headline number in the roadmap
("2 genes of 61," "28 of 61 carry no gene symbol," "57 of 61 upregulated in *isp-1*")
assumes 61. This was checked against the actual source paper rather than assumed
either way: Soo & Van Raamsdonk 2021 (microPublication Biology,
[10.17912/micropub.biology.000484](https://doi.org/10.17912/micropub.biology.000484))
state explicitly — *"We identified a total of 61 genes... Surprisingly, neither hsp-6
nor hsp-60 were among the 61 genes on this list."*

hsp-6 and hsp-60 occupy rows 0-1 of the spreadsheet, scored with the same formula,
because Soo added them back in as comparison points against the field-standard
reporter genes — not because they are census members. This matches the roadmap's own
"hsp-6 inserted: rank 43 of 62" language, which was already describing this without
spelling it out.

**Consequence:** `binding.ipynb` Cell 1 now splits the loaded table into 61 census
genes and 2 excluded reference genes explicitly, and asserts the count is 61 rather
than silently trusting it. The chaperone/protease census (Analysis B) and every "of
61" ratio must use the 61-gene set, never the raw 63-row sheet. hsp-6 and hsp-60
remain usable as individual comparison points for Claim 2, just never as census
members.

---

## Day 1 · Chaperone/protease census, frozen

**Date:** 2026-08-12
**Outcome:** 72 genes (65 chaperones, 7 QC proteases). Frozen before any comparison against ATFS-1 target data. File: `data/chaperone_protease_census.csv`.

**Source and method.** WormBase's gene-class pages are a website feature blocked to
scripted access (same 403 behavior as the operon lookup), so this was built instead
from real Pfam protein-domain annotations in the WS285 release
(`c_elegans.PRJNA13758.WS285.protein_annotation.gff3.gz`, EBI mirror) — domain
evidence is a stronger, more falsifiable basis for "is this a chaperone" than gene
naming convention in any case, since it doesn't depend on genes being named `hsp-*`.

**Inclusion rule, written down before the count was known:** a gene qualifies if it
carries one of these Pfam domains, matched with sufficient score to be its real
functional domain rather than a weak structural echo — HSP70 (PF00012), DnaJ/Hsp40
(PF00226), HSP90 (PF00183), HSP20/small-HSP (PF00011), Cpn60/TCP-1 chaperonin
(PF00118), Prefoldin (PF01920), ClpP protease (PF00574), Lon protease (PF05362 +
PF02190), or the FtsH/m-AAA/i-AAA protease family (PF01434) — **and** shows no
ER/secretory signal peptide, since the paper's scope is mitochondrial and cytosolic
folding machinery, not the separate ER-UPR pathway.

> **Two clarifications added 2026-08-14**, when this rule was reconstructed in code
> (`scripts/census_build.ipynb`) and found to reproduce the census exactly. Both
> were ambiguities in the wording above, not errors in the census itself.
> **(1)** The Lon "+" is a conjunction: both PF05362 and PF02190 are required.
> Reading it as "either" admits five genes carrying a lone Lon_C hit.
> **(2)** The signal-peptide screen operates per *protein isoform*, not per gene: a
> gene is excluded when a signal peptide and a qualifying domain occur **on the same
> protein**. Neither "any isoform has a peptide" nor "every domain-bearing isoform
> has one" reproduces the frozen file. See the 2026-08-14 entry for the worked cases.
> **(3)** The candidate count below should read **85**, not 83; 85 − 13 − 2 + 2 = 72.

**Exclusions, enumerated:**
- **13 genes excluded as ER-targeted** (signal peptide present): `hsp-3`, `hsp-4`
  (the two BiP/GRP78 paralogs), `enpl-1` (GRP94/HSP90B1), `stc-1`, and 6 DnaJ-family
  co-chaperones (`dnj-2`, `dnj-7`, `dnj-8`, `dnj-20`, `dnj-27`, `dnj-28`) plus 3
  unnamed genes — `F54F2.9`, `T14G8.3`, `T24H7.2`, identified by name during the
  2026-08-14 reconstruction. This was checked systematically across all 85
  domain-based candidates, not assumed gene-by-gene.
- **3 genes excluded on manual domain-architecture review** — in practice 2, since
  `lido-17` is removed automatically once Lon correctly requires both domains —
  because the matched
  domain is a minor accessory feature, not the gene's primary function: `ppk-3`
  (a 1,400-residue PIKfyve-family lipid kinase; the chaperonin-domain hit scored
  71/1000+ against a >1,400-residue kinase domain), `lido-17` (dominated by a Lin-8
  vulval-development domain; weak secondary Lon-protease hit), `rme-8` (an
  838-residue endosomal-trafficking domain with a small accessory DnaJ domain,
  functionally analogous to auxilin — same category as the PEX19-type exclusion
  below).

**Permissive-rule addendum — the roadmap's named borderline cases, checked, not
included:** `prx-19` (Pex19 domain — a peroxisomal *membrane-protein* import
chaperone, not a folding chaperone; PEX19-type genes are excluded by design),
`cbp-3` (zf-TAZ zinc-finger domain, not a chaperone domain), `tspo-1` (TspO_MBR — an
outer mitochondrial membrane channel/transporter, not a chaperone domain). None
share a Pfam domain with the inclusion list, so the strict/permissive split the
roadmap anticipated collapses here: there is no domain-level argument for including
any of the three. If a reviewer wants the permissive count anyway on functional
rather than domain grounds, it is 72 + up to 3 = 75, with the three named and their
actual domains stated.

**Sanity checks passed:** `hsp-6`, `hsp-60`, `dnj-10`, `ymel-1`, `spg-7`, `clpp-1`,
`cct-1` all present as expected. `daf-21` was checked and confirmed to be `hsp-90`'s
old name (same gene, WBGene00000915) — present under its current name.

**One manual addition, checked not assumed:** prefoldin is a 6-subunit complex
(`pfd-1` through `pfd-6`). Only 4 subunits (`pfd-1`, `pfd-2`, `pfd-4`, `pfd-6`)
matched PF01920 automatically. `pfd-3` (T06G6.9) and `pfd-5` (R151.9) were checked
directly against the annotation file: both are real, confirmed genes with no Pfam
domain call of any kind in this release — most likely because prefoldin subunits are
short (~150-185 residues) and fell below this particular scan's detection threshold,
not because they aren't real complex members. Added manually since their identity as
canonical prefoldin subunits is unambiguous, unlike the borderline cases above.

---

## Day 6 (prep) · Wu 2018 gene set counts, reconstructed and checked

**Date:** 2026-08-13
**Outcome:** 529 confirmed exactly. 1,704 reconstructs to 1,673 (98% match) — close, not exact, gap unexplained.

Reconstructed both figures directly from `data/raw/wu2018_AdditionalFile2.xlsx`,
following Soo & Van Raamsdonk 2021's own stated method: *"Genes upregulated in
nuo-6 worms in an ATFS-1-dependent manner are genes that are upregulated in nuo-6
mutants but not nuo-6;atfs-1 mutants."*

- ***atfs-1(et15)* ∩ *atfs-1(et17)*, both upregulated: 529 — exact match.** No
  ambiguity in this one; the intersection of the two sheets' `logFC > 0` gene sets
  lands on the published number precisely.
- ***nuo-6* ATFS-1-dependent upregulated (up in *nuo-6*, not up in
  *nuo-6;atfs-1*): 1,673**, against the published 1,704 — a 98% match, not exact.
  Checked for the obvious explanations and ruled them out: no duplicate `ens_gene`
  entries in either sheet, no missing IDs, and the sheets are already filtered to
  FDR < 0.05 with no headroom for an additional threshold to explain the gap. The
  discrepancy (31 genes, 1.8%) is real and unexplained by anything checkable from
  the data alone — most likely a minor difference in Wu et al.'s original processing
  pipeline that isn't fully specified in the microPublication's brief methods text.

**Consequence for Analysis A:** both reconstructed sets are usable. The 529 figure
can be cited as independently confirmed. The 1,673/1,704 figure should be reported
as "reconstructed to within 2% of the published count" rather than presented as an
exact match — an honest gap is more defensible than a silently rounded one.

---

## Day 5 · Analysis C — occupancy vs. output (Claim 2)

**Date:** 2026-08-13
**Outcome:** Primary (condition-matched): 101 of 391 spg-7 ATFS-1-dependent genes are bound (25.8%). Secondary (cross-condition): 29 of 61 regulon genes are bound. Both computed from an independent, validated peak-to-gene assignment, not assumed from Soo's column.

**Method.** Built an operon-aware peak-to-gene assignment from the real WS285
annotation and the lifted GSE63803 peaks (`scripts/analysis_c.ipynb`): a gene counts
as bound if a ChIP peak falls within 2kb of *either* its own TSS or, for downstream
operon members, its operon head's TSS. Validated against the four genes with
independently reconciled ground truth before trusting it further: *hsp-6* bound,
*hsp-60* bound, *dnj-10* not bound, *ymel-1* bound — all four matched.

**A real bug found and fixed during validation, not just noted.** An earlier version
of the assignment rule checked *only* the operon head's TSS for downstream members,
discarding the gene's own TSS entirely. This produced a genuine false negative for
*tspo-1*: a real, close peak (confirmed against the peak's own original MACS
gene-name annotation, `"C41G7.9"` = *tspo-1*) sits almost exactly on *tspo-1*'s own
gene body, but fell 150bp outside the 2kb window once measured only from the operon
head. A sensitivity check across 1kb/2kb/5kb windows and with/without operon logic
is what surfaced this — checking robustness, not just a single cutoff, caught an
error a single-window check would have missed. Fixed by checking both TSS candidates
(union, not override); re-validated clean afterward.

**Primary, condition-matched result.** Nargund 2012's real spg-7(RNAi)
ATFS-1-dependent gene set (Table S3, 391 genes — corrected count, see above) against
the same-condition ChIP peaks: **101 of 391 (25.8%) are ATFS-1-bound.** This is the
comparison the roadmap calls for specifically to avoid the cross-condition confound
(ChIP done under spg-7(RNAi); Soo's regulon ranked under *nuo-6*/*atfs-1(et15,et17)*).

**Secondary, cross-condition result.** The 61-gene regulon against the same binding
calls: **29 of 61 bound**, vs. Soo's own column stating 22 of 61 (which matches the
roadmap's cited anchor number exactly — a good check that the regulon itself is
loaded correctly). All 7 disagreements run the same direction — this pipeline finds
additional bound genes; it never fails to find one Soo's column already calls bound.
One of the 7 is *ymel-1* (already independently confirmed above); the other 6
(`srm-3`, `nhr-115`, `DC2.5`, `F56C11.3`, `clec-265`, `M01F1.4`) are **not yet
individually verified the way *ymel-1* and *tspo-1* were** — flagged as an open item,
not asserted as fact. Do not cite the 29/61 figure as more reliable than 22/61
without doing that check first.

**Chaperone-census cross-check.** Of the 391 condition-matched genes, only 2 are
chaperone-census members: *ymel-1* (bound) and *dnj-10* (not bound) — the identical
two genes that make up the entire "2 of 61" answer in Analysis B. The same trace
representation shows up independently in both the cross-condition regulon and the
condition-matched spg-7 set, which is a coherent cross-validation between Claim 1 and
Claim 2, not a coincidence worth dismissing.

**Fisher's exact test, reported honestly.** Bound-vs-census contingency on the 391
genes: odds ratio 2.89, p=0.45. With only 2 census genes total in the set, this has
essentially no statistical power, the same limitation as Analysis B's rank-sum test.
Not evidence against the pattern, not proof of it either — inconclusive on this
narrow question, same as before.

**Consequence:** the primary, condition-matched result (25.8% bound) is solid and
ready to cite. The secondary cross-condition figure (29/61) needs the remaining 6
gene-level checks before it should be treated as more authoritative than Soo's
published 22/61.

---

## Day 4 · Analysis B — the chaperone/protease census result (Claim 1)

**Date:** 2026-08-12
**Outcome:** 2 of 61 (strict), 5 of 61 (permissive). Matches the roadmap's expected headline exactly.

Cross-referenced the 61-gene ATFS-1 regulon against the frozen 72-gene chaperone/
protease census (`scripts/census.ipynb`). Matched by gene name or sequence name.

**Strict result:** 2 of 61 — `dnj-10` (Score rank 45/61, Score/variability rank
23/61) and `ymel-1` (61/61, 58/61). Independently re-derived, not assumed; the ranks
match the roadmap's pre-recorded values exactly (`dnj-10`: 45, 23; `ymel-1`: 61, 58),
which is a strong cross-check that the census and regulon were both built correctly.

**Permissive result:** 5 of 61. The three borderline genes excluded from the strict
census on functional grounds (`prx-19`, `cbp-3`, `tspo-1` — see the census decision
above) are all actually present in the 61-gene regulon: `prx-19` (rank 54/20),
`cbp-3` (44/57), `tspo-1` (42/21). Again matches the roadmap's pre-recorded `prx-19`
value (54, 20) exactly.

**Statistical check, reported honestly:** a Mann-Whitney U test comparing the ranks
of the 2 strict-census genes against the other 59 regulon genes gives p=0.079
(uncorrected) and p=0.482 (variability-corrected) — not significant at either
threshold. With n=2 this test has essentially no power and should not be presented
as evidence of anything beyond the count itself. Per Part 0 of the roadmap, **the
count is the primary, metric-independent claim; the rank-sum test is a supporting
check, not the headline result.**

**Consequence for Claim 1:** confirmed as stated in the roadmap — folding/QC
machinery is a trace component of the high-confidence ATFS-1 regulon (2 of 61
strict), and the permissive reading (5 of 61) is a materially weaker but still small
fraction. Both numbers should be reported together with the inclusion rule, per the
roadmap's own instruction that a reviewer who disagrees with the strict exclusions
must be able to see exactly what changes.

---

## Day 6 · Analysis A — composition and GO enrichment of the regulon

**Date:** 2026-08-13
**Outcome:** The intersection-artifact hypothesis is rejected. One category reaches
significance (glucuronosyltransferase activity, 17.2×, FDR 0.041). Folding machinery
is **not** depleted relative to the expressed background, which constrains how
Claim 1 can be worded.

`scripts/analysis_a.ipynb`. Inputs: GO annotations (`ref_data/go/wb.gaf.gz`, GOC
release 2026-05-21, 103,606 usable annotations over 12,282 genes after dropping 64
NOT-qualified and 182 ND rows) and the ontology graph (`go-basic.obo`, release
2026-07-26). Annotations are propagated to all ancestor terms over `is_a` and
`part_of`, giving 471,587 gene-term pairs.

**Background.** Genes passing GSE110984's own expression filter (13,837), of which
9,371 carry a GO annotation. Chosen because the regulon and both Wu 2018 lists derive
from that dataset, so this is the pool of genes that could actually have appeared in
them. This is the choice the roadmap flags as the easiest thing for a reviewer to
reject.

**Pipeline validation.** Run against the 72-gene chaperone/protease census, which was
built from Pfam domains with no reference to GO. Recovers `protein folding` at 45 of
62 genes against 0.8 expected (56.7×, FDR 1.6e-71), with `protein refolding`,
`protein folding chaperone` and `heat shock protein binding` following. The notebook
raises if this control fails.

**Result on the 61.** 42 of 61 carry any GO annotation; the 19 that do not cannot
enter the test in either direction, so all counts are out of 42. One term survives
FDR correction: `glucuronosyltransferase activity`, 5 genes against 0.29 expected
(17.2×, FDR 0.041) — phase II detoxification, not proteostasis. Nothing is
significantly depleted. Notably `mitochondrion` itself does not reach significance
(10 genes, 2.86×, FDR 0.57).

**Unannotated fraction — a prior expectation corrected.** 19 of 61 (31%) carry no GO
annotation, against 32% of expressed genes generally. The regulon is *not*
disproportionately uncharacterised on this measure. This is distinct from the 45.9%
carrying no gene *symbol* (see Verified constants): a gene can lack a name and still
carry inferred annotation. An earlier draft of the notebook asserted the two rates
differed; its own output contradicted that, and the text was corrected before commit.

**Intersection-artifact test.** The concern was that the 61 requires induction in
nuo-6, et15 and et17 simultaneously, and that a strict AND could remove real targets
for statistical rather than biological reasons — `hsp-6`, induced in two of the three,
is the known case. If the filter were manufacturing the shortage of chaperones,
representation would fall as the filter tightened. Walking the same category up the
series (all from GSE110984, one background):

| Gene set | conditions | census genes | % | fold | p |
|---|---|---|---|---|---|
| nuo-6 ATFS-1-dependent | 1 | 12 of 1,673 | 0.72% | 1.48 | 0.105 |
| et15 ∩ et17 | 2 | 4 of 529 | 0.76% | 1.56 | 0.253 |
| three-way intersection | 3 | 3 of 231 | 1.30% | 2.68 | 0.101 |
| Soo high-confidence 61 | 3 + further filtering | 2 of 61 | 3.28% | 6.77 | 0.035 |

Representation **rises** monotonically as the filter tightens — the opposite of the
artifact prediction. The scarcity of folding machinery among the 61 is a property of
the ATFS-1 response, not of how Soo's list was assembled. The GO-defined folding
category (9 current terms under `protein folding`, `protein folding chaperone`,
`unfolded protein holdase activity`) moves the same way over the first three sets
(0.74% → 1.53% → 2.48%) and is flat into the fourth (2.38%).

Also recorded here: the three-way intersection is **231** genes, not 61. Soo applied
further filtering beyond the intersection itself. The 61 ⊂ 231 nesting is asserted in
the notebook.

**Consequence for Claim 1 — a real constraint on wording.** Against the expressed
background, 2 of 61 is 6.8× the 0.30 expected by chance. The p-value (0.035) is
uncorrected across the four sets walked; Bonferroni gives 0.141, and at 2 observed
genes one gene either way moves it. So this is a direction, not a significant
finding — but it is emphatically *not* evidence of under-representation. **Claim 1
must be stated in absolute terms ("folding machinery is a trace component of the
output", "2 of 61") and must not be stated as depletion, under-representation, or
"not enriched".** Any of those three phrasings is contradicted by this project's own
analysis and would be the paper's most exposed sentence.

**Background sensitivity.** Repeating the regulon test against all 12,282
GO-annotated genes rather than the 9,371 expressed ones changes the outcome hardly at
all: one term significant either way, `glucuronosyltransferase activity` at FDR 0.041
(expressed) vs 0.039 (genome-wide). The background choice is still reported and
defended, but on this dataset it is not load-bearing — which is a stronger answer to
the anticipated reviewer objection than a procedural one, since it is demonstrated
rather than asserted.

**Two obsolete GO terms, caught and removed.** The first version of the folding
category hand-picked `GO:0051082` (unfolded protein binding) and `GO:0061077`
(chaperone-mediated protein folding). Both are obsolete in the current release —
replaced by `GO:0140309` and `GO:0006457` respectively — and both silently
contributed zero-gene rows that read as genuine absences of signal. The category is
now defined structurally as three current roots plus every descendant, and the
notebook raises if any named root is obsolete.

---

## Day 7 · Analysis D — robustness, and the Gate 2 evidence summary

**Date:** 2026-08-14
**Outcome:** All five robustness checks pass or are explained. One previously-recorded
constant corrected (F22B3.7 WT zero count). Gate 2 framing is closest to the roadmap's
outcome 3, not outcome 1 — a wording decision, laid out here, not made here.

`scripts/analysis_d.ipynb`, 8 cells.

**Column mapping, validated before use.** GSE110984's sample columns (`WT1`, `nuo6_1`,
`atfs1et152`, etc.) don't self-document genotype. The mapping used here was inferred
from naming pattern, cross-checked two ways: group sizes reproduce the replicate
counts the Score formula already implies (12/6/6/3/5/6 = 38, matching the README's
recorded weights), and the `atfs-1` transcript itself drops to 36% and 43% of WT in
the two groups that should carry the deletion allele (`atfs-1(gk3094)` and
`nuo-6;atfs-1`) — the biological signature a real loss-of-function allele should
produce. The notebook raises if either check fails.

**Item 1 — raw-count magnitude check.** The Soo file's percentage columns are already
WT-normalised (column O: *"Raw Expression Data as percentage of wild-type"*), and for
the top-ranked genes that WT baseline is frequently zero — a fold change against zero
is not a real number. Pulled absolute CPM from GSE110984 instead, for the union of the
top 10 genes on each metric (17 genes, since the two rankings mostly disagree — see
Item 2). One gene, **F22B3.7**, is zero in at least half its WT replicates (9 of 12)
and should be reported as *"effectively off in wild type, on at ~13 CPM in nuo-6 and
et15, ~2 CPM in et17"* rather than as a fold ratio, per the roadmap's framing.

**Item 2 — metric sensitivity.** Two numbers long carried as quoted "verified
constants" from the roadmap had never actually been computed from the Soo file in
this repo's own code: genes ranked above *hsp-6* (42 on Score, 28 on Score/variability
— roadmap said 42 and 27–28, both reproduce) and the *isp-1* concordance (below). Rank
correlation between the two metrics across all 61 genes: Spearman ρ=0.42 (p=8e-4) —
positive but far from tight. The top-10 lists by each metric share only 3 of 10 genes.
The census-relevant genes (`dnj-10`, `ymel-1`, and the three permissive-count genes)
all sit in broadly similar territory on both metrics, which is why the census count
itself (2 strict, 5 permissive) doesn't move between metrics even though individual
ranks shift substantially.

**Item 3 — *isp-1* concordance.** Checked directly against Soo's own
`Significantly upregulated in isp-1 worms` column: 57 of 61 "Yes", exceptions
`F49H12.4`, `Y51B9A.9`, `H34I24.2`, `tag-234` — exact match to the recorded figure,
now with a citation to the actual column rather than the roadmap's assertion of it.
Framed per the roadmap as concordance in a second mild-ETC mutant from the same lab
and likely pipeline as *nuo-6*, not independent external validation.

**Item 4 — annotation-depth control.** Analysis A found the regulon's unannotated
fraction (31%) roughly matches all expressed genes (32%) — but that background isn't
matched on expression level, and lowly-annotated genes are known to skew toward
lowly-expressed ones for reasons that have nothing to do with ATFS-1. Repeated the
comparison against an expression-decile-matched background (deciles built from mean
WT CPM). Observed regulon annotation rate: 68.9%. Expected from the matched
background: 61.5%. Binomial test: p=0.29 — no meaningful gap. The unannotated
fraction is a property of this regulon's identity, not an artefact of it skewing
toward obscure, poorly-expressed genes.

**Item 5 — replicate and batch structure.** WT (n=12) is pooled across at least two
batches by naming pattern alone (`WT1`–`WT_9` vs. `WTb`/`WTbl`/`WTr`), consistent with
the GSE110984/GSE93724 split flagged at Gate 1. `nuo-6;atfs-1` (n=3) is both the
thinnest arm and carries a ×3 weight in the Score formula
(`Score = nuo-6% + et15% + et17% − 3×(nuo-6;atfs-1%)`) — disproportionate leverage
from the least-replicated condition. One sentence for Limitations, per the roadmap.

**Correction: F22B3.7 WT zero count.** The README's Verified constants recorded
F22B3.7 as zero in 8 of 12 WT replicates, quoted from the roadmap. Recomputed directly
from both the raw and the normalised/filtered CPM tables (they agree): it is zero in
**9** of 12. Both source files were checked before concluding the previously-recorded
figure, not this one, was wrong. README corrected.

**Gate 2 — evidence, not a verdict.** The roadmap names four possible outcomes and
asks that the framing be fixed today. Evidence assembled from Analyses A–D:

- Census count (B) is stable across metrics: 2/61 strict, 5/61 permissive on both.
- Composition (A) *rises* with looser filtering (61 → 231 → 529 → 1,673) — the
  intersection artefact is rejected, so the scarcity is a property of the
  high-confidence set specifically, not the regulon-construction method.
- Direction (A): 2/61 is 6.8× the expected count against the expressed background,
  not significant either way at this n, but the opposite of depletion.
- Metric sensitivity (D): ρ=0.42, census membership stable, individual ranks not.
- *isp-1* concordance (D): 57/61, same-pipeline caveat attached.

This does not match roadmap outcome 1 (*"folding-poor across all sets, both
metrics"* — it is not folding-poor across all sets, only the most-filtered one) or
outcome 4 (*"well represented throughout"* — 2/61 remains a small absolute fraction).
It is closest to **outcome 3**: folding machinery is present but weak, concentrated in
the highest-confidence tier, not absent — a real dissociation, stated in absolute
rather than depletion terms. Per the roadmap, outcome 3's own instruction is to
retitle rather than force the stronger claim. **This is a wording decision for the
manuscript and has not been made in this notebook or this entry** — brought to the
author separately as the actual Gate 2 checkpoint.

**Gate 2 closed — Outcome 3 confirmed, 2026-08-14.** Reviewed against the evidence
above and locked in: folding/QC machinery is present but weak, and concentrated
specifically in the highest-confidence tier of ATFS-1 targets rather than absent
throughout. The manuscript is written to this claim from Day 8 onward. The working
title and every magnitude claim in Results/Discussion are checked against it
directly — no version of the stronger outcome-1 framing ("folding machinery is
depleted/absent from the ATFS-1 output") goes in the text. Per the roadmap's own
rule for this gate, this framing is not revisited after today except in response to
something found during writing, which gets handled in prose, not by rerunning
analysis.

---

## 2026-08-14 · Pre-freeze audit

**Date:** 2026-08-14
**Outcome:** Every documented number verifies against source data (27 of 27). Three
reproducibility defects found and fixed; one gap found and left open pending a
decision.

Run before freezing the analysis and moving to figures and writing. The point was to
find anything a reviewer or a re-user could find first.

**Clean.** Every tracked data file is genuine — no HTML error pages masquerading as
data, the failure mode this project hit three times earlier. `Context/` has never
been committed in any commit on any branch. No AI attribution exists anywhere in
commit metadata or message bodies. No `try`/`except`/`fillna` anywhere in the
notebooks, so the no-silent-fallbacks rule is enforced in code and not only stated.
No `stepN`-style naming, no banner comments, no TODO/FIXME/debug leftovers.

**Every number independently recomputed.** All 27 figures quoted in the README and
this file were recomputed from the source files by a script that did not reuse any
notebook code: regulon size (61), no-gene-symbol count (28, 45.9%), Soo's bound
column (22), *isp-1* concordance (57 with the same four exceptions), genes above
*hsp-6* (42 / 28), *hsp-6*'s inserted rank (43 and 29 of 62), the five
census-relevant genes' ranks on both metrics, Nargund Table S2/S3 row counts
(685 / 391), liftover counts (1,005 in, 1,005 out, unmapped file empty), census
composition (72 = 65 + 7, no duplicates), and the GAF counts (103,606 usable, 12,282
genes, 64 NOT-qualified and 182 ND dropped). Zero mismatches.

**Liftover spot-checked rather than assumed.** `peaks_ce6.bed` and `peaks_ce11.bed`
are the same length, which would also be true if the "lifted" file were a copy. They
are not: 978 of 1,005 peaks moved, shifts from −6 to 4,612 bp, chromosome names
preserved throughout.

**Defect 1 — three notebooks could not run on a clean clone.** `census.ipynb`,
`analysis_c.ipynb` and `wu2018_verification.ipynb` declared a Jupyter kernel named
`atfs1` that is not registered on this machine and would not exist on anyone else's.
They failed immediately with `NoSuchKernel`. Since the notebooks that had been
re-executed most recently were the ones that worked, this had stayed invisible.
Normalised all six to the standard `python3` kernel.

**Defect 2 — one notebook's outputs came from the wrong interpreter.** `binding.ipynb`
carried outputs generated under Python 3.13 in the `base` environment, not the 3.11
`atfs1` environment the README documents. The stored results were therefore not
produced by the environment the repo tells a reader to use. All six notebooks have
now been re-executed under `atfs1` (Python 3.11.15); provenance is uniform, and every
headline result — 2 of 61, 5 of 61 permissive, 101 of 391, 29 of 61, 57 of 61,
ρ=0.417, 9 of 12, the 529 exact match, the Analysis A validation and 6.8× figure —
is unchanged.

**Defect 3 — the environment was documented but not specified.** There was no
`environment.yml` or `requirements.txt`, so "conda environment `atfs1`" was not
reproducible by anyone else. The README also claimed R 4.5.3, `bedtools` and
`samtools` were part of the environment; none of the three is referenced by any
notebook. Added `environment.yml` pinned to the versions the committed outputs were
produced under, and corrected the README to describe what the analysis actually
needs. Also added a table mapping each notebook to what it produces, and stated
explicitly that the notebooks are independent of one another.

**Gap found and closed — the census is now reproducible.** See the entry below.

---

## 2026-08-14 · Census reconstruction — reproduces exactly, two rule details corrected

**Date:** 2026-08-14
**Outcome:** The frozen 72-gene census reproduces **exactly** from the annotation
file — same 72 WBGene IDs, same 65/7 role split, zero disagreements.
`scripts/census_build.ipynb`.

**Addendum, 2026-08-18.** Further review ahead of building the paper's figures
surfaced two more mislabelled Pfam family names in this notebook's own
`SINGLE_DOMAIN` dict: `PF01434` was labelled `"FtsH_AAA"` and `PF00574` was labelled
`"ClpP"` — both plausible mnemonics, neither the real family name in this annotation
release. Checked directly against the raw file: PF01434 is
`Peptidase_M41` (`ymel-1`'s domain), PF00574 is `CLP_protease` (`clpp-1`'s domain).
The original exact-match check did not catch either, because it compared gene
membership and role assignment only, not the domain-name text — a real gap in the
check itself, not only in the labels. Both are now fixed, and the check now also
compares `pfam_families` text exactly (including the two prefoldin manual-addition
entries' explanatory text), so a labelling drift like this cannot pass silently
again. Re-executed; the census still reproduces exactly, now on all three axes.

The audit above found the census was consumed by three notebooks but built by none.
It had entered as a finished CSV, so its documented method could not be checked
against code. Reconstructing it was worth doing properly rather than documenting as a
limitation: had the rule failed to reproduce, that needed finding before submission,
not after.

The notebook **verifies** rather than regenerates. It rebuilds the census from
`c_elegans.PRJNA13758.WS285.protein_annotation.gff3.gz` and raises if the result
differs from the frozen CSV in membership or role. It never writes to the CSV. If a
future WormBase release changes a domain call, this fails loudly instead of quietly
moving the number the paper reports.

**Two details in the original write-up were imprecise, and both mattered.**

*Lon requires both domains, not either.* The rule was recorded as "Lon protease
(PF05362 + PF02190)". Read as "either domain", five extra genes qualify on a lone
Lon_C hit. `lonp-1` and `lonp-2` both carry Lon_C **and** LON_substr_bdg, so the "+"
means conjunction. Requiring both also removes `lido-17` automatically — it had only
ever qualified through a lone Lon_C hit — which means the three documented manual
exclusions are really two (`ppk-3`, `rme-8`) plus one that the corrected domain rule
handles on its own. The notebook keeps `lido-17` in the exclusion list and asserts
that it never has to fire.

*The signal-peptide screen is per-protein, not per-gene.* The original entry said
genes were excluded where a signal peptide is "present", which is ambiguous for
multi-isoform genes, and both readings are wrong:

- Exclude if *any* isoform has a peptide → wrongly drops `F11F1.1`. Its peptide is on
  isoform `c`, which carries DUF148 and no chaperone domain; the HSP70 domain sits on
  isoforms `a` and `b`, neither of which has a peptide.
- Exclude only if *every* domain-bearing isoform has one → wrongly keeps `hsp-3`,
  `hsp-4`, `enpl-1`. Each has a short isoform lacking the peptide purely because it
  starts downstream of it. These are genuine ER chaperones.

The rule that reproduces the frozen file, and is the biologically correct question,
is: **exclude a gene when a signal peptide and a qualifying domain co-occur on the
same protein.** That yields exactly the 13 ER exclusions the original entry
enumerated — `hsp-3`, `hsp-4`, `enpl-1`, `stc-1`, six DnaJ co-chaperones, and three
unnamed genes, now identified as `F54F2.9`, `T14G8.3`, `T24H7.2`.

**Arithmetic in the original entry, corrected.** It stated 83 domain-based
candidates. The real figure is **85**, and the chain is 85 − 13 ER = 72, − 2 manual
= 70, + 2 prefoldins = 72. The previously recorded numbers did not sum to 72 (83 − 13
− 3 + 2 = 69); the discrepancy was in the write-up, not the census, which is the
outcome the reconstruction was run to distinguish between.

**Independently confirmed by the rebuild:** all four prefoldin subunits that match
automatically plus `pfd-3`/`pfd-5` added manually give the complete six-subunit
complex; the manual-addition step raises if either ever starts matching on its own,
so the exception cannot go stale unnoticed. Named sanity-check genes (`hsp-6`,
`hsp-60`, `dnj-10`, `ymel-1`, `spg-7`, `clpp-1`, `cct-1`, `hsp-90`) all present. The
roadmap's three borderline genes (`prx-19`, `cbp-3`, `tspo-1`) all correctly absent
on domain evidence, which is what makes the permissive count a functional argument
rather than a domain one.

**Consequence:** no change to any result. The census is the same 72 genes it has been
since it was frozen, Analysis B still reports 2 of 61, and the paper's Data
Availability statement can now claim full reproducibility from public accessions
without qualification.

---

## 2026-08-18 · Table S2 — functional category for all 61 regulon genes

**Date:** 2026-08-18
**Outcome:** All 61 genes categorised: 2 Folding/QC, 8 Xenobiotic detoxification, 4
Innate immunity, 19 Uncharacterised (no GO annotation), 28 Other annotated function.
`scripts/table_s2.ipynb`, writing `results/regulon_61.csv` and
`results/table_s2_regulon_annotation.csv`.

This closes the one real gap the pre-freeze audit left open: only the two anchor
genes had ever been annotated, and Figure 1C (what the regulon is, not only what it
isn't) needs a category per gene. Categories are the ones the roadmap's Part 0
already commits to in prose — *"the bulk of the regulon is xenobiotic
detoxification, innate immunity, and functionally uncharacterised genes"* — not a
new taxonomy invented for this table. Built from the same GO annotation file and
ancestor-propagation pipeline Analysis A already validated, applied to two more
category roots instead of only the folding one. Folding/QC status is the frozen
census, reused rather than re-derived.

**The validation check caught a real gap before it became a wrong figure.** A first
pass defined "xenobiotic" only from the biological-process terms (`GO:0006805`,
`GO:0009410`) and put 4 known xenobiotic genes in as a check — `cyp-14A1`,
`cyp-33C8`, `cyp-14A4`, `ugt-19`, three of them among the regulon's top-ranked genes.
Only 1 passed. The other three carry solely the molecular-function activity terms —
monooxygenase activity, UDP-glycosyltransferase / glucuronosyltransferase activity —
without a formal link to the xenobiotic *process* term in this GO release. Those
activities are literally the textbook Phase I (cytochrome P450) and Phase II (UGT)
xenobiotic-metabolising enzyme families, and adding them is consistent with, not
independent of, Analysis A's own finding that glucuronosyltransferase activity is
the one GO term significantly enriched in this regulon (FDR 0.041) — the same
biology surfacing twice, not two different claims. Checked before adding: each term
covers 72–89 genes genome-wide, not a broad catch-all. After the fix, all 8 genes in
the category are real `cyp-*`/`ugt-*` family members and nothing else — inspected by
hand, not just asserted.

**Cross-checks against numbers already established elsewhere, not re-derived:**
Folding/QC = 2 (Analysis B's strict count, exact). No-symbol count = 28 of 61
(45.9%, matches the README exactly). Uncharacterised-by-annotation = 19 of 61 —
independently matches Analysis D's annotation-depth control (which found 19 of 61
carry no GO annotation) without having been built to target that number.

**Explicitly not merged, on purpose:** "no gene symbol" (28) and "no GO annotation"
(19) are different axes — only 13 genes are both. A gene can lack a public name and
still carry real inferred annotation (`Analysis D`'s annotation-depth control already
established the two rates aren't the same). Figure 1C must show them as what they
are, not collapse them into one bar.

---

## 2026-08-19 · Figure 1 — composition (Claim 1)

**Date:** 2026-08-19 · **panels merged into one file 2026-08-20**
**Outcome:** Built and visually verified. Three panels — A: Score/variability,
B: Score, C: category breakdown — in `figures/figure1_composition.{pdf,svg,png}`.
`scripts/figure_1.ipynb`. Panels A/B and panel C were originally written to two
separate files; they were merged during the pre-commit pass, since a reviewer
expects "Figure 1" to arrive as one image rather than as parts to be assembled.

Reads only from `results/regulon_61.csv` and `results/reference_genes.csv` — no
recomputation, and every plotted number is re-asserted against the recorded figures
in this log before the notebook draws anything (`dnj-10` 45/23, `ymel-1` 61/58,
`hsp-6` inserted 43/29, strict census n=2, permissive-only n=3). If any of these
were ever stale, the notebook raises instead of producing a plausible-looking wrong
figure.

Panels A/B: dual-metric rank plot per the standing rule, Score/variability first as
the conservative metric. Score's range (68–218,882) needed a log y-axis; Score/
variability's (5.4–37.7) did not. Panel C: category composition from
`table_s2.ipynb`, folding/QC placed last so the paper's central comparison sits at
the visual anchor rather than buried in the middle. "No gene symbol" (28 of 61)
deliberately excluded as a bar segment — it overlaps the functional categories
rather than partitioning the same 61 genes a second, incompatible way — and is
reported as a separate annotation instead.

**Two real layout defects caught by actually looking at the rendered image, not just
executing without error.** First pass: panel C's x-axis label overlapped the legend
text directly — visually confirmed on the first render. Second pass, overcorrecting
the fix: the bar shrank to an illegible sliver and the panel label collided with the
axis. Fixed by moving to explicit axes positioning (`fig.add_axes`) instead of
fighting `tight_layout`'s interaction with a side-mounted legend. Re-rendered and
re-inspected before accepting. A figure that executes without a Python error is not
the same thing as a figure that is correct — both defects would have passed a
"does the code run" check.

A full pass over the repo found two recurring failure modes. Both are process
problems, not one-off mistakes, and both had already produced conclusions that reached
this log.

**Fabricated results from silent fallbacks.** Three cells reported findings their code
never computed: the *hsp-6* lookup (`except FileNotFoundError` → hardcoded `True`), the
operon check (`except Exception` → hardcoded "not in an operon"), and the dataset
overlap (hardcoded quote printed as "Confirmed"). Of the three, one was wrong, one was
unsupported, and one happened to be right. All are fixed; failures now raise, and
facts retrieved by hand are recorded as dated citations rather than dressed up as
computation.

**Silently-failed downloads saved as data.** Three files were HTML error pages carrying
data extensions: `data/soo_dataset_s1.csv` (CaltechDATA 404, unused — deleted),
`data/raw/c_elegans...gff3.gz` and `ref_data/c_elegans...geneIDs.txt.gz` (both 404s;
the README listed them as WormBase annotations). WormBase refuses scripted downloads,
which is how the error pages were written to disk. Both were re-fetched from the EBI
WormBase mirror and verified as real gzip archives.

**Standing rule:** verify that a download is what it claims to be before recording it
as acquired. Check the file type, not just that a file exists.

---

## 2026-08-19 · Table 1 — the five census-relevant genes

Built `scripts/table_1.ipynb` (Day 8): the two strict chaperone/protease census
members found in the regulon (`dnj-10`, `ymel-1`) plus the three borderline genes
the census decision named and checked but excluded on domain grounds (`prx-19`,
`cbp-3`, `tspo-1`). Reads ranks, scores, and Soo's published binding column from
`results/regulon_61.csv`; everything else is re-derived and validated rather than
carried over from prose.

**Domain text for the three borderline genes, read directly off the annotation
file** rather than typed from memory, the same discipline that caught the
`FtsH_AAA`/`Peptidase_M41` naming error in the census rebuild: `prx-19` →
`PF04614 (Pex19)`, `cbp-3` → `PF02135 (zf-TAZ)`, `tspo-1` → `PF03073 (TspO_MBR)`.
Exact match to the census decision's prose description of all three.

**Binding reported as three separate columns, not collapsed into one**, per the
standing rule that binding calls should never be merged when they can disagree:
Soo's own published ChIP column, Nargund 2015's independently deposited bound-gene
list, and this project's own operon-aware peak-to-gene reassignment (the same 2kb,
own-or-operon-head-TSS method from Analysis C, re-derived here and re-validated
against the same four known-true genes — `hsp-6`, `hsp-60`, `dnj-10`, `ymel-1` —
before anything downstream trusted it). Nargund 2015 and this-study binding had
only been checked for `dnj-10`/`ymel-1` before now; the three borderline genes
needed the same lookup run for the first time, using the identical, already-
validated method.

**Result: all three sources agree on 4 of 5 genes.** The one disagreement is
`ymel-1` — published column says no, both Nargund 2015 and this-study say yes —
which is the same reconciled case already on record above ("Binding Reconciliation
Decision, corrected"), not a new discrepancy. Wrote `results/table_1.csv` and
`tables/table_1.csv`.

---

## 2026-08-19 · Figure 2 — occupancy vs. output (Claim 2)

Built `scripts/figure_2.ipynb`: all 7 census-relevant genes (both reference genes
plus the 5 from Table 1), each shown as a promoter-window occupancy track (peaks,
gene model, TSS) paired with its induction rank on both metrics. Re-derives peak
positions, fold-enrichment, and bound calls from the raw ChIP data and WS285
annotation the same way `table_1.ipynb` does, and re-validates against the same
known-true values (the four independently reconciled genes, plus the exact
*ymel-1* peak fold-enrichment/FDR and the *tspo-1* own-TSS-vs-operon-head-TSS
distances already on record above) before drawing.

**Real layout defects caught only by cropping and zooming into the rendered PNG,
not the full-figure thumbnail** — the same lesson as Figure 1, one level deeper.
*ymel-1*'s operon-head-TSS marker sat just outside the first draft's ±10kb display
window and its label bled into the row above; widened to ±12kb. Two peaks inside
the display window belong to neighbouring genes by MACS's own gene-name
assignment (*hsp-6*'s window shows a second peak actually called for *C37H5.6*;
*ymel-1*'s window shows one actually called for *M03C11.3*) — both are real,
correctly-positioned peaks, but showing them unlabelled would read as extra hits on
the row's own gene. Now annotated with their real MACS gene name. A two-line
"operon head TSS" label overflowed past its own row's bottom axis spine and was cut
by it on both rows that use it (*ymel-1*, *tspo-1*) — visible only after cropping
each row individually, not in the assembled figure. Fixed by shortening to one
line and moving the anchor point. All three defects were real regardless of
whether they were visually obvious at full-figure scale.

**Reading the result:** occupancy and output track together at the strong end
(*hsp-6*, bound at 11.8×, rank 29/43) and diverge sharply at the weak end
(*hsp-60*, bound at 3.8× yet rank 62/62 — the weakest gene in the entire regulon
despite carrying a called peak). The two strict census genes split the same way:
*dnj-10* is unbound but ranks 23/45, *ymel-1* is bound at 13.1× but ranks 58/61.
Binding does not predict induction strength among these 7 genes, which is the
occupancy-side complement to the composition finding in Figure 1.

---

## 2026-08-19 · Figure 3 — the filtering-series test (Claim 3)

Built `scripts/figure_3.ipynb`: the intersection-artifact test from Analysis A,
re-derived independently (GO ontology and annotation parsing, the four nested
gene sets, the structurally-defined folding-related GO category, both walk
tables) rather than read from a stored intermediate, and validated against the
exact percentages already on record — 0.72→0.76→1.30→3.28% (Pfam census) and
0.74→1.53→2.48→2.38% (GO folding-related) — before drawing. Two panels: percent
representation and fold-vs-expected, both across the same four filter stages
(1,673 → 529 → 231 → 61 genes).

**One layout defect caught by inspecting the rendered image**: the "3/231"
sample-size label at the third point sat directly on the line segment rising
steeply into the fourth point, legible only by looking closely. Moved
below-left of its marker instead of the default upper-right used at the other
three points.

**What the figure shows:** the artifact hypothesis predicts falling
representation as the AND filter tightens. Neither metric falls — the Pfam
census rises monotonically and finishes 6.8× expected at the strict end; the
GO-based category moves within noise (0.74→2.48%) rather than either rising
cleanly or falling. Both readings reject the artifact hypothesis; only the
census reading supports a positive claim about the 61, and it is captioned with
its own uncorrected p-value rather than presented as settled.

---

## 2026-08-19 · Figure 4 — robustness

Built `scripts/figure_4.ipynb`: three of Analysis D's five robustness checks,
re-derived independently and validated against the exact recorded values before
drawing (the full metric-sensitivity scatter is reserved for Figure S2, not
repeated here). Panel A: expression-matched annotation-depth control (observed
68.9% vs. expected 61.5%, p=0.292 — no gap once expression level is controlled
for). Panel B: *isp-1* concordance (57 of 61, four named exceptions, captioned
as same-lab/same-pipeline concordance rather than independent validation).
Panel C: absolute CPM for the union of top-10 genes on either ranking metric
(17 genes), flagging *F22B3.7* by name — 9 of 12 WT replicates are exactly
zero, so a fold-change reading for that gene is undefined rather than merely
large.

**Two text-collision defects in Panel B, both caught only by inspecting the
rendered image.** First draft: the exceptions list and the italic caption both
sat near the top of the axes and overlapped. Second draft, after separating
them: still collided in the same region because the fix moved position without
increasing the vertical gap. Resolved by merging the exceptions list and the
"N of 61" count into a single text block placed once, well clear of both the
bar and the caption — the same lesson as Figures 1–3, that a fix has to be
re-inspected rather than assumed to have worked.

---

## 2026-08-19 · Table S1 — full 72-gene census

Built `scripts/table_s1.ipynb`: the complete chaperone/protease census as a
supplementary table, with the inclusion rule written out in full and a flag for
which of the 72 also appear in the 61-gene high-confidence regulon. Re-runs the
independent reproduction from the raw annotation file (the same check
`census_build.ipynb` performs) before formatting rather than trusting the
frozen CSV on its own, and confirms the regulon-membership flag lands on
exactly `dnj-10` and `ymel-1` — the same fact Analysis B already established,
now visible from the census's side rather than the regulon's side. Wrote
`results/table_s1_census.csv`, `tables/table_s1_census.csv`, and
`tables/table_s1_census_note.txt` (the inclusion-rule text for the caption).

---

## 2026-08-19 · Figure S2 — metric sensitivity

Built `scripts/figure_s2.ipynb`: the full Score-vs-Score/variability rank-rank
scatter for all 61 regulon genes, deliberately deferred out of Figure 4 to keep
that figure to a single-page summary. Re-derives both rankings from the source
file and validates the Spearman correlation (rho=0.417) and top-10 overlap (3
of 10) against Analysis D's recorded numbers before drawing. Points are
coloured by top-10-list membership under either metric; the five
census-relevant genes are outlined and labelled.

**One label-collision defect caught by inspecting the rendered image**:
*dnj-10* and *tspo-1* sit only 2 ranks apart on each axis, and the default
upper-right label offset put *tspo-1*'s text directly on *dnj-10*'s marker.
Moved *tspo-1*'s label below-left; the other four census labels kept their
default placement, which had clear space around them already.

---

## 2026-08-19 · Figure S1 — pipeline validation

Built `scripts/figure_s1.ipynb`: the GO enrichment pipeline's positive control,
re-derived independently and validated against the exact recorded numbers
before drawing. The 72-gene Pfam census (built from protein domains, with no
reference to GO at any point) against the expressed background recovers
"protein folding" as the single most significant enriched term — 45 of 62
annotated census genes, 57× expected, FDR = 1.55e-71 — which is what
establishes that the pipeline used for the regulon (Analysis A) and the
filtering series (Figure 3) actually works, rather than assuming it does. Top
8 enriched terms shown; no layout defects on this one.

---

## 2026-08-19 · Figure S3 — peak-assignment window sensitivity

Built `scripts/figure_s3.ipynb`: the binding-window and operon-logic sweep
that the earlier binding-reconciliation note ("Binding Reconciliation
Decision, corrected") only ever described qualitatively — "a sensitivity
check across 1kb/2kb/5kb windows... is what surfaced this" — without the
numbers themselves being run end-to-end and recorded anywhere. This notebook
is that sweep, actually executed: 6 window sizes (0.5–10kb) × with/without
operon logic, against the primary condition-matched set (391 Table S3 genes),
using the identical peak-assignment method as `analysis_c.ipynb` /
`table_1.ipynb` / `figure_2.ipynb`. The reported headline (101 of 391, 25.8%
at 2kb with operon logic) reproduces exactly.

A first version scanned every gene against every peak per sweep point (fine
for the single number `analysis_c.ipynb` needed, far too slow for 12 sweep
points — it did not finish in two minutes and was killed). Rewritten with
per-chromosome sorted TSS arrays and binary search instead of a linear scan;
same rule, same answer at 2kb, ~75 seconds for the full sweep.

**What it shows:** operon logic only ever adds genes, never removes them
(the blue "own-or-head" line sits at or above the grey "own-TSS-only" line at
every window), consistent with it being a genuine recovery of otherwise-missed
binding rather than a free parameter that could cut either way. The reported
2kb choice sits in the flatter part of the curve (≈20–26% across 0.5–3kb)
rather than at a spike — the percentage only climbs steeply past 5kb, where a
window this wide starts plausibly picking up unrelated neighbouring genes
rather than real regulatory proximity.

---

## 2026-08-20 · Pre-commit pass over the figures

**Date:** 2026-08-20
**Outcome:** Every figure re-rendered on a shared house style; six presentation
defects found and fixed, one of them a misspelt gene name. No number changed.

Run before committing the figure work. All seven figure notebooks and both table
notebooks were re-executed from scratch; every validation assertion in them still
passes against the frozen inputs, so nothing in this pass touched a result.

**House style.** `scripts/figure_style.py` now sets the conventions this literature
actually uses — left and bottom axes only, outward ticks, frameless legends inside
the panel, bold letters at the panel corner — on a 9pt base rather than 8pt. The
Wong colour-blind-safe palette is unchanged; the point was to stop the panels
reading as generic plotting-library output next to published UPRmt figures, not to
restate the colour decision.

**Defects found by looking at the renders, one per figure that had one:**

- *Figure 1* — on the Score ranking, *dnj-10*'s marker sat on top of the *hsp-6*
  label and covered its first letter, so the label read "nsp-6". A misspelt gene
  name is the worst class of defect here: it is silently wrong, and it is wrong in
  the one direction a reader will not question. Label moved to the other side.
- *Figure 2* — three. The legend advertised an orange "peak present, not called
  bound" class that is never drawn, because every gene in the panel that has a peak
  at all is also called bound; the legend is now built from what was actually
  drawn. Every row carried a bare bottom axis line, six of which read as table
  borders; only the bottom row keeps its axis now. Blue meant "ATFS-1 peak" in
  panel A and "Score/variability rank" in panel B — two unrelated meanings for one
  colour in one figure — so panel B moved to ink/grey. The operon-head marker is
  identified in the legend rather than labelled per row, having had nowhere to sit
  that did not collide with either the row axis or the peak labels.
- *Figure 3* — the fold-change axis was printing matplotlib's "6 x 10^0" form.
  Replaced with plain numbers.
- *Figure 4* — the panel B caption ran into the y-axis tick labels and the panel C
  title ran into panel A's tick labels, both consequences of the larger base font.
  Re-laid out.
- *Figure S1* — the GO namespace was being truncated to its first two characters,
  giving "(bi)" and "(mo)". These are now the conventional BP/MF, and the notebook
  raises on any namespace it has no abbreviation for rather than inventing one.
- *Figure S3* — the "Reported" annotation overlapped the own-TSS-only line. Moved.
- *Figure S2* — legend read "var only"/"score only", working shorthand that should
  not have reached a finished figure. Spelled out.

The pattern is the same one this log has recorded since Figure 1: these all
executed without a Python error, and none of them would have been caught by
re-running the notebook. They were found by cropping into the rendered PNG and
looking at it.

**Two further defects that the image would never have shown.**

*A `fillna` in Figure 1*, the one violation of this repo's no-silent-fallbacks
rule anywhere in the notebooks. `value_counts().reindex(CATEGORY_ORDER).fillna(0)`
turns a category renamed upstream in `table_s2.ipynb` into a zero-height bar
rather than an error. Replaced with an explicit check that the categories on both
sides match, which raises and names the difference.

*Figure 1's page was 185mm wide, over the journal's 180mm maximum.* The panels
span the whole canvas, so `savefig`'s tight bounding box plus its padding pushed
the page past the limit — and nothing in the image looks wrong when it happens.
Panel C's side legend was the original overhang; narrowing that panel and trimming
the canvas to 0.98 x the full width brings it to 177mm. All seven figures were
then checked by reading the `/MediaBox` out of each PDF directly: widest is now
177.1mm, tallest 164.9mm, all within 180 x 210mm, all with Arial embedded as
TrueType so the text stays editable.

**Verification.** All 17 notebooks re-executed end to end and every assertion in
them passes. Separately, 19 headline numbers were recomputed from the source
files by a script sharing no code with the notebooks — regulon size, Soo's bound
column, *isp-1* concordance, all five census-relevant gene ranks on both metrics,
genes above *hsp-6* on both metrics, census size and role split, census
membership in the regulon, and the row counts and column structure of all three
tables. 19 of 19 match.

**A reproducibility defect found by re-running, not by reading.** Re-executing
`analysis_a.ipynb` from unchanged source produced a different file. The cause is
benign but worth fixing: four GO terms carry byte-identical statistics (k=2,
expected 0.049, 40.6x, p=0.41), and `sort_values("p_enrich")` left their relative
order to fall out of set iteration, which varies with Python's per-process hash
seed. Ties are now broken on `go_id` in `analysis_a.ipynb` and `figure_s1.ipynb`.
This is a display-order change only — the tied rows are identical in every
reported column, and every headline number from Analysis A is unchanged
(glucuronosyltransferase 17.2x / FDR 0.041; the 0.72 -> 3.28% filtering series;
2 of 61 at 6.8x, uncorrected p=0.0352, Bonferroni 0.141). Confirmed by running
the notebook twice and diffing: byte-identical.

This does not reopen the Gate 2 freeze. No statistic was recomputed and no value
moved; a sort key was made deterministic so that re-running the repository
returns the same file, which is the property the freeze exists to protect.

`analysis_c.ipynb` also showed a diff on re-execution. That one is not a defect:
the identical text was split across two stream outputs instead of three by
Jupyter's output buffering. Checked and left alone.

---

## 2026-08-21 · Table PDFs

**Date:** 2026-08-21
**Outcome:** All three tables (Table 1, Table S1, Table S2) now export as
manuscript-ready PDFs alongside their CSVs, on the same journal spec and font as
the figures. Two real defects fixed before accepting the output.

Added `scripts/table_style.py`: a plain three-line table renderer (rule above the
header, rule under it, rule at the foot, no vertical gridlines, no shading) that
paginates by measured height so nothing runs off a page, and repeats the header
on every page of a multi-page table. `table_1.ipynb`, `table_s1.ipynb`, and
`table_s2.ipynb` each gained a final cell calling it; no existing cell in any of
the three was touched except to sort rows for display (below), so nothing
upstream of the CSV output changed.

**First defect: character-count wrapping does not track rendered width.** A
first version of `table_style.py` decided line wraps from a guessed
characters-per-line number, on the assumption that a domain string like
"PF03073 (TspO_MBR)" (19 characters) was short enough to leave on one line. It
was not, at 8pt Arial, in that column's width - it overflowed into the next
column, invisible until the rendered PDF was actually opened. The multi-line
column headers had the same problem the other way: three lines of header text
were given a fixed, too-small height allowance, so the third line printed on top
of the header rule and the first data row. Rewritten to measure real glyph width
with a throwaway figure and renderer before laying out any page, and to size the
header band from however many lines the headers actually need rather than a
guess. Both defects were caught by opening the rendered PDF, not by the code
running without error.

**Second defect: gene names were sorted as plain strings.** `dnj-10` sorted
before `dnj-2`, because `"dnj-10" < "dnj-2"` character-by-character. Fixed with a
natural-sort key (digit runs zero-padded before comparison, then discarded) in
`table_s1.ipynb`; confirmed the fix by reading the rendered page rather than
trusting the sort call. `hsp-16.2` correctly sorts before `hsp-16.11` under this
key, which is the right semantics here — these are sequential subunit numbers,
not decimal fractions.

**Display sorting, applied only to the human-facing `tables/` copy, never to the
`results/` copy other notebooks read from:**
- Table 1: strict-census genes first (the headline 2), then permissive-only,
  each group by Score/variability rank ascending.
- Table S1: chaperones before proteases (65/7, the majority-first framing used
  throughout), then natural gene-name order within each role.
- Table S2: functional category (Folding/QC first, matching Figure 1's anchor
  placement), then Score/variability rank within category.

**Verification.** All three CSVs re-checked against their known row/column
counts (5/9, 72/6, 61/8) after sorting - membership and every value are
unchanged, only row order differs from the `results/` copies. `results/regulon_61.csv`
and `results/reference_genes.csv` (written by `table_s2.ipynb`, read by every
figure notebook) confirmed byte-identical by MD5 before and after this change.
All 17 notebooks re-executed end to end afterward; every assertion still passes.
Page sizes read from each PDF's own `/MediaBox`: widest 159mm, tallest 196mm,
both within the 180 x 210mm limit.
