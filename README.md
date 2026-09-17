# Biomass Waste-to-Energy (WtE) Decision Framework

A reproducible data-science pipeline that turns a laboratory biomass/waste
fuel database into an interpretable, engineering-defensible **conversion
technology recommendation** (combustion, gasification, or pyrolysis) for
each sample, combining unsupervised fuel-typology clustering with
literature-aligned thermochemical process-suitability rules.

Built on 135 characterized Australian biomass and waste fuel samples
(proximate/ultimate analysis, higher heating value, and ash-mineral
composition), the project handles three questions:

1. **What *is* this fuel?** : data-driven fuel typology via unsupervised clustering, independent of administrative `Biomass_Type` labels.
2. **What *can* this fuel do?** : literature-aligned thermochemical process-suitability screening (VM/FC/Ash/moisture/alkali thresholds).
3. **What *should* we build?** : a hybrid decision layer combining (1) and (2), benchmarked against cluster-only and rule-only baselines, with a full disagreement/interpretability audit of where and why the frameworks diverge.

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
| 1 | `01_data_audit.ipynb` | Is the raw dataset complete and well-typed? | `data/interim/validated_data.csv` |
| 2 | `02_basis_harmonization.ipynb` | Which analytical basis best represents intrinsic fuel chemistry? | `data/interim/harmonized_db_basis.csv` (dry basis) |
| 3 | `03_feature_engineering.ipynb` | Which engineered indices capture reactivity, energy intensity, and ash risk? | `data/interim/engineered_features.csv` |
| 4 | `04_clustering_analysis.ipynb` | Do fuels separate into physically meaningful clusters? | KMeans fuel typology (k = 3) |
| 4A | `04a_process_suitability.ipynb` | Which processes are chemically/physically feasible per sample? | Primary/Secondary process + constraint level |
| 4B | `04b_cluster_explainability.ipynb` | Which properties drive the cluster separation? | Random Forest feature importance |
| 4C | `04c_wte_conversion_decision.ipynb` | Combining typology + suitability, what's the final technology? | `data/processed/wte_final_decisions.csv` |
| 5 | `05_decision_comparison.ipynb` | How much does clustering actually add vs. rules alone? | `data/processed/comparison_decisions.csv` |
| 6 | `06_decision_interpretability.ipynb` | Where and why do the three frameworks disagree? | `data/processed/disagreement_analysis.csv` |

Each notebook is a thin orchestration layer i.e all transformation and
decision logic lives in the tested `src/` package, so notebooks stay
readable and results stay reproducible outside Jupyter (e.g., from
`app.py` or a CI pipeline).

## Repository structure

```
biomass-wte-decision-framework/
├── app/
│   └──app.py                    # Streamlit dashboard for the final decisions
├── data/
│   ├── raw/                     # original 79-column fuel database
│   ├── interim/                 # validated → dry-basis harmonized → engineered
│   ├── processed/               # clustering-ready + final decision tables
│   └── metadata/                # variable-categorization & basis-selection audit trails (JSON)
├── notebooks/                   # 01 → 06, run in numeric order
├── src/
│   ├── config/                  # thresholds & column-group reference (no data transforms)
│   ├── data/                    # load / validate / harmonize
│   ├── features/                # engineered fuel-quality + ash-risk indices
│   ├── clustering/               # scaling, KMeans, k-selection, label canonicalization
│   ├── models/                  # process-suitability & conversion-technology decision rules
│   ├── analysis/                # cluster explainability, disagreement labeling, feature diagnostics
│   └── visualization/           # all matplotlib/seaborn plotting functions
├── results/
│   ├── tables/                  # every summary/crosstab CSV produced by the notebooks
│   └── figures/                 # every PNG produced by the notebooks
├── tests/                       # pytest unit tests for src/
├── pyproject.toml               # pytest config
├── requirements.txt
├── .gitignore
├── LICENSE
├── CITATION.cff
└── README.md
```

## Key results

- **Fuel typology (k = 3, silhouette ≈ 0.58):**

  | Cluster | Regime | CV (MJ/kg, db) | VM (%, db) | Ash (%, db) | Best suited for |
  |---|---|---|---|---|---|
  | 0 | Ultra-high-energy, volatile-rich | ≈40.6 | ≈97.8 | ≈1.3 | Gasification / combustion |
  | 1 | Balanced, conversion-ready (majority class) | ≈19.5 | ≈80.6 | ≈2.7 | Pyrolysis / combustion |
  | 2 | Low-energy, ash-constrained | ≈12.9 | ≈52.9 | ≈35.4 | Gasification / pre-treatment |

- **Final hybrid technology distribution** (135 samples): Pyrolysis 111,
  Further Assessment Needed 17, Gasification 6, Combustion 1.

- **Framework agreement:** cluster-only vs. rule-only 90.4%, rule-only vs.
  hybrid 85.2%, cluster-only vs. hybrid 92.6%. The frameworks broadly agree
  on the dominant fuel population, with disagreement concentrated in the
  small high-ash Cluster 2 subgroup (see Phase 6A for the full breakdown).

- **Cluster separation is driven primarily by energy density and ash
  chemistry** (Random Forest feature importance, Phase 4B) whereas moisture and
  raw calorific value play secondary roles.

## Getting started

```bash
git clone https://github.com/Mishal-Asmat/biomass-wte-decision-framework.git
cd biomass-wte-decision-framework
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Reproducing the pipeline

Run the notebooks in order from the `notebooks/` folder (each one reads
the previous phase's output from `../data/` and writes its own output back
there and to `../results/`):

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

The checked-in `data/interim`, `data/processed`, and `results/`
files would reproduce by running notebooks from scratch.

## Interactive dashboard

```bash
streamlit run app.py
```

Filters the final decision table by biomass class and fuel cluster, and
shows technology distributions, cluster-vs-technology crosstabs, and
decision-active feature profiles per recommended technology.

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
