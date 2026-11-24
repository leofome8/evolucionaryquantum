# When does offline configuration pay off?

Code, registration documents and raw results for the manuscript *When does offline configuration pay off? A cost-accounted comparison of linear-ramp QAOA and tabu search* (L. A. Forero Mendoza, H. D. de Mello Junior, M. R. Kohler, E. C. S. Batista, M. A. Pacheco), submitted to the *Journal of Heuristics*.

The study compares a linear-ramp schedule of the quantum approximate optimization algorithm (QAOA), calibrated once and reused across instances, with tabu search and other classical heuristics. Every arm draws from one budget of objective evaluations, calibration samples are amortized over the instances that reuse them, and each round of experiments was registered, with the SHA-256 hash of its code, before it was run.

## Layout

| Folder | Contents |
| --- | --- |
| `code/` | Final version of the simulator and experiment driver (`qevo.py`) and of the report generator (`qevo_report.py`), identical to `registration/code_v9/`. |
| `registration/` | Amendments 3, 4 and 5 and Deviation 1, each with the exact code it froze (`code_v5` to `code_v9`), the scripts that ran each round, and `SHA256SUMS.txt`. |
| `data/` | Raw results of every round, one JSON line per run, compressed with gzip. |
| `analysis/` | Scripts for the analyses added after the runs (total cost, break-even, batch charging, instance features, sampler validation, tabu configuration, quality at fixed budgets, time). |
| `environment.yml` | Conda environment used for all runs. |
| `unpack_data.py` | Decompresses `data/` and creates `analysis/work/`. |

## Rounds and data

| Round | Governed by | Code | Data | Runs |
| --- | --- | --- | --- | --- |
| v5, full grid | Pre-registration and Amendment 1 | `code_v5` | `data/v5` | 137,400 |
| v6, confirmation on new instances | Amendment 2 | `code_v6` | `data/v6` | 48,150 |
| v7, calibration draws, interaction ablation, transferred tabu | Amendment 3 | `code_v7` | `data/v7` | 136,185 |
| v8, noise, depth, size extension | Amendment 4 | `code_v8_amendment4` | `data/v8_noise`, `data/v8_depth`, `data/v8_scale` | 104,160 with the rerun below |
| v8, first N = 26 run (invalid, kept for the record) | Amendment 4 | `code_v8_amendment4` | `data/v8_n26_invalid` | 5,280 |
| v8, N = 26 rerun after the sampler fix | Deviation 1 | `code_v8_deviation1` | `data/v8_n26_rerun` | 5,280 |
| v9, component tests | Amendment 5 | `code_v9` | `data/v9/*` | 47,280 |
| v9, tabu configurations on training instances (exploratory) | none | `code/` | `data/v9_tabu_training` | 1,920 |

`data/v9/teste_v9` is the smoke test that precedes the v9 runs. The pre-registration and Amendments 1 and 2 are deposited at [DOI do Zenodo].

The hashes in `registration/SHA256SUMS.txt` match those written in each amendment. Seeds are derived from the protocol label, the cell and the seed index, so running a cell again with the same code version gives the same result.

## Reproducing

Create the environment and decompress the data, from the repository root:

```
conda env create -f environment.yml
conda activate artigo3pip
python unpack_data.py
```

To rerun a round, run its script inside its code folder, for example `registration/code_v9/run_v9_amendment5.bat` on Windows. The scripts were written for a 24-core workstation; lower `--workers` on smaller machines. Interrupted runs resume, because cells already written are skipped. The scripts print messages in Portuguese, as they were deposited.

To rebuild the registered tables from the stored results:

```
cd registration/code_v9
python qevo_report.py ../../data/v9/artigo3_v9_cal ../../data/v9/artigo3_v9_classico ../../data/v9/artigo3_v9_classico24 ../../data/v9/artigo3_v9_classico26 ../../data/v9/artigo3_v9_dn
```

The same call with the folders of an earlier round, from that round's code folder, rebuilds its report.

## Analyses added after the runs

Run every script from the repository root, after `python unpack_data.py`. Start with `prep.py`, which builds `analysis/work/runs.pkl` from the v7 and v8 results; most other scripts read it.

| Script | Manuscript |
| --- | --- |
| `a1_total_cost_cvar/prep.py` | Builds the per-run table used by the scripts below |
| `a1_total_cost_cvar/an.py` | Three-level bootstrap and the analysis without draw d0 (Section 4.5, Table B1) |
| `a1_total_cost_cvar/agg.py` | Total-cost ratio and reuse curve (Tables 8 and 9) |
| `a1_total_cost_cvar/cvar.py`, `corr.py` | Calibration objective against samples to the optimum (Section 4.3) |
| `a2_batch_features_sampler/feat_ci.py` | Batch charging and instance features (Table 7, Section 4.5) |
| `a2_batch_features_sampler/sampler.py` | Validation of the sampler above 2^24 states (Appendix C) |
| `a2_batch_features_sampler/stale.py`, `sampler_old.py` | Stale-cache check of the original and fixed samplers |
| `a3_tabu_configuration/tabu_dev.py` | Runs the eight tabu configurations on 20 training instances per regime |
| `a3_tabu_configuration/table5_direct.py` | Ramp against the selected tabu configuration (Table 5) |
| `a3_tabu_configuration/table5.py` | Conservative estimate through the default tabu of each round (Section 4.4) |
| `a3_tabu_configuration/tabu_loo.py` | Earlier leave-one-instance-out selection, kept for reference |
| `a3_tabu_configuration/reseed_tabu.py` | Default tabu under the new random stream of v9 (Section 4.2) |
| `a4_breakeven_quality_time/nstar3.py` | Break-even number for a typical instance (Table 8) |
| `a4_breakeven_quality_time/fixedbudget.py` | Success rate and cut ratio at fixed budgets (Section 4.5) |
| `a4_breakeven_quality_time/time_table.py` | CPU time of tabu and the shot rate a device would need (Table 10) |

`tabu_dev.py` was stopped before finishing N = 26, where the configurations without restarts run for hours; the manuscript keeps the configuration chosen at every smaller size. `fixedbudget.py` reads the default tabu runs from two folders that hold identical runs, so its counts are doubled while its shares are not affected.

## Citation

If you use this material, please cite the manuscript (reference to be added on publication) and the Zenodo deposit [DOI do Zenodo].

## Contact

Leonardo Alfredo Forero Mendoza, Rio de Janeiro State University (UERJ), mendonza@ica.ele.puc-rio.br
