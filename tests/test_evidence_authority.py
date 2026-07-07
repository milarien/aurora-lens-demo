import pytest

from aurora_lens_demo.evidence_authority import (
    AuthorityState,
    EvidenceInput,
    LensAction,
    evaluate_evidence,
)


def test_authoritative_evidence_maps_to_pass() -> None:
    evidence = EvidenceInput(
        evidence_id="MC-001",
        freshness_status="current",
        authority_status="verified",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.AUTHORITATIVE
    assert result.mapped_action == LensAction.PASS
    assert result.demotion_reason is None


def test_stale_evidence_maps_to_force_revise() -> None:
    evidence = EvidenceInput(
        evidence_id="MC-002",
        freshness_status="stale",
        authority_status="verified",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.SIGNAL_ONLY
    assert result.mapped_action == LensAction.FORCE_REVISE
    assert "stale" in result.demotion_reason.lower()


def test_expired_evidence_maps_to_contain() -> None:
    evidence = EvidenceInput(
        evidence_id="MC-003",
        freshness_status="expired",
        authority_status="verified",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.REQUIRES_REVALIDATION
    assert result.mapped_action == LensAction.CONTAIN
    assert "expired" in result.demotion_reason.lower()


def test_revoked_evidence_maps_to_hard_stop() -> None:
    evidence = EvidenceInput(
        evidence_id="MC-004",
        freshness_status="current",
        authority_status="revoked",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.INADMISSIBLE
    assert result.mapped_action == LensAction.HARD_STOP
    assert "revoked" in result.demotion_reason.lower()


def test_unverified_evidence_maps_to_force_revise() -> None:
    evidence = EvidenceInput(
        evidence_id="MC-005",
        freshness_status="current",
        authority_status="unverified",
    )
    result = evaluate_evidence(evidence)
    assert result.authority_state == AuthorityState.SIGNAL_ONLY
    assert result.mapped_action == LensAction.FORCE_REVISE
    assert "unverified" in result.demotion_reason.lower()


def test_typo_in_freshness_status_fails_closed() -> None:
    evidence = EvidenceInput(
        evidence_id="BAD-001",
        freshness_status="currrent",
        authority_status="verified",
    )
    with pytest.raises(ValueError, match="Unrecognised evidence input") as exc_info:
        evaluate_evidence(evidence)
    message = str(exc_info.value)
    assert "currrent" in message
    assert "verified" in message


def test_typo_in_authority_status_fails_closed() -> None:
    evidence = EvidenceInput(
        evidence_id="BAD-002",
        freshness_status="current",
        authority_status="verifed",
    )
    with pytest.raises(ValueError, match="Unrecognised evidence input") as exc_info:
        evaluate_evidence(evidence)
    message = str(exc_info.value)
    assert "current" in message
    assert "verifed" in message


def test_audit_records_contain_required_fields() -> None:
    evidence = EvidenceInput(
        evidence_id="MC-001",
        freshness_status="current",
        authority_status="verified",
    )
    record = evaluate_evidence(evidence).to_record()
    required_fields = {
        "evidence_id",
        "authority_state",
        "freshness_status",
        "authority_status",
        "demotion_reason",
        "mapped_action",
    }
    assert all(field in record for field in required_fields)
