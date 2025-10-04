# AI assistance notes

The artefacts in this folder were generated with the help of an AI coding
assistant.  The workflow is scripted (`render_register_spec.py`) so future
changes can be reproduced deterministically by running the tool against the
canonical JSON data.

We are now moving toward a knowledge-graph backed consolidation pipeline. Code
that populates the graph, reconciles sources or exports derived artefacts should
continue to live in reproducible CLI tooling (`doc/` or `tools/`) so the graph
can always be regenerated from the raw JSON sources.

### Current tasks for agents

1. Prototype `doc/build_register_graph.py` to ingest all existing JSON sources
   into a NetworkX graph with provenance attributes.
2. Extend the prototype with block-mirroring logic and canonical data-type
   normalisation helpers.
3. Update `doc/generate_consolidated_ref.py` to read from the graph instead of
   direct JSON inputs while preserving the output schema.
4. Add `doc/growatt_web/classify_translations.py` to label translation keys and
   produce allow/deny lists for the matcher.
5. Deliver validation/diff utilities under `tools/` that compare successive
   graph builds and highlight conflicting metadata.
