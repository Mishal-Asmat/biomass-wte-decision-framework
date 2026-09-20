# Biomass Waste-to-Energy (WtE) Decision Framework

A reproducible data-science pipeline that converts the laboratory databse of biomass or waste
fuel into an interpretable and defensible **conversion
technology recommendation** (combustion, gasification, or pyrolysis) for
each sample by combining unsupervised fuel-typology clustering with
literature based thermochemical process-suitability rules.

It is built on 135 characterized Australian biomass and waste fuel samples
(proximate/ultimate analysis, higher heating value, and ash-mineral
composition). It handles three questions:

1. **What *is* this fuel?** : data-driven fuel typology via unsupervised clustering, independent of `Biomass_Type` labels.
2. **What *can* this fuel do?** : literature based thermochemical process-suitability analysis (VM/FC/Ash/moisture/alkali thresholds).
3. **What *should* be build?** : a hybrid decision layer combining (1) as cluter-only and (2) as rule-only baselines, and a full disagreement/interpretability analysis of where and why the frameworks disagree.

---

## Table of contents
- [Biomass Waste-to-Energy (WtE) Decision Framework](#biomass-waste-to-energy-wte-decision-framework)
  - [Table of contents](#table-of-contents)
  - [Pipeline overview](#pipeline-overview)
  - [Repository structure](#repository-structure)
  - [Key results](#key-results)
  - [Getting started](#getting-started)
  - [Reproducing the pipeline](#reproducing-the-pipeline)
  - [Interactive dashboard](#interactive-dashboard)
  - [Testing](#testing)
  - [Methodology notes \& corrections](#methodology-notes--corrections)
  - [License](#license)
  - [Citation](#citation)

---

## Pipeline overview

| Phase | Notebook | Question | Key output |
|---|---|---|---|
| 1 | `01_data_audit.ipynb` | Is the raw dataset complete and well arranged? | `data/interim/validated_data.csv` |
| 2 | `02_basis_harmonization.ipynb` | Which analytical basis out of all best represents intrinsic fuel chemistry? | `data/interim/harmonized_db_basis.csv` (dry basis) |
| 3 | `03_feature_engineering.ipynb` | Which indices explains reactivity, energy intensity, and ash risk? | `data/interim/engineered_features.csv` |
| 4 | `04_clustering_analysis.ipynb` | Do fuels separate into physically meaningful clusters? | KMeans fuel type (k = 3) |
| 4A | `04a_process_suitability.ipynb` | Which processes are chemically/physically feasible for each sample? | Primary/Secondary process + constraint level |
| 4B | `04b_cluster_explainability.ipynb` | Which properties drive the cluster separation? | Random Forest feature importance |
| 4C | `04c_wte_conversion_decision.ipynb` | Combines typology + process suitability rules, which technology is best to apply? | `data/processed/wte_final_decisions.csv` |
| 5 | `05_decision_comparison.ipynb` | How much weightage does clustering actually add vs. the weightage of rules alone? | `data/processed/comparison_decisions.csv` |
| 6 | `06_decision_interpretability.ipynb` | Where and why do the three frameworks disagree? | `data/processed/disagreement_analysis.csv` |

## Repository structure

```
biomass-wte-decision-framework/
├── app/
│   └──app.py                    # Streamlit dashboard 
├── data/
│   ├── raw/                     # original fuel database
│   ├── interim/                 # validated → dry-basis harmonized → engineered
│   ├── processed/               # clustering-ready + final decision tables
│   └── metadata/                # variable-categorization & basis-selection trials
├── notebooks/                   
├── src/
│   ├── config/                  # thresholds & column-grouping
│   ├── data/                    # load / validate / harmonize basis
│   ├── features/                # engineered fuel-quality + ash-risk indicators
│   ├── clustering/               # scaling, KMeans, k-selection, label canonicalization
│   ├── models/                  # process-suitability & conversion-technology decision rules
│   ├── analysis/                # cluster explainability, disagreement analysis, feature diagnostics
│   └── visualization/           
├── results/
│   ├── tables/                  
│   └── figures/                
├── tests/                       # pytest unit tests for src/
├── pyproject.toml               # pytest config
├── requirements.txt
├── .gitignore
├── LICENSE
├── CITATION.cff
└── README.md
```

## Key results

- **Fuel typology (k = 3, silhouette ≈ 0.62):**

  | Cluster | Regime | CV (MJ/kg, db) | VM (%, db) | Ash (%, db) | Best suited Technology |
  |---|---|---|---|---|---|
  | 0 | Ultra-high-energy, volatile-rich | ≈40.6 | ≈97.8 | ≈1.3 | Gasification / combustion |
  | 1 | Balanced, conversion-ready (major class) | ≈19.5 | ≈80.6 | ≈2.7 | Pyrolysis / combustion |
  | 2 | Low-energy, ash-constrained | ≈12.9 | ≈52.9 | ≈35.4 | Gasification / pre-treatment |

- **Distribution of final _hybrid technology_** (135 samples): with Pyrolysis (111),
  Further Assessment Needed (17), Gasification (6), Combustion (1).

- **Agreement (%) among frameworks:** cluster-only vs. rule-only (90.4%), rule-only vs.
  hybrid (85.2%), cluster-only vs. hybrid (92.6%). Overall,frameworks agree
  on the dominant fuel population. Disagreement is revealed only in the
  small high-ash (Cluster 2) subgroup.

- **Cluster separation is majorly driven  by energy density and ash
  chemistry** (Random Forest feature importance, Phase 4B) however moisture and
  raw calorific value has secondary roles.

## Getting started

```bash
git clone https://github.com/Mishal-Asmat/biomass-wte-decision-framework.git
cd biomass-wte-decision-framework
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Reproducing the pipeline

Run the notebooks in order from the `notebooks/` folder 

```
01_data_audit.ipynb
02_basis_harmonization.ipynb
03_feature_engineering.ipynb
04_clustering_analysis.ipynb
04a_process_suitability.ipynb
04b_cluster_explainability.ipynb
04c_wte_conversion_decision.ipynb
05_decision_comparison.ipynb
06_decision_interpretability.ipynb
```

## Interactive dashboard

```bash
streamlit run app/app.py
```

Shows the choosen filters final decision table by biomass class and fuel cluster. It also
shows technology distributions, cluster-vs-technology crosstabs, and the feature profiles of recommended technology whose decision is obtained acoording to selected filters.

## Testing

```bash
pytest
```

17 unit tests cover the data-validation schematic logic, every engineered
fuel-quality/ash-risk formula, and the cluster-label canonicalization fix
described below.

## Methodology notes & corrections

This section documents substantive corrections made while assembling this
repository, for transparency:

1. **`Sample_ID` was being scaled and clustered on.** The clustering step
   originally passed the full `clustering_ready` dataframe, including the
   `Sample_ID` (reference column) into `StandardScaler`/`KMeans`. `Sample_ID`
   is an arbitrary integer key with no physical meaning; it has been
   excluded from the feature matrix (`src/clustering/preprocess.py` usage
   in `04_clustering_analysis.ipynb`).

2. **Cluster index was not semantically stable.** `scikit-learn`'s `KMeans`
   assigns integer cluster labels (0, 1, 2) based on internal
   centroid-discovery order. The
   rule-based decision modules (`src/models/cluster_only_rules.py`,
   `src/models/wte_conversion_rules.py`) hardcode technology decisions per
   literal cluster index, assuming Cluster 0 = lowest ash / most stable and
   Cluster 2 = highest ash / most constrained. Auditing the originally
   generated results showed Clusters 0 and 1 were transposed relative to
   that assumption, silently swapping the intended Combustion/Pyrolysis
   recommendation for over 100 out of 135 samples. `src/clustering/kmeans.py`
   now includes `canonicalize_cluster_labels()`, which deterministically
   relabels clusters by ascending mean `Ash_db` immediately after fitting,
   and every notebook/`src` call site uses it. All figures, tables, and the
   Phase 5/6A agreement-rate narrative in this repository reflect the
   corrected labels.

3. **A dead-end conditional in `wte_conversion_rules.py`.** The Cluster 2
   branch checked `constraint == "High Constraint"`, but
   `suitability_rules.py` only ever emits `"High"`, `"Moderate"`, or
   `"Low"`, so that branch could never fire. Fixed to check `"High"`.

4. **`cluster_explainability.py` (Phase 4B) had no notebook and hardcoded
   relative paths**, making it un-runnable outside one specific working
   directory. It has been refactored into reusable, parameterized functions
   in `src/analysis/cluster_explainability.py`with corresponding
   `04b_cluster_explainability.ipynb` notebook.

5. **`tests/test_data_validation.py` and `tests/test_feature_engineering.py`
both contain real pytest suites.

## License

Released under the [MIT License](LICENSE).

## Citation

If you use this framework or its methodology, please cite it using the
metadata in [`CITATION.cff`](CITATION.cff) 

**Author:** Mishal Asmat
