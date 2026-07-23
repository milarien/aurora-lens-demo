# Aurora-Lens Public Demo

Aurora-Lens is a deterministic machine-reasoning governance architecture that controls whether a candidate output, determination, action, interpretation, or state transition may proceed to delivery, execution, reliance, or other consequence.

The model or other output-generating system is non-authoritative. Commitment authority remains with the Aurora-Lens governance layer.

The governing invariant is:

> Commitment is permitted only when applicable admissibility conditions are satisfied.

Where admissibility is not satisfied, Aurora-Lens produces a governed non-commitment outcome, including:

- FORCE_REVISE
- CONTAIN
- HARD_STOP
- constrained clarification
- escalation
- maintained unresolved state
- terminal refusal

This repository provides bounded public demonstration surfaces for that architecture. It does not contain the production Aurora-Lens runtime.

## Interactive Demo

The repository root hosts the public interactive demo.

Open the deployed GitHub Pages site at the repository root, or open `index.html` locally using a static file server.

The demo calls the public Aurora-Lens API at:

`https://aurora-lens.ai/v1/...`

The public API is intentionally capacity-limited. A `429` response means current public capacity has been exhausted. Wait briefly and retry, or begin a new demo session.

The interactive demo demonstrates:

- pre-consequence admissibility evaluation
- governed release and non-release
- persistent session state
- PASS / FORCE_REVISE / CONTAIN / HARD_STOP outcomes
- audit and verification surfaces
- model output treated as a non-authoritative candidate

## Local CLI Walkthrough

A separate pedagogical CLI provides synthetic, deterministic walkthroughs of selected governance behaviours.

```bash
pip install -e ".[dev]"
python -m aurora_lens_demo.demo
python -m pytest -q
```

Requires Python 3.12.

The CLI does not call the hosted API and does not include the production engine.

## Repository Boundaries

This repository does not include:

- production Aurora-Lens source
- the private runtime package or wheel
- private deployment configuration
- private infrastructure origins
- unrestricted API access
- local production evaluation backends

Cloning this repository does not grant access to the production runtime or any commercial licence.

## Architecture

Aurora-Lens may be deployed in three forms:

1. Full-stack, receiving structured conceptual state from a reasoning-construction layer.
2. Reduced runtime, interposed between an application and a model interface.
3. Hybrid, receiving any combination of structured state, evidence, authority, policy, freshness, source, or consequence metadata.

Across all forms, the same admissibility invariant applies.

## Provenance

Aurora-Lens was created and authored by Margaret Stokes.

The architecture is supported by Australian provisional patent filings beginning 27 November 2025, including admissibility-controlled epistemic governance filed 19 December 2025 and reduced runtime governance deployment filed 1 July 2026.

A US nonprovisional application covering the integrated architecture and reduced runtime deployment was filed on 19 July 2026.

Public demonstrations, repository records, publications, and cryptographic provenance materials provide additional dated evidence of development and disclosure.

## Website

Project, architecture, licensing, and contact information:

`https://aurora-lens.ai`
