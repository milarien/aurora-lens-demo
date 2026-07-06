# Aurora-Lens: Evidence Authority Demo

Aurora-Lens governs AI systems at the execution boundary. Nothing becomes a consequence until it clears admissibility. This repository demonstrates one behaviour: **evidence that is stale, expired, or revoked cannot carry decision authority**.

A live interactive demo is available at [aurora-lens.ai/demo](https://aurora-lens.ai/demo).

## The behaviour

Before a decision is authorised to proceed, Aurora-Lens classifies the evidence behind it:

| Evidence state | Authority | Lens action |
|---|---|---|
| Current, verified | Authoritative | `PASS` |
| Stale | Signal only; decision must be revised | `FORCE_REVISE` |
| Expired | Held until revalidated | `CONTAIN` |
| Revoked | Inadmissible | `HARD_STOP` |

Demoted evidence does not disappear. It becomes a contextual signal, but it can no longer drive the decision.

## Run it

```
pip install -e ".[dev]"
python -m aurora_lens_demo.demo
python -m pytest -q
```

Requires Python 3.12.

## Scope

This is a bounded public demonstration of one admissibility behaviour. The full Aurora-Lens runtime is not included.

Authored by Margaret Stokes.