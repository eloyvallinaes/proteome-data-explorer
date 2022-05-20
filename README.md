# Proteome physicochemical properties across cellular organisms

As a complement to our paper [_Physicochemical classification of organisms_](https://doi.org/10.1073/pnas.2122957119), this website was built as a tool for any reader to directly explore the data, much in the same way as I did during the study.

The underlying data in `csv` format can be found under the `Downloads` tab.

## Scope
### Datasets of cellular organisms
- UniProt Proteomes (n=10,052).
- NCBI Assembly (n=17,879).

### Features
Each takes a value along the following eleven dimensions. In general, these values
refer to the average over all proteins in a proteome, while the corresponding
median values can be found under the `Downloads` tab.

| Name | Symbol | Comment |
|------|--------|---------|
| Protein length | $l_{sequence}$ | number of residues in protein |
| Protein count  | $n_{genes}$ | number of proteins in the proteome|
| Protein size  | $MW$ | the typical molecular weight of proteins in a proteome, in kDa.|
| Solvent-accessible surface area | $SASA$ | an approximation obtained with Miller's empirical formula: $SASA = 6.3 \cdot MW^{0.73}$; in Å<sup>2</sup>. |
| Fraction positive | $f_{positive}$ | $(n_R + n_K) / l_{sequence}$ |
| Fraction negative | $f_{negative}$ | $(n_D + n_E) / l_{sequence}$ |
| Charged residue fraction | $f_{charged}$ | $(n_D + n_E + n_R + n_K) / l_{sequence}$ |
| Fraction hydrophobic | $f_{hydrophobic}$ | $(n_F + n_L + n_I + n_V) / l_{sequence}$ |
| Net charge | $charge_{net}$ | difference between counts of basic (KR) and acidic (DE) residues: $(n_R + n_K) - (n_D + n_E)$.
| Net charge density | $NCD$ | net charge over SASA: $\frac{charge_{net}}{SASA}$
| GC content | $GC%$ | genome-wide percentage of guanidine and cytosine nitrogenous bases|




## Technical notes
Backend was developed in Django3.7.

Frontend relies on a single `main.js` and Bootstrap4.0 utilities.

Deployed to Heroku on September 2021.

### Updates
- May 2022:
    - bug fixes
    - data under _Downloads_
    - _About_
    - link to publication
