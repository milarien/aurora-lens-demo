"""CLI demo for evidence authority demotion."""

from __future__ import annotations

import json

from .evidence_authority import EvidenceInput, evaluate_evidence


DEMO_CASES = [
    EvidenceInput(
        evidence_id="ev-001",
        freshness_status="current",
        authority_status="verified",
    ),
    EvidenceInput(
        evidence_id="ev-002",
        freshness_status="stale",
        authority_status="verified",
    ),
    EvidenceInput(
        evidence_id="ev-003",
        freshness_status="expired",
        authority_status="verified",
    ),
    EvidenceInput(
        evidence_id="ev-004",
        freshness_status="current",
        authority_status="revoked",
    ),
]


def main() -> None:
    print("Aurora-Lens Public Verification Slice")
    print("This is a bounded runnable proof of evidence authority demotion, not the full Aurora-Lens architecture.")
    print()

    for evidence in DEMO_CASES:
        result = evaluate_evidence(evidence)
        print(json.dumps(result.to_record(), indent=2))
        print()


if __name__ == "__main__":
    main()
