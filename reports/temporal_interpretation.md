# Real-data temporal interpretation

Temporal findings identify transitions requiring review. They do not classify biological change as data corruption. A value can be structurally valid while its meaning depends on organism identity, time, field protocol and observation notes.

Total temporal findings: 502. Counts below are findings/pairs, not unique cacti or independent note texts. A note is counted if either member has nonempty commentary. Explicit alive/dead status uses the same conservative note parser and survey-year guard as ingestion. Operational tags use exact documented phrases only. These counts show potential context, not proof that a note explains a transition.

## Categories in all real validation findings

| finding_category | count |
| --- | --- |
| integrity_violation | 9467 |
| semantic_contradiction | 0 |
| biological_transition | 320 |
| data_quality_warning | 6228 |
| informational | 1693 |

Integrity-violation labels identify declared constraint/evidence-chain breaches; they are not adjudications of which biological source value is wrong.

## Temporal counts and commentary coverage

| rule_id | finding_category | severity | count | has_any_note | has_explicit_alive_dead_note | has_explicit_status_note | has_review_annotation | has_tag_only_or_off_plot | has_not_measured_annotation | has_verify_status | verify_yes | verify_no | verify_not_found |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEMPORAL_SHRINKAGE | biological_transition | warning | 94 | 80 | 47 | 47 | 0 | 0 | 0 | 94 | 74 | 19 | 1 |
| TEMPORAL_ARM_DECREASE | biological_transition | warning | 226 | 177 | 100 | 109 | 0 | 0 | 0 | 226 | 179 | 35 | 12 |
| TEMPORAL_STATUS_CONTRADICTION | semantic_contradiction | warning | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| TEMPORAL_MEASUREMENT_AFTER_DEATH | data_quality_warning | warning | 49 | 49 | 49 | 49 | 0 | 0 | 0 | 49 | 46 | 2 | 1 |
| TEMPORAL_REOBSERVED | informational | info | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 3 | 0 | 0 |
| TEMPORAL_GROWTH_OUTLIER | data_quality_warning | warning | 21 | 17 | 15 | 15 | 0 | 0 | 0 | 21 | 21 | 0 | 0 |
| TEMPORAL_STATUS_RESOLVED | informational | info | 109 | 109 | 109 | 109 | 0 | 0 | 0 | 109 | 86 | 23 | 0 |

## Pair-level totals

| context | findings |
| --- | --- |
| has_any_note | 435 |
| has_explicit_alive_dead_note | 320 |
| has_explicit_status_note | 332 |
| has_review_annotation | 0 |
| has_tag_only_or_off_plot | 0 |
| has_not_measured_annotation | 0 |
| has_verify_status | 502 |
| verify_yes | 409 |
| verify_no | 79 |
| verify_not_found | 14 |

Verify values are source-row flags. In the Historic workbook a single Verify cell is shared by multiple year columns; it does not establish independent verification of each survey. Yes and No are context, not correctness labels. Yes/No counts can overlap in a pair and must not be summed as mutually exclusive classes. Unknown/unrecognized values remain visible; blank is not_recorded.

## Representative examples

Selection prioritizes L130/L167 where applicable, then deterministic finding-ID order, up to five examples per rule. No example is used to infer which record is wrong.

### TEMPORAL_SHRINKAGE

- Finding `ec05f0030484165fe3fdef17` · historic_plots:75L / L130 · biological_transition / warning
  - Large height decrease detected. Possible explanations include top/stem breakage, measurement differences, source-unit problems, transcription error, or identity mismatch.
  - 1975: height=7.455, arms=6.0, status=unknown, notes='fairtop thin', Verify=no; 2001: height=1.55, arms=0.0, status=alive, notes='live', Verify=no
  - Evidence: previous `e3770fc78729a3b8520c5cb2`, current `58f020371babd818c05cb635`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2928 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `0022b2a72d4859c06caf0a77` · historic_plots:75J / J38 · biological_transition / warning
  - Large height decrease detected. Possible explanations include top/stem breakage, measurement differences, source-unit problems, transcription error, or identity mismatch.
  - 2010: height=10.0, arms=4.0, status=unknown, notes=' ', Verify=yes; 2014: height=4.8, arms=4.0, status=unknown, notes='frost damage; broken top', Verify=yes
  - Evidence: previous `4e037ca50a6609fc32099034`, current `971f76315debb9479d9231a5`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2262 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `05314c952655783b263ad6d4` · historic_plots:75L / L61 · biological_transition / warning
  - Large height decrease detected. Possible explanations include top/stem breakage, measurement differences, source-unit problems, transcription error, or identity mismatch.
  - 2001: height=6.8, arms=2.0, status=alive, notes='live', Verify=yes; 2010: height=5.05, arms=1.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `a9171f937317e543bb7cdd10`, current `685d2eb8c667a0130dac2d71`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3072 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `05ab24555500071b0ae96a68` · historic_plots:75K / K8 · biological_transition / warning
  - Large height decrease detected. Possible explanations include top/stem breakage, measurement differences, source-unit problems, transcription error, or identity mismatch.
  - 1975: height=6.575, arms=1.0, status=unknown, notes='good', Verify=yes; 2001: height=3.1, arms=1.0, status=unknown, notes='yestop broken off just above arm', Verify=yes
  - Evidence: previous `bc618cadbc9f5cbc937dcfa8`, current `f1fdea8b7b0a0fe345c9d0e3`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2604 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `09a4941d491961869967bf92` · historic_plots:75L / L137 · biological_transition / warning
  - Large height decrease detected. Possible explanations include top/stem breakage, measurement differences, source-unit problems, transcription error, or identity mismatch.
  - 1975: height=7.66, arms=2.0, status=unknown, notes='missingone arm droops', Verify=no; 2001: height=5.0, arms=0.0, status=alive, notes='live', Verify=no
  - Evidence: previous `c2f562b8d1b2c50a58986e80`, current `6103846bb87d399e96fe8ba7`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2935 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`

### TEMPORAL_ARM_DECREASE

- Finding `ab7549627e42bf157c5b847b` · historic_plots:75L / L130 · biological_transition / warning
  - Arm count decreased between surveys. Saguaros can lose arms through breakage or damage; review source notes and measurements before interpreting this as an error.
  - 1975: height=7.455, arms=6.0, status=unknown, notes='fairtop thin', Verify=no; 2001: height=1.55, arms=0.0, status=alive, notes='live', Verify=no
  - Evidence: previous `e3770fc78729a3b8520c5cb2`, current `58f020371babd818c05cb635`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2928 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `00c86b06d5688193040322b2` · historic_plots:75L / L84 · biological_transition / warning
  - Arm count decreased between surveys. Saguaros can lose arms through breakage or damage; review source notes and measurements before interpreting this as an error.
  - 2001: height=4.9, arms=3.0, status=alive, notes='live', Verify=no; 2010: height=2.55, arms=0.0, status=unknown, notes='', Verify=no
  - Evidence: previous `dcec776977007fe0dfa9ba3c`, current `81f00051303f8bf7542dfe11`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3097 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `015017920626170d54245d6e` · historic_plots:75L / L206 · biological_transition / warning
  - Arm count decreased between surveys. Saguaros can lose arms through breakage or damage; review source notes and measurements before interpreting this as an error.
  - 1975: height=5.145, arms=2.0, status=unknown, notes='fair', Verify=yes; 2001: height=2.7, arms=0.0, status=alive, notes='live', Verify=yes
  - Evidence: previous `3d9a927f21e740146ad61438`, current `267f153c9d418e4b9eea2551`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3013 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `0167a142f47cdc5d39e3e1e8` · historic_plots:75M / M97 · biological_transition / warning
  - Arm count decreased between surveys. Saguaros can lose arms through breakage or damage; review source notes and measurements before interpreting this as an error.
  - 2010: height=3.6, arms=3.0, status=unknown, notes='', Verify=yes; 2014: height=3.69, arms=2.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `810e24b632b94b69ee5a96f5`, current `b710204d4bf2a2f7119c9dfc`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3636 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `0278cd76be1919c322663d82` · historic_plots:41D / D11 · biological_transition / warning
  - Arm count decreased between surveys. Saguaros can lose arms through breakage or damage; review source notes and measurements before interpreting this as an error.
  - 1975: height=8.495, arms=5.0, status=unknown, notes='GOOD', Verify=no; 2010: height=0.0, arms=0.0, status=unknown, notes='dead no tag; redo 05/26/11', Verify=no
  - Evidence: previous `febb1220e4c5cd3ca942165b`, current `4f5b0a9b3d019c67d232b2d7`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 865 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`

### TEMPORAL_STATUS_CONTRADICTION

No real findings of this type were emitted.

### TEMPORAL_MEASUREMENT_AFTER_DEATH

- Finding `155dffabaa8d7b132eca0796` · historic_plots:75L / L167 · data_quality_warning / warning
  - A standing dead cactus can still be measured. A later positive height does not establish survival; review status and measurement semantics.
  - 2001: height=0.0, arms=None, status=dead, notes='dead', Verify=yes; 2014: height=3.4, arms=0.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `2b5ded29b7b4e5aec8a28645`, current `cff6f41d0157a359f1238936`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2969 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `bfcf14ab785007073b33933d` · historic_plots:75L / L167 · data_quality_warning / warning
  - A standing dead cactus can still be measured. A later positive height does not establish survival; review status and measurement semantics.
  - 2001: height=0.0, arms=None, status=dead, notes='dead', Verify=yes; 2010: height=3.4, arms=0.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `2b5ded29b7b4e5aec8a28645`, current `8b997c50962a63933437451a`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2969 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `05992e5d0985313496722a6c` · historic_plots:75L / L30 · data_quality_warning / warning
  - A standing dead cactus can still be measured. A later positive height does not establish survival; review status and measurement semantics.
  - 2001: height=0.0, arms=None, status=dead, notes='dead', Verify=yes; 2014: height=8.1, arms=1.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `25b126c2a4f5d0a9238a4544`, current `06498e959c1678d4b6da1ad2`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3038 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `05b89dc0fb5523c1b588af9c` · historic_plots:75L / L136 · data_quality_warning / warning
  - A standing dead cactus can still be measured. A later positive height does not establish survival; review status and measurement semantics.
  - 2001: height=0.0, arms=None, status=dead, notes='dead', Verify=yes; 2014: height=6.6, arms=0.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `cdc0111f780e114d5e1c37ae`, current `4e45191a27afe7e8ddf32cdf`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2934 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `0d997cfde760085a1ecd5b12` · historic_plots:75L / L196 · data_quality_warning / warning
  - A standing dead cactus can still be measured. A later positive height does not establish survival; review status and measurement semantics.
  - 2001: height=0.0, arms=None, status=dead, notes='dead', Verify=yes; 2010: height=4.8, arms=0.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `6cfb339e032cae8ee39c7beb`, current `827dbb1f7963a95e99e3055f`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3001 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`

### TEMPORAL_REOBSERVED

- Finding `0ab658bf610212581e6f9af7` · historic_plots:41C / C33 · informational / info
  - Re-observation after not_found. Prior absence is not equivalent to death.
  - 1975: height=0.475, arms=0.0, status=not_found, notes='missing', Verify=yes; 2001: height=1.35, arms=0.0, status=unknown, notes='no tag', Verify=yes
  - Evidence: previous `51ffe7954d730feaf8f6bf01`, current `4dc4e4694f7f376135cdbbfe`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 688 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `1e63878da439b45dc5162463` · historic_plots:75M / M191 · informational / info
  - Re-observation after not_found. Prior absence is not equivalent to death.
  - 1975: height=5.615, arms=2.0, status=not_found, notes='missing', Verify=yes; 2001: height=6.4, arms=5.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `5c9a9e69a20717ad581519cf`, current `0473543e145452c215548e50`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3501 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `f7467808828d8d854304c7c2` · historic_plots:41C / C213 · informational / info
  - Re-observation after not_found. Prior absence is not equivalent to death.
  - 1975: height=0.133, arms=0.0, status=not_found, notes='missing', Verify=yes; 2001: height=0.86, arms=0.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `0f26ee2708b6a24a9f82c801`, current `6da21f280ad8b3ff704da590`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 648 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`

### TEMPORAL_GROWTH_OUTLIER

- Finding `115b407dc9438b4550466f53` · historic_plots:75L / L120 · data_quality_warning / warning
  - Statistical screening only; no biological maximum asserted.
  - 2001: height=1.6, arms=0.0, status=alive, notes='live', Verify=yes; 2010: height=6.05, arms=1.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `381c67cb74a76d0729975a8c`, current `11df53369faecaa4d04a112f`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2850 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `199baa455defa66fefbcba10` · historic_plots:75M / M1150 · data_quality_warning / warning
  - Statistical screening only; no biological maximum asserted.
  - 2010: height=6.0, arms=5.0, status=unknown, notes='', Verify=yes; 2014: height=8.0, arms=5.0, status=unknown, notes='frost damage', Verify=yes
  - Evidence: previous `c585b7ef801dfc91a403268b`, current `3aad997ba6baffa526f73f89`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3279 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `1e477bd40d1d89b0a23e8896` · historic_plots:75L / L220 · data_quality_warning / warning
  - Statistical screening only; no biological maximum asserted.
  - 2010: height=7.05, arms=1.0, status=unknown, notes='', Verify=yes; 2014: height=9.1, arms=1.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `72c253aa48d2d58816cbcd15`, current `6785ecec4de949b1332fa562`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3029 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `28398040323e19d64ae86e31` · historic_plots:75L / L1147 · data_quality_warning / warning
  - Statistical screening only; no biological maximum asserted.
  - 2010: height=0.28, arms=0.0, status=unknown, notes='', Verify=yes; 2014: height=2.75, arms=0.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `30fa7a10635b39a4d9793047`, current `a33a51dc06d32f1b5d6db1b0`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2792 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `4768e72205655717ae8fc1de` · historic_plots:75J / J1171 · data_quality_warning / warning
  - Statistical screening only; no biological maximum asserted.
  - 2010: height=1.17, arms=0.0, status=unknown, notes='', Verify=yes; 2014: height=3.24, arms=0.0, status=unknown, notes='', Verify=yes
  - Evidence: previous `0806625da0863a7f282eed20`, current `d72bf4d47dbf5b396fa15200`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2153 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`

### TEMPORAL_STATUS_RESOLVED

- Finding `18a935e88ee232979ce67931` · historic_plots:75L / L130 · informational / info
  - A status-resolution event, not an inconsistency.
  - 1975: height=7.455, arms=6.0, status=unknown, notes='fairtop thin', Verify=no; 2001: height=1.55, arms=0.0, status=alive, notes='live', Verify=no
  - Evidence: previous `e3770fc78729a3b8520c5cb2`, current `58f020371babd818c05cb635`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2928 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `07c6d70a6496d3db9ab09144` · historic_plots:75L / L69 · informational / info
  - A status-resolution event, not an inconsistency.
  - 1975: height=3.055, arms=0.0, status=unknown, notes='excellent', Verify=no; 2001: height=2.2, arms=0.0, status=alive, notes='live', Verify=no
  - Evidence: previous `d13ff8fec77b242148e48e02`, current `2313db665b72c97f568e828c`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 3080 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `09b68f336085f701a334f928` · historic_plots:75L / L120 · informational / info
  - A status-resolution event, not an inconsistency.
  - 1975: height=3.86, arms=0.0, status=unknown, notes='missingtop pinched, deformed', Verify=yes; 2001: height=1.6, arms=0.0, status=alive, notes='live', Verify=yes
  - Evidence: previous `7ac578785eed86aa13bd35d0`, current `381c67cb74a76d0729975a8c`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2850 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `0b76ab54eb0cb8b7409e5cbb` · historic_plots:75L / L18 · informational / info
  - A status-resolution event, not an inconsistency.
  - 1975: height=2.72, arms=0.0, status=unknown, notes='excellent', Verify=yes; 2001: height=5.0, arms=0.0, status=alive, notes='live', Verify=yes
  - Evidence: previous `24d91d0960b57b2307cd89c5`, current `efb179db050a89de4728db1c`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2983 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`
- Finding `0c641a6657d62bb074f10947` · historic_plots:75L / L181 · informational / info
  - A status-resolution event, not an inconsistency.
  - 1975: height=0.302, arms=0.0, status=unknown, notes='excellent', Verify=yes; 2001: height=0.7, arms=0.0, status=alive, notes='live', Verify=yes
  - Evidence: previous `be89cd60f9cc79dd00bd03f8`, current `9430ed2986e072b757f3de21`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/2225187) · Sheet1 row 2985 · SHA-256 `6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a`

## Source-checked case studies

### L130

| survey_year | height_m | arm_count | status | notes | verification_raw | verification_status | source_row |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1975 | 7.455 | 6.0 | unknown | fairtop thin | No | no | 2928 |
| 2001 | 1.55 | 0.0 | alive | live | No | no | 2928 |
| 2010 | 0.0 | 0.0 | dead | dead | No | no | 2928 |

The height and arm counts fall between 1975 and the nominal 2001 round while the later note explicitly says live. The 1975 phrase fairtop thin is retained as descriptive prose, not a damage/status classification. The 2010 note explicitly says dead. This is consistent with several possible biological or recording explanations; the source does not establish that the earlier decrease is an error. Verify=No is a shared-row context flag, not proof of invalid measurements.

Source: Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls · Sheet1 row 2928 · NPS 2225187. A shared workbook row contains multiple survey-year columns; Verify has no independently documented survey date.
### L167

| survey_year | height_m | arm_count | status | notes | verification_raw | verification_status | source_row |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1975 | 1.12 | 0.0 | unknown | excellent | Yes | yes | 2969 |
| 2001 | 0.0 | — | dead | dead | Yes | yes | 2969 |
| 2010 | 3.4 | 0.0 | unknown |  | Yes | yes | 2969 |
| 2014 | 3.4 | 0.0 | unknown |  | Yes | yes | 2969 |

The 2001 note explicitly says dead; later positive heights have unknown formal status and blank notes. Those measurements do not establish later life or a literal reversal of death. A standing dead cactus can still be measured; classification, linkage and transcription also remain review possibilities. Verify=Yes does not adjudicate the conflicting interpretations.

Source: Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls · Sheet1 row 2969 · NPS 2225187. A shared workbook row contains multiple survey-year columns; Verify has no independently documented survey date.
