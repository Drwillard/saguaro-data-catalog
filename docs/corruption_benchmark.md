# Synthetic intervention benchmark

Ordinary scalar validity cannot establish whether a plausible measurement belongs
to the right organism, follows a death record, lies in its assigned plot, or
agrees with recorded source evidence. This benchmark tests those distinctions
through controlled interventions; it is not machine learning and does not
estimate ecological anomaly prevalence.

## Reproduce

Build and validate the canonical data first. From the project root:

```powershell
saguarodata benchmark corruption --seed 42 --count 100
saguarodata benchmark corruption --seeds 1,2,3 --count 100 --sample-size 1200
saguarodata benchmark corruption --seed 42 --count 30 --sample-size 1200 --intensity 0.25 --append
saguarodata benchmark report
```

The second and third commands reproduce the executed multi-seed/magnitude experiment. `--count` controls
the number of independent interventions per seed; changing it changes
experimental replication, not the fraction of simultaneously damaged
rows in a single dataset. Each trial starts again from the same baseline and
injects one scenario. This deliberately avoids interactions between a dropped
column and an unrelated temporal test. Results do not establish performance at
different simultaneous-error densities.

`--intensity` is a positive numeric magnitude multiplier: it scales height changes,
negative measurements, coordinate offsets, source-row offsets and artificial
geometry size. It retains the same target selection for a seed. Schema/key,
categorical and CRS-label interventions are discrete and unchanged by magnitude.
Use `--append` for distinct seeds/magnitudes with identical canonical input hashes
and cohort settings; duplicate trial IDs are rejected. The executed comparison
contains magnitude 1 with seeds 1/2/3 (100 trials each), plus magnitude 0.25 with
seed 42 (30 trials). Per-magnitude metrics are in
`corruption_benchmark_by_intensity.csv`; pooling across these deliberately chosen
magnitudes does not estimate a naturally occurring error distribution.

By default, a fixed cohort selected with cohort seed 17 contains approximately
1,200 real canonical organism observations. Whole supported histories are kept;
remaining slots are sampled from unlinked observations. All canonical plot and
organism/event context is retained. The cohort also includes the first 25
vegetation and aggregate observations and spatial features supplying plot
geometries plus the first 40 source features. It is a reproducible capability
experiment, not a representative park-wide error-rate sample. `--sample-size 0`
uses the entire canonical corpus and can be substantially slower. Experiment
seeds choose corruption targets; they do not change the comparison cohort.

## Scenarios

`configs/corruption_scenarios.yaml` defines all 30 scenarios, scheduled in order
and repeated round-robin when count exceeds 30. Eligibility is checked rather
than inventing identities, geometry or histories. Ineligible scenarios are
recorded as skips, not detections or misses.

| Family | Implemented interventions |
|---|---|
| Schema/representation (6) | Rename height column; store height as text; remove observation-ID column; change status token; null observation ID; remove normalized unit metadata |
| Scalar/row (6) | Negative height; negative arms; impossible latitude; duplicate source/event row with new canonical ID; exact canonical duplicate; malformed numeric token |
| Longitudinal (7) | Explicit death followed by explicit life; artificial height decrease; extreme positive growth; arm collapse; duplicate organism/event; unrelated identity reassignment; year swap with event IDs unchanged |
| Spatial (6) | Move outside known assigned plot; remove feature CRS; mislabel source CRS; swap coordinates; invalidate geometry bytes while retaining stored flags; borrow another plot's coordinates |
| Provenance (5) | Change physical row with stale lineage; replace SHA with unknown hash; remove transformation; change normalized value without updating its trace; duplicate canonical row with identical lineage |

Raw NPS files and normal processed Parquet are never written by this experiment.
Every mutation is applied to a deep copy. Table-wide schema interventions record
all affected source/canonical IDs; local interventions record changed rows and
the supported history affected by them. The ground truth preserves before/after
values, fields, scenario ID, seed and deterministic corruption ID. No injector
changes raw artifacts to manufacture a source error.

## Intervention semantics

Each configuration entry, ground-truth row and result row carries `scenario_semantics` independently of its legacy implementation family:

| scenario_semantics | Scenarios |
|---|---|
| plausible_biological_transition | temporal_height_decrease, temporal_arm_collapse |
| semantic_contradiction | temporal_dead_to_alive |
| statistical_anomaly | temporal_positive_growth |
| integrity_violation | Other schema, key, scalar, identity, spatial-reference and provenance interventions |

The by-semantics detection matrix is exported as `corruption_benchmark_by_semantics.csv`. A height or arm decrease is not intrinsically an error. Those trials ask whether a transition is screened, not whether biology is invalid. Most simulated changes retain the original provenance snapshot, so provenance recovery for a biological transition means stored evidence is inconsistent with the changed canonical value; it does not establish that the changed value is biologically impossible. The legacy `benchmark corruption` CLI and `corruption_id`/`corruption_class` fields remain supported for reproducibility.

## Validation layers

1. **Schema:** required columns, strict numeric/text types on declared fields,
   required-ID nullability, and status enum membership. Extra adapter columns are
   allowed. Types are declared independently of corrupted data, not inferred from it.
2. **Row-wise:** numeric parsing/finite values, geographic ranges, height 0–30 m,
   arms 0–200, integer arm counts, exact duplicate rows, observation primary keys,
   source-row/event and supported organism/event composite keys. These broad
   scalar ceilings are benchmark baseline assumptions, not new ecological truth.
3. **Structural:** existing saguarodata checks plus explicit organism/tag/plot
   consistency, event-year agreement, and normalized-height unit metadata checks.
4. **Temporal:** the actual existing death/life, after-death measurement,
   shrinkage, arm-decrease and robust growth screens, with their configured
   eligibility and thresholds.
5. **Spatial:** existing coordinate, plot, geometry and CRS checks plus direct
   source-to-geographic CRS consistency and validation of geometry bytes even if
   the cached validity flag says true.
6. **Provenance:** manifest, source-row, sheet/field, normalization-record,
   value-snapshot and finding-reference integrity checks.

The extra contextual checks are disclosed additions; the report does not claim
that they were present in the original release. Conventional checks can detect
several temporal/spatial scenarios, and overlap is reported rather than hidden.
Schema failures are preserved as schema findings. Numeric inputs supplied to
legacy scientific validators are safely coerced to null when unparseable, never
restored from uncorrupted values. Detector exceptions are recorded and scored as
misses, not as successful validation failures.

## Scoring

For each layer, run the unchanged cohort once, then subtract its existing warning
and error signatures from each intervention trial. Informational collection notes
are not error detections. Signatures use source-row/event anchors so removing a
canonical key or changing lineage metadata cannot turn the same old scientific
warning into a claimed new detection. Numerically equivalent JSON values are
normalized for comparison.

Explicit predecessor IDs and empirical threshold summaries are excluded from
baseline equivalence: losing an ID or recomputing a median must not relabel an
already-emitted scientific condition as a newly recovered corruption. Measured
before/after values, annual growth, status changes and elapsed time remain part
of the comparison. A separate diagnostic column records newly emitted
UNKNOWN_SPATIAL_CRS informational findings; they do not inflate warning/error
recall or get relabeled as scientific errors.

New warning/error alerts attached to the intervention's affected row or supported
history count as matched evidence. Each trial has only one intervention, so
downstream integrity symptoms on other fields are attributable effects too.
New alerts on other evidence count as **operational false-positive alerts**.
These may be secondary consequences of a corruption, such as changing a robust
growth threshold; they are not adjudicated scientifically false claims.

- Recall: detected injections / completed injections.
- Event precision: detected injections / (detected injections + unmatched new
  alerts), collapsing redundant matched alerts for the same injection.
- F1: harmonic mean of event precision and injection recall.
- Alert precision: matched new alerts / all new alerts, separately reported.
- Miss: no attributable new warning/error from that layer, including detector failure.

Report both alert counts and injection counts because their units differ. This
is an intervention-recovery benchmark with no validated all-clean natural-data
gold standard; it does not establish natural-data specificity or a true-negative
rate. The source may contain legitimate biological exceptions and unresolved
pre-existing anomalies. A successful synthetic detection is not proof of a
source error in an unmodified dataset.

Most numeric interventions change canonical values while retaining the recorded
provenance snapshot. That gives the provenance layer independent stored context
that the schema/range baselines do not inspect. These results establish
cross-table inconsistency recovery, not recovery of a transcription error already
present in the original workbook. A coherent alteration of canonical values,
source evidence and provenance together is outside this experiment and can evade
these checks.

## Outputs and audit trail

Ignored `data/benchmark/` contains ground truth, per-layer results, new alerts and
matching decisions, plus input/configuration/implementation hashes and skip logs.
The run checks the SHA-256 of every normal processed Parquet before and after.
`reports/corruption_benchmark.md` and its summary, scenario, semantics, class, group and
overlap CSV companions are small reviewable artifacts. Tables come from executed
results. Running the command again replaces the current benchmark output; archive
the folder externally to retain a prior experiment. Seed recall variation is
reported across the executed seeds, without an unsupported population confidence
interval.
