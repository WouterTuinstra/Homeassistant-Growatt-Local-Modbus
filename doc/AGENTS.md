# AI assistance notes

The artefacts in this folder were generated with the help of an AI coding
assistant.  The workflow is scripted (`render_register_spec.py`) so future
changes can be reproduced deterministically by running the tool against the
canonical JSON data.

The register reference now uses the knowledge graph as its authoritative
consolidation pipeline. Code that populates the graph, reconciles sources or
exports derived artefacts must remain in reproducible CLI tooling (`doc/` or
`tools/`) so the graph can always be regenerated from the raw JSON sources.

The supported route is `build_register_graph.py` followed by
`generate_consolidated_ref.py --validate-schema`. Register identity is always
the pair `(table, register)`; never key holding and input registers by their
numeric address alone. Source payloads, alternate datatypes and conflicts must
remain inspectable in the graph export.

The direct JSON merge in `generate_consolidated_ref.py` is a named legacy
fallback for comparison only. It requires an explicit output path and must not
silently replace the graph-derived export. Web metadata, overlays and MIN
live-validation evidence are not graph inputs unless a later task explicitly
migrates them with provenance.

### Current tasks for agents

1. Keep `doc/build_register_graph.py` reproducible and preserve source
   provenance, including explicit OpenInverter register mappings.
2. Keep block mirroring and canonical datatype conflict reporting table-aware.
3. Keep `doc/generate_consolidated_ref.py` graph-only by default and validate its
   output with `doc/consolidated_register_ref.schema.json`.
4. Treat web metadata, overlays and live MIN evidence as separate enrichment or
   validation work until a task migrates them explicitly.
5. Add future graph diff tooling only when it preserves the same identity and
   provenance rules.
