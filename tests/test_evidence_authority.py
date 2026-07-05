from aurora_lens_demo.evidence_authority import (
    AuthorityState,
    EvidenceInput,
    LensAction,
    evaluate_evidence,
)


def test_authoritative_evidence_maps_to_pass() -> None:
    evidence = EvidenceInput(
        evidence_id="ev-001",
        freshness_status="current",
        authority_status="verified",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.AUTHORITATIVE
    assert result.mapped_action == LensAction.PASS
    assert result.demotion_reason is None


def test_stale_evidence_maps_to_force_revise() -> None:
    evidence = EvidenceInput(
        evidence_id="ev-002",
        freshness_status="stale",
        authority_status="verified",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.SIGNAL_ONLY
    assert result.mapped_action == LensAction.FORCE_REVISE
    assert "stale" in result.demotion_reason.lower()


def test_expired_evidence_maps_to_contain() -> None:
    evidence = EvidenceInput(
        evidence_id="ev-003",
        freshness_status="expired",
        authority_status="verified",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.REQUIRES_REVALIDATION
    assert result.mapped_action == LensAction.CONTAIN
    assert "expired" in result.demotion_reason.lower()


def test_revoked_evidence_maps_to_hard_stop() -> None:
    evidence = EvidenceInput(
        evidence_id="ev-004",
        freshness_status="current",
        authority_status="revoked",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.INADMISSIBLE
    assert result.mapped_action == LensAction.HARD_STOP
    assert "revoked" in result.demotion_reason.lower()


def test_unverified_evidence_maps_to_force_revise() -> None:
    evidence = EvidenceInput(
        evidence_id="ev-005",
        freshness_status="current",
        authority_status="unverified",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.SIGNAL_ONLY
    assert result.mapped_action == LensAction.FORCE_REVISE
    assert "unverified" in result.demotion_reason.lower()
