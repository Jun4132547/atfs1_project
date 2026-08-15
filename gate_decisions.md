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

## 2026-08-11 · Data integrity audit

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
