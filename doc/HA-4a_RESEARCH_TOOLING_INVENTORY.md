# HA-4a research and tooling inventory

Status: read-only inventory, captured 2026-09-05. No live HA, broker,
inverter, serial device or Growatt web endpoint was changed. Existing local
logs and the untracked web mirror were preserved.

## A. Current repository state and history

The HA-core checkout is a wrapper, not the authoritative source repository for
the integration or broker. Its relevant submodules are:

| Component | Current checkout | Role |
|---|---|---|
| `external/Homeassistant-Growatt-Local-Modbus` | `c11ed6e` (`fix/min-6000xh`) | HA integration and register research |
| `external/growatt-rtu-broker` | `b42445f` (`develop/live-broker-battery`) | RTU master, TCP bridge, Shine passthrough and log tools |
| `external/OpenInverterGateway` | `9fbe4d2` | Community firmware reference |
| `external/grott` | local untracked submodule | Grott layouts and Shine/server protocol reference |
| `external/inverter-to-mqtt-esp8266` | local untracked submodule | Community register/topic reference |

The parent worktree is intentionally dirty: the integration and broker
submodules differ from the recorded parent gitlinks, and Grott plus
inverter-to-mqtt are untracked. Those changes belong to the existing research
workspace and were not altered.

The integration history is staged rather than linear in purpose:

1. vendor PDF conversion and the original register documentation;
2. TL-XH/runtime mapping and simulator work;
3. best-guess cleanup, catalogue/schema and source overlays;
4. graph/consolidated-reference work;
5. local web extraction;
6. MIN 6000TL-XH read-only hardware validation and correction.

The broker history has a separate progression: initial single-master broker,
HA deployment and sniffing, optional/hot-pluggable Shine, 20 ms RTU framing,
the 2 ms gap-floor experiment, then deterministic standard TCP framing and a
retry for silent standard reads. The latest broker source therefore contains
both a generic gap/CRC framer for Shine and a request-aware standard Modbus
reader for TCP clients.

The README and `AGENTS.md` files are partly aspirational. In particular, the
integration README describes the simulator as the normal development path and
the integration `doc/README.md` describes a future overlay-promotion and
conflict-review pipeline. Those promotion/classification tools are not
present; the current graph/export code is the executable description.

## B. Python tooling inventory

### Integration and register knowledge

| Script | Inputs → outputs | Status and overlap |
|---|---|---|
| `doc/build_input_spec.py` | `HA_local_registers.json` → mutates input part of `growatt_registers_best_guess.json` and datatype data | Older curated rebuild step; destructive in-place generator; overlaps `normalize_register_spec.py` and the HA extractor. Use only deliberately. |
| `doc/normalize_register_spec.py` | best-guess JSON + HA snapshot → in-place best-guess normalization | Curated-source mutator, not the canonical export. |
| `doc/build_register_data_types.py` | HA snapshot → `growatt_register_data_types.json` | Reproducible; also adds a large manual datatype catalogue. Feeds the graph. |
| `doc/convert_growatt_registers_best_guess.py` | best-guess, catalogue, datatypes, vendor tables → `growatt_registers_best_guess.v2.json` | Reproducible schema projection; parallel to, but not the same as, the graph export. |
| `doc/extract_vendor_tables_overlay.py` | vendor tables + v2 + catalogue → `overlays/growatt_vendor_tables_overlay.json` | Reproducible overlay; currently not ingested by the graph builder. |
| `doc/extract_growatt_datatypes_overlay.py` | datatype catalogue + v2 + catalogue → `overlays/growatt_datatypes_overlay.json` | Reproducible overlay; currently not ingested by the graph builder. |
| `doc/extract_HA_local_registers.py` | live integration Python modules/translations → `HA_local_registers.json` | Reproducible snapshot; graph input and an important runtime-to-doc bridge. |
| `doc/extract_grott_register_layouts.py` | local `external/grott` → `grott_register_layouts.json` | Reproducible only with the local Grott checkout; graph input. |
| `doc/extract_openinverter_gateway.py` | local OpenInverter source/docs → `openinverter_gateway_registers.json` | Reproducible only with that submodule; graph input with explicit register mappings and provenance. |
| `doc/extract_inverter_to_mqtt_registers.py` | local inverter-to-mqtt Markdown/source → `inverter_to_mqtt_registers.json` | Reproducible only with that submodule; graph input. |
| `doc/build_register_graph.py` | vendor tables, best-guess, Grott, HA, manual datatypes, OpenInverter, inverter-to-mqtt → `register_graph.gpickle` | Current knowledge-graph builder. It does not ingest web metadata, overlays, v2, catalogue JSON, live-validation JSON or the MIN-specific overlay. |
| `doc/generate_consolidated_ref.py` | graph pickle → `consolidated_register_ref.json`; explicit legacy fallback for comparison | Graph path is canonical and fails loudly when the graph is absent. The loose-source path requires `--legacy-fallback` and an explicit noncanonical output path. |
| `doc/compare_openinverter_gateway.py` | OIG export + best-guess + datatypes → `doc/ref/openinverter_gateway_comparison.md` | Comparison report; does not feed runtime or graph. |
| `doc/render_register_spec.py` | best-guess + HA snapshot → local Markdown preview | Ad-hoc renderer; output is not currently committed. |
| `doc/showSettings.py` | saved settings/capture material → human-readable settings analysis | One-off research helper; no structured output pipeline was found. |
| `doc/validate_min_6000tl_xh_map.py` | model map + captured raw validation JSON → assertions | Current deterministic hardware-evidence validator; separate from the general graph. |

The integration testing/read utilities are:

| Script | Purpose | Status |
|---|---|---|
| `testing/modbus_simulator.py` | deterministic Modbus simulator | Runtime test utility; the broker package now owns the richer simulator implementation. |
| `testing/probe_simulator.py` | starts the simulator and reads a few ranges | Reproducible smoke helper. |
| `testing/tcp_read.py` | small PyModbus TCP read, with stale example host `192.168.2.48` | Useful template, not production-ready as written. |
| `testing/read_registers.py` | direct serial scan of broad TL-XH ranges | Hardware utility; unsafe for concurrent production use and explicitly bypasses the broker. |
| `testing/parse_registers.py` | old Markdown table → four JSON maps | Legacy parser; its expected `testing/growatt_registers.md` is not the current canonical pipeline. |
| `testing/build_dataset_from_scan.py` | scanner text → simulator dataset | Reproducible capture conversion. |
| `testing/compact_capture.py` | broker/backend JSONL → simulator dataset | Reproducible, but writes the requested output path and keeps only last values. |

The integration tests are runtime/config-flow/sensor tests plus simulator/API
tests (`tests/test_config_flow.py`, `test_growatt_api_read_write.py`, sensor
and unique-ID tests). They are not a general register-map validator. The
broker test suite was attempted under the current environment but all tests
were blocked at setup by the repository's async `configure_event_loop` fixture
being rejected by the installed pytest/pytest-asyncio combination; this is a
test-environment issue, not evidence about live broker behaviour.

### Web research tooling

| Script | Inputs → outputs | Status |
|---|---|---|
| `doc/growatt_web/extract_ui_metadata.py` | saved `Dashboard.html`, JS and local properties files → `ui_metadata.json` | Local-only, deterministic against the mirror; extracts 15 sections and 111 commands. |
| `fetch_growatt_lang.py` | authenticated Growatt endpoint → local `.properties` files | Network/sensitive acquisition helper; do not run for this task. |
| `find_translation_usages.py` | mirror + local language files → `translation_usages.json` | Local-only deterministic scan; 550 keys have 6,221 usage records. |
| `suggest_translation_register_mapping.py` | UI metadata + consolidated reference → mapping proposals and LLM context JSON | Proposal-only fuzzy matcher. All 111 commands receive candidates, but only 10 top candidates score at least 0.9 and only 2 are exact-command matches. No accepted/rejected review store exists. |
| `prune_ui_translations.py` | currently empty | Placeholder; no effect. |

### Broker tooling

| Script | Inputs → outputs | Status |
|---|---|---|
| `tools/parse_live_log.py` | broker JSONL → bounded summaries/register statistics | Reproducible read-only parser; used on small bounded slices in this inventory. Its response-field interpretation is imperfect for logged responses, so raw JSON remains authoritative. |
| `tools/analyze_sniff_log.py` | broker JSONL → client, CRC, timeout, unusual-function and pairing report | Reproducible read-only analyzer; useful for finding Shine/TCP failures. |
| `tools/reverse_engineer_growatt.py` | broker JSONL → byte/word variability and sample-frame report | Reproducible Shine/protocol analysis helper. |
| `tools/build_sample_sets.py` | JSONL logs → append/merge `docs/data/shine_sample_sets.json` | Reproducible but mutating; current tracked sample set contains 120 samples from three 2025-09-26 logs. It is Shine-focused, not a standard TCP replay harness. |

The broker runtime is in `growatt_broker/broker.py`; `backend.py`,
`cli.py` and `simulator/` support dataset/API testing. The tests cover
simulator, backend, CLI, CRC/parse helpers, downstream timeout and standard
framing, but there is no complete capture replay or request/response
correlation test against all six local log formats.

## C. Data and artifact inventory

| Artifact | Classification | Current status / recommendation |
|---|---|---|
| Vendor PDFs and `.txt` | raw source | Keep for provenance. V1.24 tables are the main source; V3.14 is a separate older protocol family. |
| `...-tables.json` | generated raw extraction | Keep; input to overlays, graph and fallback export. |
| `growatt_registers_best_guess.json` | curated source | Keep as the current curated baseline, but its generic family semantics are not safe as a model-specific truth. |
| `growatt_registers_best_guess.v2.json` | generated schema projection | Keep as a reproducible intermediate; not the current graph input. |
| `register_catalog.json` | curated family/block catalogue | Keep; useful identity/range source, but not currently consumed by `build_register_graph.py`. |
| `register_data_scheme.json` and `..._idea.json` | schema/design | Keep the implemented scheme; the “idea” file is historical design material. |
| `growatt_register_data_types.json` | generated/manual datatype catalogue | Keep; graph input, but its generic manual entries are a known contamination risk. |
| `HA_local_registers.json` | generated runtime snapshot | Keep/regenerate when runtime mappings change. |
| `grott_register_layouts.json` | generated external-source snapshot | Keep with the Grott checkout/version; graph input. |
| OIG and inverter-to-MQTT exports | generated external-source snapshots | Keep as provenance and graph inputs; do not treat either as universal truth. |
| `overlays/*.json` | generated additive overlays | Keep for provenance, but current graph/export does not consume them. The documented promotion/conflict queue is not implemented. |
| `doc/register_graph.gpickle` | graph-derived intermediate | Graph input to consolidated export; the HA-4b rebuild supersedes the HA-4a snapshot. |
| `doc/doc/register_graph.gpickle` | duplicate/stale graph artifact | Removed in HA-4b after source search found no generator reference. |
| `consolidated_register_ref.json` + schema | graph-derived canonical cross-reference | Current broad machine-readable export; it is an output, not an input to the general pipeline. |
| `ref/REGISTERS.md`, OIG comparison | human/source-specific references | Keep as readable evidence, but label as source-specific/legacy where applicable. |
| `min_6000tl_xh_register_map.json` + `ref/MIN_6000TL_XH_REGISTER_MAP.md` | model-specific resolved view | Strongest current MIN 6000TL-XH semantic reference; intentionally separate holding/input namespaces. |
| `min_6000tl_xh_live_validation.json` | hardware evidence | Read-only FC03/FC04 capture via broker `:5021`, unit 1, with identity, telemetry and raw responses. It is evidence for this device, not all families. |
| `doc/growatt_web/` | local-only mirror/analysis | Entire directory is untracked in the integration worktree. Preserve; do not treat proposals as accepted mappings. |
| broker `docs/data/shine_sample_sets.json` | tracked derived Shine evidence | 120 samples from three local logs; useful for future correlation. |
| broker `broker-*.log` | local/partly tracked capture evidence | Six logs total, about 531 MB / 1.63 M JSONL lines. `broker-210925.log` and `broker-260925-2.log` are untracked; other listed logs are tracked. Preserve all. |

The current consolidated reference is therefore useful for broad lookup and
cross-source context, but it is not a complete validated answer for every
register. The MIN overlay and raw capture remain the authority for the live
MIN device where the broad graph has conflicting family/manual metadata.

## D. Actual register pipeline

```text
vendor PDF -> txt/tables JSON
                  ├─> curated best_guess
                  │     ├─> normalize/build_input_spec/build_datatypes
                  │     └─> best_guess.v2 + catalogue/schema projections
                  └─> vendor overlay

HA runtime ───────────────> HA_local_registers ───────┐
Grott checkout ───────────> grott_register_layouts ────┤
OpenInverter checkout ────> OIG export ────────────────┤
inverter-to-MQTT checkout -> MQTT export ──────────────┤
manual datatype catalogue ────────────────────────────┤
vendor tables + best_guess + family range rules ──────┘
                              -> build_register_graph.py
                              -> doc/register_graph.gpickle
                              -> generate_consolidated_ref.py
                              -> consolidated_register_ref.json

web mirror -> ui_metadata/translations/usages -> fuzzy mapping proposals
       (currently bypasses graph and canonical promotion)

MIN live capture + map -> validate_min_6000tl_xh_map.py
       (model-specific evidence path; bypasses broad graph)
```

The graph ingests vendor tables, curated best-guess, Grott, HA, vendor family
range rules, OIG, inverter-to-MQTT and manual datatype definitions. It creates
canonical datatype nodes by merging source attributes. If multiple values for
a canonical field exist, the graph records a `conflicts` field and leaves the
aggregated field unset; provenance/source datatype links are retained. There
is no separate conflict-resolution queue or reviewed promotion implementation.

Holding/input identity is generally explicit in graph node IDs and in the
consolidated `canonical_registers` keys (`register:holding:*` and
`register:input:*`). It is not safe to collapse by numeric address alone in
downstream consumers. The known contamination path was the generic manual
datatype catalogue: holding `3047–3048` and `3079–3082` could receive legacy
energy semantics even though the MIN device's FC03 words are battery-first/UPS
controls. HA-4b removed those overrides and added table-aware identity checks;
MIN evidence remains outside the general graph.

The current broad export is graph-derived. The fallback remains available only
as an explicit comparison artifact because it still exposes block-level source
details that are useful for audit. Web artifacts, overlays, v2, catalogue,
live evidence and MIN map do not affect either canonical path.

## E. Web scrape state

The mirror contains `Dashboard.html`, a large saved JS/HTML tree, language
properties, a second Growatt protocol PDF and helper scripts. Extraction has
already produced:

- 15 UI sections and 111 commands in `ui_metadata.json`;
- 550 translation keys with 6,221 mirror usage records;
- 111 mapping proposal records and 111 LLM-context records;
- a manually written cross-reference with explicit high/medium/low confidence
  and many unmapped/conflicting settings.

This is not “111 controls mapped”. All commands have fuzzy candidates, but
only 10 top candidates score at least 0.9 and only 2 are exact command matches.
There is no accepted/rejected mapping file, classifier, reviewer workflow or
graph edge connecting the web metadata to canonical registers. The manually
written cross-reference is valuable research evidence precisely because it
marks contradictions such as the UI's `charge_power` versus vendor holding
3047. The web evidence is currently informational and proposal-only.

## F. Broker, log and Shine research state

The six local logs include both `SHINE` and `TCP:<peer>` clients. The existing
tools recognize JSONL `REQ`/`RSP` events, CRC status, client direction,
function code, address/count and timeout events. Small bounded runs confirmed
that the logs contain standard FC03/FC04 polling, FC06/FC16 write-capable
paths, Shine function `0x20` (decimal 32), and unusual/orphan frames. The
large logs also contain many empty responses following downstream timeouts;
they are not a clean replay corpus.

Evidence for Shine is real, not inferred from titles:

- `broker-260925-set-winter.log` contains valid request
  `01 20 0000 0064 81e6` and 205-byte CRC-valid `0x20` responses;
- the same log contains normal FC03/FC04 Shine requests and responses;
- analyzer output reports orphan/unknown-function payloads (including
  function byte 0) and unmatched `0x20` requests;
- `docs/data/shine_sample_sets.json` is explicitly built from `0x20` frames;
- the logs show repeated `downstream_timeout` followed by an empty bad-CRC
  response, including for Shine and TCP clients.

The present evidence supports: standard FC03/FC04 and the proprietary/vendor
Shine `0x20` path are both present. It does not prove that decimal `0x14`
(function 20) is the same protocol: no clean, confirmed standard FC `0x14`
transaction was established. The current logs/tooling do not resolve the
payload field semantics, exact unsolicited-frame behaviour, or the relation
between Shine writes/file-transfer-like operations and inverter register
writes. The broker's reverse-engineering plan correctly keeps this as a
separate research track.

Historical framing interpretation:

| Commit | Observed change | Interpretation |
|---|---|---|
| `3ae4a21` | 20 ms floor, capped reads, buffer reset/drain, CRC search | Generic robustness changes made in a broker serving both paths; not proof they were Shine-only. |
| `5398ba2` | Shine optional/hot-pluggable | Clearly Shine/deployment driven. |
| `a877ba7` | gap floor 20 ms → 2 ms | Generic framer timing experiment; commit alone does not establish motivation. |
| `1d85223` | request-aware exact-length standard reader; TCP uses it | Directly standard TCP/RTU robustness, avoiding arbitrary CRC-valid substrings. |
| `b42445f` | retry only standard FC03/FC04 reads after silence | Directly standard TCP read resilience; writes and nonstandard Shine requests are not retried. |

The most proportional current architecture is therefore the one already
present: deterministic request-aware framing for standard TCP and the generic
gap/CRC path reserved for Shine. Do not tune or replace the Shine framer for
an MVP that has no Shine client.

## G. Runtime architecture state

`custom_components/growatt_local` uses a `DataUpdateCoordinator` and one API
layer with serial/network transports. `GrowattDevice` selects a
`DeviceTypes`-specific register dictionary, groups requested addresses into
sequences, reads holding/input tables separately, then processes raw words
into named values. `inverter_120.py` owns the TL-X input base and appends
storage/TL-XH extensions; `storage_120.py` owns storage holding/input blocks.
Other families live in `inverter_315.py` and `offgrid.py`.

Sensors and switches are separate entity-description tables. Config flow
supports serial, TCP and UDP and has the normal network device/options path.
The runtime still contains writable register methods and switch entities; the
HA-3 live validation intentionally did not use them.

Pressure points are the duplicated/overlapping family dictionaries, inherited
TL-XH/storage extensions, generic manual datatype definitions, and the fact
that runtime metadata is extracted into a snapshot but not generated from the
canonical graph. The broad knowledge base is richer than the runtime, while
the runtime can still be the source of stale or family-specific definitions.

## H. Upstream divergence

The integration remotes are:

- fork `origin`: `l4m4re/Homeassistant-Growatt-Local-Modbus`;
- upstream `upstream`: `WouterTuinstra/Homeassistant-Growatt-Local-Modbus`.

After fetching only the upstream ref for comparison (no merge or update),
`fix/min-6000xh` is 154 commits ahead and 36 commits behind
`upstream/master`. The local HEAD is `c11ed6e`; upstream/master is
`93dbda3` (`Bump manifest version`, 2025-12-13). The upstream-only history
includes storage/TL-XH fixes, AC-load/powermeter sensors, state-class changes,
and power-control fixes. These are relevant to runtime divergence, but the
large fork-local register research series is not upstream.

An upstream sync should happen before a major runtime/register redesign, but
only after preserving/reconciling the fork-local research and the live pinned
integration. It should be a separate controlled task, not mixed with web or
register consolidation.

## I. Redundancy and cleanup candidates

Do not delete anything in this inventory. The likely next cleanup decisions are:

- choose one general canonical path: graph → consolidated export; retain the
  direct fallback only until a parity check proves it unnecessary;
- declare `growatt_registers_best_guess.json` the curated source and make v2,
  overlays and consolidated output visibly derived from it, or explicitly
  migrate authority into the graph;
- keep the graph/export validation path healthy after future source changes;
- consolidate `build_input_spec.py`, `normalize_register_spec.py` and the
  datatype/build steps so in-place mutation is not confused with generation;
- implement the documented overlay promotion/conflict-review step, or remove
  that roadmap language in a later documentation task;
- add web metadata as a namespaced, proposal-only graph source only after a
  human review model exists; do not promote fuzzy mappings automatically;
- keep the MIN map/live evidence separate as a model-specific validation view;
- keep all six broker logs and the tracked Shine sample set as provenance;
  improve parsers/replay correlation before considering any derived log output
  authoritative;
- fix the broker test fixture/environment separately; it is not a reason to
  alter broker code during this inventory.

The web mirror and two broker logs are local-only/untracked and must not be
mistaken for missing upstream artifacts. Conversely, the existence of a
tracked generated JSON file does not make it authoritative.

## J. Goals A–F and next bounded task

| Goal | Done | Partial/missing | Main constraint |
|---|---|---|---|
| A. Complete register knowledge base | Vendor, community, HA and graph sources; model-specific MIN evidence; holding/input keys in current export | Firmware applicability, conflict review, family-wide semantics and graph/runtime authority are incomplete | Architecture split and generic/manual contamination |
| B. Human documentation | Vendor-derived refs, OIG comparison, MIN reference, web notes | Web proposals are not reviewed/promoted; many labels remain cryptic or contradictory | No accepted mapping/provenance review path |
| C. Hardware validation | Strong read-only MIN identity/telemetry capture through broker; deterministic validator | One device and firmware cannot validate all families; broader map is not hardware-proven | Scope of evidence, not a live-access blocker |
| D. Shine protocol | Real `0x20` captures, sample sets, analyzers and historical notes | Semantics, FC `0x14` question, write/file-transfer relation and clean replay remain unresolved | Proprietary/unsolicited traffic and incomplete pairing |
| E. Better HA integration | Working family modules, TCP config flow, sensors/switches and tests | Runtime is not generated from the validated knowledge base; family duplication and stale upstream divergence remain | Runtime/schema boundary |
| F. Avoid duplicate research infrastructure | Several useful source-specific exports and one current graph export exist | Multiple overlapping generators, stale pickle, loose overlays, web bypass and fallback path remain | No declared ownership/acceptance contract |

### Smallest sensible next task

The next bounded task should be **pipeline ownership and parity reconciliation**:

1. document and test the exact graph input set and `(table, register)` identity;
2. compare graph-derived and fallback consolidated output for a bounded set of
   representative MIN/TL-XH holding/input addresses;
3. make conflicts and source provenance visible in that comparison;
4. decide which generated files are required outputs and mark the others as
   intermediate/local evidence.

This reuses existing scripts and the existing MIN validation artifact. It does
not require more live reads, Shine work, a graph rewrite, entity expansion or
an upstream merge. Once ownership/parity is explicit, a separate upstream-sync
and runtime-consumer task can safely use the validated knowledge without adding
another parallel register map.

## Answers to the ten success questions

1. Research exists in the vendor conversion, curated map, community exports,
   HA snapshots, graph, web mirror, broker captures and MIN evidence.
2. The tooling-to-output relationships are in section B.
3. The graph-derived consolidated export is the broad current output; the
   curated best-guess and MIN map have different authority scopes.
4. Overlap is concentrated in in-place best-guess generators, graph/fallback
   exports, duplicate pickles and web/overlay bypasses.
5. Coverage is broad but semantic completeness is not established; the MIN
   model-specific map is materially stronger than the family-wide output.
6. The web scrape is substantially extracted but minimally exploited: 111
   proposal records exist, with only 10 high-scoring top candidates and no
   accepted mapping workflow.
7. Shine `0x20` is evidenced; standard FC `0x14` and full payload semantics
   remain unresolved.
8. Runtime definitions feed `HA_local_registers` and the graph, but the graph
   does not generate runtime code and runtime definitions can contaminate the
   broad manual datatype view.
9. The fork is 154 ahead/36 behind upstream/master as of this inventory.
10. The smallest next task is graph/fallback parity and ownership
    reconciliation, not another live experiment or new data representation.

## K. HA-5 controlled upstream reconciliation

HA-5 was performed on a dedicated branch, `maintenance/upstream-sync-20260905`,
created from the exact HA-4b fork baseline
`9c82748cec96d4dd35c58f9589136c731b5efdbc`. The upstream ref was fetched from
`WouterTuinstra/Homeassistant-Growatt-Local-Modbus` without changing the
parent repository or the `fix/min-6000xh` branch:

- `upstream/master`: `93dbda335815e26032f943f33c43fcf44a1fbb60`;
- merge base: `50a24849e6627647f8a37468b283f154bed986e3`;
- pre-merge divergence: fork `156` commits ahead and `36` behind;
- the branch was pushed to the fork before the merge for recovery and review.

The upstream-only history is primarily general integration maintenance: number
entities and output-power-limit support, PyModbus `device_id` naming, release
automation, state-class/powermeter/AC-load sensors, and storage/hybrid power
control fixes. It is not a Shine or broker change. The untracked local
`doc/growatt_web/` research tree has no path collision with upstream.

The merge was performed with `--no-ff`. The two content conflicts were
resolved semantically. The merged runtime retains upstream's `device_id` API
and number/sensor improvements, while preserving the fork-local MIN/TL-XH
register documentation, corrected 3000-series addresses, reactive-power and
hybrid telemetry extensions, and the HA-4b graph/export ownership. The local
typed write path was retained and now uses `device_id` consistently. The
upstream output-power-limit register is represented in the runtime snapshot;
its source disagreement with the existing manual/OpenInverter datatype is
visible in the canonical graph rather than silently flattened.

Because runtime definitions changed, `HA_local_registers.json`, the NetworkX
graph, and the graph-derived consolidated export were regenerated. The
canonical export schema and the MIN/TL-XH validator pass. Python compilation
of the integration and documentation scripts passes. The standalone
integration pytest collection remains environment-blocked by the existing
missing Home Assistant test modules (`homeassistant.helpers` through
`pytest_homeassistant_custom_component`); this was not repaired as part of the
upstream sync.

No live HA, inverter, broker, Shine, parent gitlink, or live integration
version was changed. The maintenance branch is intentionally not merged back
into `fix/min-6000xh`; it is the review point for this reconciliation.
