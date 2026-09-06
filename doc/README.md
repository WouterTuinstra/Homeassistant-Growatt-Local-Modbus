# Documentation assets

This directory collects the source specification and machine-readable material
for Growatt's “Inverter Modbus RTU Protocol v1.24”, along with generated
reference docs for the Home Assistant `growatt_local` integration.

## Authoritative register pipeline

The authoritative machine-readable route is:

```text
source JSON inputs -> doc/build_register_graph.py
                   -> doc/register_graph.gpickle
                   -> doc/generate_consolidated_ref.py
                   -> doc/consolidated_register_ref.json
```

The graph keeps register identity as `(table, register)`; holding and input
registers with the same numeric address are different records. It retains
source payloads, alternate datatypes and conflicts so disagreements remain
inspectable. OpenInverter mappings are graph inputs, while MIN live-validation
evidence and web-derived proposals remain separate evidence artefacts.

From the integration checkout, rebuild and validate the canonical export with:

```sh
python3 doc/build_register_graph.py --output doc/register_graph.gpickle
python3 doc/generate_consolidated_ref.py --validate-schema
```

`generate_consolidated_ref.py` fails if the graph is absent. Its old direct
source merge is retained only for explicit comparison:

```sh
python3 doc/generate_consolidated_ref.py --legacy-fallback --output /tmp/consolidated-legacy.json
```

That fallback is not a canonical export and is intentionally not accepted by
the graph-export schema.

The graph pickle is a NetworkX intermediate; its raw pickle hash can vary with
Python object memoisation even when nodes, edges and attributes are unchanged.
Determinism is therefore checked semantically: rebuild the graph, compare the
node/edge model and compare the consolidated JSON after removing only
`meta.generated_at` and the graph-file fingerprint.

### HA-4b parity decision

The representative holding and input audit covered the common ranges, the
TL-XH telemetry/control ranges, BDC battery registers, and non-MIN examples
such as holding `23–27`, `43`, `44` and `88`. The differences are structural:
the graph is per-register with explicit table identity, family links,
canonical/alternate datatypes and source payloads, while the fallback is
block-oriented with source summaries and legacy datatype names.

The fallback did expose useful OpenInverter register entries that the old graph
builder had kept only on a device node. Those mappings are now graph edges and
register payload provenance, including the holding `3047/3048` battery-first
controls and input `3047–3048`/`3081–3082` telemetry. The graph also retains
datatype conflicts instead of flattening them. The numeric-address-zero export
bug was fixed at the graph exporter, so holding and input `0` are retained.

The fallback is therefore retained temporarily as an explicitly noncanonical
parity/debug view (decision B), not as a second supported generation route.
No MIN live-validation data, web proposal, overlay or Shine evidence was
ingested into the graph.

## Source versus best-guess datasets

- `Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf` is the vendor
  specification we mirrored verbatim. The adjacent `.txt` and `.json` files in
  the same directory are raw artefacts from pdftotext and an early parsing
  exercise.
- Files named `*_best_guess.json` (for example `growatt_registers_best_guess.json`)
  capture our consolidated interpretation of the register map. They include
  descriptive prose, inferred ranges and other curation work that goes beyond
  what the vendor document states explicitly.
- Helper scripts such as `convert_growatt_registers_best_guess.py`, the
  catalogue in `register_catalog.json`, and the schema in
  `register_data_scheme.json` operate on the “best guess” data to produce
  canonical, schema-compliant exports used by the rest of the toolchain.

## Register catalog and data scheme

The reusable inverter-family, block and section definitions live in
`doc/register_catalog.json`. The catalogue distils the static ranges described
in the vendor PDF (augmented with community discoveries such as the 5000–5399
BDC mirrors) and supplies canonical ids, human-readable labels and provenance
notes. Each block lists its section slices inline so consumers get a concise
label plus the register start/length without chasing separate lookups.

The consolidated export produced by `generate_consolidated_ref.py` references
that catalogue and follows the schema captured in `doc/register_data_scheme.json`.
The structure mirrors the conceptual model below so every source-specific
perspective can be compared side-by-side:

- **Inverter families** – high level groupings (e.g. TLX, SPH) that enumerate
  the register blocks they support. Each family entry carries optional aliases
  and metadata but does not duplicate block contents.
- **Blocks** – contiguous address ranges (holding/input) described by a start
  register and length. Blocks embed their full section list so the hierarchy is
  self-contained and can optionally point back to catalogue ids.
- **Sections** – annotated sub-ranges inside a block. Sections list the
  register values they contain, optional child sections, and provenance links:
  `mirror_of` documents true register mirrors, while `template_instance_of`
  denotes repeated layouts (e.g. BDC slots) that reuse the same template but
  hold independent data.
- **Register values** – the atomic register descriptions shared by all
  perspectives. Every extractor must emit the base fields (id, register,
  length, unit, writable, scale, encoding hints). The canonical view extends
  this with richer prose (`tooltip`, `help`, `annotations`) and tracks sibling
  ids for alternate descriptions (HA, Grott, inverter-to-mqtt, vendor, etc.).
- **Canonical register catalogue** – `canonical_register_values` is simply the
  list of register value ids we treat as authoritative. Sibling entries reference
  these ids so conflicts and gaps can be highlighted automatically.

Keeping the hierarchy explicit like this lets the graph builder reason about
mirrors, repeated templates, and per-source divergences without duplicating
payloads across files.

## Holding BDC registers 5000-5399

On page 47 of the Protocol v1.24 pdf document 10 sets of registers are described
for up to 10 parallel BDC's, with for each BDC the same set of registers as
holding register range 3085 to 3124 for BDC1. The catalogue entry
`holding_bdc_5000_5399` records this mirror range so downstream tooling can
link BDC slots back to the canonical TL-XH definitions.

## UI metadata and translation enrichment

To complement the raw Modbus tables we mirrored the Growatt web portal and
normalised its configuration UI into machine-readable metadata. The extractor
(`doc/growatt_web/extract_ui_metadata.py`) walks rendered HTML snapshots and the
companion JavaScript bundles to capture control groups, option identifiers and
context such as tooltips. During extraction we also ingest the vendor-provided
language bundles (`doc/growatt_web/lang/language_*.properties`), converting them
into JSON blobs that travel alongside each UI command. This gives every control
access to multi-lingual labels and helper text without needing to load the web
app at runtime.

These artefacts (`doc/growatt_web/ui_metadata.json` and supporting
translation maps) let us cross-reference UI concepts with the consolidated
register catalogue. In practice this means we can enrich register entries with
human-friendly labels from the vendor UI, verify that we are covering the same
controls exposed on the web portal, and ship descriptive strings in multiple
languages for Home Assistant’s frontend. The same pipeline also highlights
translation keys that are only resolved dynamically online, guiding further
instrumentation work to close any remaining gaps.

## Grott register layouts as a supplemental source

The `external/grott` project intercepts the ShineWiFi/ShineLAN link to
`server.growatt.com` and bundles a large set of decoded record layouts. The
root-level layout file `external/grott/T06NNNNXMOD.json` and the variants under
`external/grott/examples/Record Layout/` map Growatt field names onto Modbus
registers, offsets, scaling factors (`divide`) and payload widths. During
runtime Grott merges those JSON fragments with the baked-in layouts from
`external/grott/grottconf.py`, giving a single `recorddict` that covers MOD,
MAX, TL3, MIN, SPH, SPA and SPF families. Only the MOD layout (`T06NNNNXMOD`) is
annotated with explicit register numbers at the moment, so the other families
still need their addresses inferred from `grottconf.py`, the Grott wiki or live
captures. Even so the MOD mapping provides a rich seed dataset for closing the
gaps that remain in our vendor PDF scrape.

Each entry in Grott's `recorddict` carries consistent metadata so the field can be decoded without Grott itself:

- `value`: byte offset from the start of the decrypted payload
- `length`: number of payload bytes that belong to the field (two bytes per Modbus register)
- `type`: encoding hint—`num` for unsigned integers, `numx` for signed values, `text`/`hex` for raw payload copies and enum helpers for bitmaps
- `divide`: scaling factor applied after parsing to convert the integer into engineering units
- `register`: optional absolute Modbus register when Grott already knows the address
- `incl`: whether Grott publishes the field by default in its MQTT/JSON output

To pull this data into our reference pipeline we can:

- Export Grott’s combined `recorddict` (either by importing `grottconf.Conf`
  with `includeall=True` or by walking the JSON files directly) and serialise it
  into a neutral cache such as `doc/grott_register_layouts.json`. Capture the
  layout id, field key, byte offset (`value`), payload width (`length`), type,
  scaling factor, any pre-defined `register` hint and whether Grott marks the
  field as user-facing (`incl`).
- Derive register blocks for layouts that lack explicit addresses by matching
  the byte offsets to the ranges described in
  `external/grott/documentatie/registers.md`. Every two bytes equate to one
  Modbus register, so a `length` of 2 advances the register pointer by 1 while a
  `length` of 4 spans two registers. Storing the inferred block id alongside the
  field makes it easy to stitch the Grott data onto our existing
  `RegisterRange`/`Register` nodes.
- Export Grott’s MQTT topics from
  `external/grott/examples/Home Assistent/grott_ha.py` and the accompanying YAML
  blueprints so each Grott field records the topic fragment it publishes to.
  That cross-links community MQTT names with our Home Assistant and broker
  datasets.
- Normalise Grott field names and scales so they match our conventions
  (`snake_case` identifiers, decimal scaling expressed in powers of ten, flag
  fields tagged as enums/bitmaps) and map repeated enumerations to our canonical
  data-type catalogue.
- Extend `doc/generate_consolidated_ref.py` to ingest the Grott export, emit
  `source: "grott"` annotations and surface conflicts where Grott deviates from
  the v1.24 protocol PDF or the HA integration.
- Feed Grott’s human-facing notes from `external/grott/documentatie/registers.md`
  (or the `grott.wiki` checkout) into the enrichment step so the consolidated
  register reference inherits the community-discovered descriptions. Keep the
  provenance edge so reviewers can jump directly back to the Grott source.
- Optional: replay captured ShineWiFi traffic through
  `external/grott/tools/grottsniffer.py` or `grottserver.py` to validate scaling
  and highlight dynamic registers that the static PDF omits.

### Mapping offsets to Modbus registers

The Grott layouts describe payloads as byte streams. When a layout does not
ship a direct `register` number we can still compute it from the `value`
offset:

1. Identify the logical block (e.g. holding 0–124 or 3000–3124) from the Grott
   documentation or the vendor PDF.
2. Divide the offset delta (`value - block_start_byte`) by two to obtain the
   register index inside that block.
3. Add the index to the block’s starting register to get the canonical Modbus
   address, taking into account that 32-bit (`length` == 4) fields consume two
   consecutive registers.
4. Record mirrored ranges (such as MOD 3000–3124 reusing the content from
   holding 0–124) as explicit edges in the knowledge graph so descriptions and
   data-type hints can propagate automatically.

Capturing this derivation once in the export script keeps the downstream graph
and JSON exports free of register arithmetic and makes future Grott updates
a simple data refresh.

### Translation and explanation enrichment

Grott names are close to the Growatt UI terminology but not identical, and the
mirrored web portal contains far richer multilingual descriptions than we can
match with heuristics alone. After the Grott export is in place:

1. Generate structured prompt payloads that pair each Grott field (name, block,
   notes, MQTT topic, observed value range) with candidate translation entries
   from `doc/growatt_web/ui_metadata.json`.
2. Run the existing scorer in `doc/growatt_web/suggest_translation_register_mapping.py`
   for a fast baseline and let an opt-in `llm_proposer` re-rank difficult cases
   (e.g. explanatory paragraphs such as `cfd_When_the_solar_energy_is_sufficient`).
3. Emit LLM suggestions to `doc/grott_ui_mapping_proposals.json` with full
   context so reviewers can accept or reject them and promote confirmed matches
   back into the knowledge graph.
4. Reuse the same context bundles to summarise Grott-only notes (for example the
   SPA/SPH battery mode explanations) and feed them into the consolidated
   register reference as human-readable `explanation` fields.

Once the Grott export slot exists it becomes straightforward to keep our
consolidated register reference aligned with community discoveries: updating the
Grott checkout and rerunning the import pipeline will flag new or changed
addresses alongside the vendor and Home Assistant views we already collect.

## Incremental Enrichment Plan

We now treat `register_catalog.json` + `growatt_registers_best_guess.json` as the
authoritative baseline and layer every other source on top via additive
metadata. Each extractor produces a source-specific overlay that only carries
external identifiers, labels and explanatory text; core numerical fields remain
anchored in the best-guess dataset unless a reviewed conflict replaces them.

- **Overlay artefacts** – every extractor writes `doc/overlays/<source>_overlay.json`
  keyed by canonical register id. Payloads append identifiers (`external_ids`),
  descriptive snippets (`external_notes`) and optional enum/bitfield candidates
  under a per-source namespace. Nothing in the overlay mutates the canonical
  value directly.
- **Promotion step** – `doc/promote_overlays.py` ingests overlays, merges any
  conflict-free metadata into `growatt_registers_best_guess.json`, refreshes the
  derived `growatt_registers_best_guess.v2.json`, and writes unresolved items to
  `doc/conflicts/pending/<source>.json`.
- **Conflict handling** – reviewers triage the pending list, capture decisions
  in `doc/conflicts/resolved.json` (e.g. “prefer HA label”, “keep vendor unit”),
  and rerun the promoter. The promoter also honours the resolution file when
  regenerating the dataset.
- **Catalog alignment** – extractors must map every address to an existing block
  id; if no block fits, they emit a warning so we can extend the catalog before
  merging. Section comparisons follow the same pattern introduced in
  `convert_growatt_registers_best_guess.py` (full match, partial coverage, or
  “not catalogued”).
- **Provenance retention** – merged metadata always records its origin in
  `register_values[..]["metadata"]["sources"]` so downstream tooling can filter
  or display source-specific details without parsing the overlays again.

This incremental pipeline keeps the best-guess document authoritative, captures
all the human-friendly identifiers we need for Grott/UI matching, and ensures
that disagreements remain visible until explicitly resolved.

### Agent Task Suggestions

- Wire up `doc/extract_ha_overlay.py` that parses the Home Assistant integration
  (entities, service names, enum labels) and emits the HA overlay JSON described
  above, including block warnings when unknown registers appear.
- Implement `doc/promote_overlays.py` with support for the overlay merge rules,
  conflict queue generation and automatic regeneration of the `.v2` export.
- Draft `doc/conflicts/review_helper.py` that lists outstanding conflicts grouped
  by source, shows canonical versus candidate values, and lets a reviewer write
  decisions back into `doc/conflicts/resolved.json`.
- Extend `convert_growatt_registers_best_guess.py` (or a sibling report script)
  to ingest overlays for read-only reporting so we can diff canonical entries
  with their aggregated external identifiers in one place.
## Grott export and semantic matching roadmap

The long-term goal is a reproducible workflow that keeps deterministic sources
and any LLM-assisted annotations side by side so we can iterate safely. The
proposed milestones for a coding agent are:

- Build `doc/export_grott_layouts.py` that imports `external/grott/grottconf`
  (with `includeall=True`) and emits `doc/grott_register_layouts.json`.
  Each record should capture the layout id, field key, byte offset, length,
  type, scale, inferred register range (when present) and the MQTT topic pattern
  Grott would publish for that field.
- Wire `doc/generate_consolidated_ref.py` to ingest the Grott export so this
  becomes another structured source in `consolidated_register_ref.json`. Keep
  per-field provenance so conflicts across vendor/HA/Grott data are visible.
- Extend the translation matcher to accept multiple proposal backends. The
  existing token heuristics stay as the fast default while an optional
  `llm_proposer` writes structured suggestions (field ids, translation keys,
  prompt context, confidence) to `doc/grott_ui_mapping_proposals.json` for
  manual or automated review.
- Add validation utilities (CLI scripts or tests) that diff the latest Grott
  export against the stored JSON, flagging new layouts or register shifts.
- Document a review loop for LLM-derived matches so approved mappings can be
  promoted into the consolidated reference with audit trails.


## Knowledge-graph consolidation strategy

We now have multiple, partially overlapping register descriptions:

- Vendor PDF artefacts (`Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English`)
  provide the raw tables direct from the manufacturer.
- Curated best-guess dataset (`growatt_registers_best_guess.json`) with richer
  narratives and inferred structure. `convert_growatt_registers_best_guess.py`
  turns this into the schema-aligned `growatt_registers_best_guess.v2.json`.
- Grott payload layouts that fix byte offsets and serialised data types for the
  telemetry stream.
- Home Assistant, OpenInverter and inverter-to-MQTT metadata that provide MQTT
  keys, entity names and inferred data types.
- Translation inventories from the mirrored web portal, many of which describe
  individual settings or telemetry points.

To keep provenance and reconcile conflicts we will move toward a graph-backed
consolidation layer. The milestones for that effort are:

- **Graph substrate** – prototype a NetworkX-based loader that creates explicit
  nodes for `Register`, `RegisterBlock`, `GrottField`, `DataType`,
  `TranslationKey`, `MQTTTopic`, `HAEntity` and `SourceDocument`. Each node
  must record its origin (file path, SHA checksum, export timestamp).
- **Data ingestion** – extend the loader so every source is ingested into the
  graph rather than merged lossily. Edges capture the relationships we rely on:
  `REGISTER_IN_BLOCK`, `BLOCK_MIRRORS_BLOCK`, `FIELD_MAPS_BLOCK`,
  `REGISTER_HAS_DATATYPE`, `REGISTER_REFERENCED_BY`, `DESCRIPTION_SOURCE` and
  `TRANSLATION_DESCRIBES`.
- **Data-type normalisation** – derive canonical data-type nodes from width,
  signedness, engineering units and scaling factors. Map all source-specific
  descriptors (Grott divides, HA `SIZE_32BIT` hints, MQTT multipliers, vendor
  units) onto those canonical nodes so equivalent encodings are coalesced via
  explicit edges.
- **Block reasoning** – encode mirrored and overlapping ranges (e.g. MOD
  3000–3124 mirroring input 0–124 for XH devices) so descriptions and data-type
  hints can be propagated automatically between blocks.
- **Translation filtering** – classify translation keys before matching. Store
  only those that plausibly describe telemetry/registers; keep UI chrome in a
  separate partition to avoid polluting the matching pipeline.
- **Derived exports** – rebuild `consolidated_register_ref.json` and related
  artefacts from graph traversals. Conflicts between sources stay visible as
  parallel edges rather than being overwritten. Provide dedicated export hooks
  for LLM prompt context, translation review queues and human-readable reports.
- **Tooling and validation** – add CLI helpers to regenerate the graph,
  summarise conflicts, diff successive runs and emit targeted review checklists
  (e.g. “new Grott fields with no matching register”, “translation keys without
  links”).

This shift lets us keep every source authoritative in its own right while still
delivering a single, reconciled register reference downstream. The immediate
next steps are:

- **Graph loader prototype** – create `doc/build_register_graph.py` that ingests
  the vendor tables, Grott export, HA/OpenInverter/MQTT artefacts and writes a
  NetworkX graph (pickle/GraphML) with provenance captured on every node/edge.
- **Block and data-type normalisation** – add helper modules that map Grott
  fields to canonical register blocks, encode mirrored ranges and derive
  canonical data-type nodes from the various source vocabularies.
- **Graph-backed exports** – port `generate_consolidated_ref.py` (and related
  scripts) to consume the graph representation rather than re-parsing source
  JSON. Keep the existing JSON output format stable while sourcing data from the
  graph API.
- **Translation classifier** – introduce a new tool
  (`doc/growatt_web/classify_translations.py`) that tags translation keys as
  telemetry-related or UI-only, producing an allowlist for the matcher.
- **Validation utilities** – implement graph-diff and conflict reports under
  `tools/` so changes in any source surface as actionable review items.


## Files

- `Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf` – original vendor
  specification. This is the canonical source for all other artefacts here
  (with companion `.txt` and `.json` helpers generated from it).
- `growatt_registers_best_guess.json` – curated “best guess” interpretation of
  the register map that aggregates descriptive text and inferred structure.
- `Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English-tables.json` – raw
  per-row table export retained for traceability/debugging.
- `HA_local_registers.json` – machine-generated snapshot of the integration's
  register mappings, used when cross-referencing coverage (regenerated via
  `extract_HA_local_registers.py`).
- `render_register_spec.py` – optional Markdown renderer for ad-hoc documentation
  previews. The generated file is not versioned.
- `normalize_register_spec.py` – cleans the spec JSON and enriches it with
  integration attribute metadata.
- `build_register_data_types.py` – derives reusable data type/scale definitions
  from the integration mapping.
- `growatt_register_data_types.json` – output catalogue produced by
  `build_register_data_types.py`.
- `growatt_registers_best_guess.v2.json` – schema-compliant projection of the
  best-guess dataset generated via `python convert_growatt_registers_best_guess.py`.
- `register_catalog.json` – canonical inverter family, block and section
  catalogue distilled from the vendor PDF and Grott observations.

## Updating / regenerating the documentation

The JSON files were produced by parsing the PDF tables and normalising them
into register records. The Markdown output is rendered programmatically to stay
in sync with those JSON sources.

1. Update `growatt_registers_best_guess.json` as needed (or refresh it from the
   vendor artefacts using the helper scripts in this directory).
2. Regenerate `HA_local_registers.json` with `python extract_HA_local_registers.py`
   when the integration mapping changes.
3. Run `python normalize_register_spec.py` to tidy the JSON and attach updated
   attribute mappings.
4. Run `python build_register_data_types.py` if the type catalogue needs to be
   refreshed.
5. (Optional) Run `python render_register_spec.py` from this directory (or inside
   the `script/bootstrap` virtualenv) to emit a Markdown snapshot for review.
6. Run `python convert_growatt_registers_best_guess.py` if you need the
   schema-compliant `growatt_registers_best_guess.v2.json` to stay in sync.
7. Commit the updated JSON artefacts (Markdown snapshots are for local review only).

Regenerating each time keeps the derived artefacts and the source JSON in sync.
