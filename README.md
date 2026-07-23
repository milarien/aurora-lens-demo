# Aurora-Lens public demo

Bounded public demonstration surfaces for Aurora-Lens. This repository is **not** the production Aurora-Lens runtime.

## Interactive demo (this deployment)

The **root** of this repository / GitHub Pages deployment is the full interactive demo:

- Open the hosted demo at the repository Pages URL (root `/` → `index.html`).
- Or open `index.html` locally with any static file server (or your browser).

Evaluations call Margaret’s **capacity-bounded** public API at:

`https://aurora-lens.ai/v1/...`

That API is intentionally rate- and capacity-limited. Service capacity may occasionally be exhausted (`429`); wait and try again, or start a new demo session.

This client does **not** include:

- production Aurora-Lens source
- a private runtime wheel
- Railway or other private origins
- local evaluation backends

**Cloning this repository does not grant production source, unrestricted API access, or a licence to the private runtime.**

## CLI evidence walkthrough (local)

A separate pedagogical CLI demonstrates evidence-authority demotion on synthetic cases:

```bash
pip install -e ".[dev]"
python -m aurora_lens_demo.demo
python -m pytest -q
```

Requires Python 3.12. The CLI does not call the hosted API and does not ship the production engine.

## Scope

Authored by Margaret Stokes. Marketing and product pages live at [aurora-lens.ai](https://aurora-lens.ai).
