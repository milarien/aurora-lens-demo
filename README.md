# Aurora-Lens Demo

This repository is a limited public demonstration of one Aurora-Lens governance behaviour: demotion of stale or insufficiently authorised evidence from consequence-bearing authority to contextual signal.

It is not the full Aurora-Lens architecture.

It does not include the full PEF substrate, full Lens/Governor runtime, production audit system, corpus layer, deployment system, or commercial implementation.

The purpose of this repository is to make one bounded admissibility behaviour inspectable and testable.

## What This Demo Shows

- Evidence enters an admissibility evaluation.
- Evidence is classified into one of four authority states: `authoritative`, `signal_only`, `requires_revalidation`, or `inadmissible`.
- These states map to Lens outcomes: `PASS`, `FORCE_REVISE`, `CONTAIN`, or `HARD_STOP`.
- Stale or insufficiently authorised evidence is demoted from authority to signal.
- A minimal audit-style record is emitted for each evaluation.

## What This Demo Does Not Include

- Full PEF state substrate or persistence
- Production Lens/Governor runtime orchestration
- Real corpus layer or evidence registries
- Production policy engine or private rule taxonomies
- Commercial audit schemas or cryptographic chain-of-custody

## Quickstart (Windows PowerShell)

```powershell
cd aurora-lens-demo
python -m compileall src tests -q
python -m pytest -q
python -m aurora_lens_demo.demo
```

## Expected Demo Output

Running the demo will show four cases of evidence evaluation, each demonstrating a different authority state and its corresponding mapped outcome.

```json
{
  "evidence_id": "ev-001",
  "authority_state": "authoritative",
  "freshness_status": "current",
  "authority_status": "verified",
  "demotion_reason": null,
  "mapped_action": "PASS"
}
```

## Test Command

```powershell
python -m pytest -q
```

## Authorship

Aurora-Lens was authored by Margaret Stokes.

This demo is provided for inspection and evaluation of the bounded behaviour only.
