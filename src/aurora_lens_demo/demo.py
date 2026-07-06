"""CLI demo for evidence authority demotion."""

from __future__ import annotations

import json

from .evidence_authority import EvidenceInput, evaluate_evidence


DEMO_CASES = [
    EvidenceInput(
        evidence_id="MC-001",
        freshness_status="current",
        authority_status="verified",
    ),
    EvidenceInput(
        evidence_id="MC-002",
        freshness_status="stale",
        authority_status="verified",
    ),
    EvidenceInput(
        evidence_id="MC-003",
        freshness_status="expired",
        authority_status="verified",
    ),
    EvidenceInput(
        evidence_id="MC-004",
        freshness_status="current",
        authority_status="revoked",
    ),
]

CASE_DESCRIPTIONS = {
    "MC-001": "The evidence may support the decision.",
    "MC-002": "The evidence is demoted to contextual signal. The decision must be revised or supported by current evidence.",
    "MC-003": "The system contains the decision path until the evidence is revalidated.",
    "MC-004": "The evidence is inadmissible for consequence-bearing reliance.",
}

CASE_HEADERS = {
    "MC-001": "Current verified evidence",
    "MC-002": "Stale evidence",
    "MC-003": "Expired evidence requiring revalidation",
    "MC-004": "Revoked authority",
}


def main() -> None:
    print("Aurora-Lens Demo")
    print("Evidence Authority Demotion")
    print()
    print("This bounded demo shows one governance behaviour: evidence that is stale, ")
    print("expired, or no longer authorised cannot carry consequence-bearing authority.")
    print()
    print("Scenario frame:")
    print("A system is asked whether a maintenance record can support an operational decision.")
    print("Aurora-Lens checks the evidence authority state before allowing the record ")
    print("to support consequence.")
    print()

    results = []
    for idx, evidence in enumerate(DEMO_CASES, start=1):
        result = evaluate_evidence(evidence)
        results.append(result)
        
        print(f"CASE {idx} - {CASE_HEADERS[result.evidence_id]}")
        print(f"Evidence: Maintenance certificate {result.evidence_id}")
        print(f"Freshness: {result.freshness_status}")
        print(f"Authority: {result.authority_status}")
        print(f"Decision: {CASE_DESCRIPTIONS[result.evidence_id]}")
        print(f"Mapped action: {result.mapped_action.value}")
        print()

    print("Audit-style records:")
    for result in results:
        print(json.dumps(result.to_record(), sort_keys=True))


if __name__ == "__main__":
    main()
