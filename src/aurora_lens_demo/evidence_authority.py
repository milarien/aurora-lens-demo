"""Bounded demo of evidence authority demotion logic.

This module demonstrates the public behavioural invariant: demoting stale or
insufficiently authorised evidence from authority to contextual signal.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AuthorityState(str, Enum):
    AUTHORITATIVE = "authoritative"
    SIGNAL_ONLY = "signal_only"
    REQUIRES_REVALIDATION = "requires_revalidation"
    INADMISSIBLE = "inadmissible"


class LensAction(str, Enum):
    PASS = "PASS"
    FORCE_REVISE = "FORCE_REVISE"
    CONTAIN = "CONTAIN"
    HARD_STOP = "HARD_STOP"


AUTHORITY_TO_ACTION = {
    AuthorityState.AUTHORITATIVE: LensAction.PASS,
    AuthorityState.SIGNAL_ONLY: LensAction.FORCE_REVISE,
    AuthorityState.REQUIRES_REVALIDATION: LensAction.CONTAIN,
    AuthorityState.INADMISSIBLE: LensAction.HARD_STOP,
}


@dataclass(frozen=True)
class EvidenceInput:
    evidence_id: str
    freshness_status: str  # e.g., "current", "stale", "expired"
    authority_status: str  # e.g., "verified", "unverified", "revoked"


@dataclass(frozen=True)
class AdmissibilityResult:
    evidence_id: str
    authority_state: AuthorityState
    freshness_status: str
    authority_status: str
    demotion_reason: Optional[str]
    mapped_action: LensAction

    def to_record(self) -> dict[str, object]:
        return {
            "evidence_id": self.evidence_id,
            "authority_state": self.authority_state.value,
            "freshness_status": self.freshness_status,
            "authority_status": self.authority_status,
            "demotion_reason": self.demotion_reason,
            "mapped_action": self.mapped_action.value,
        }


def evaluate_evidence(evidence: EvidenceInput) -> AdmissibilityResult:
    """Classifies evidence into an authority state and maps it to a Lens action."""
    
    # Logic for demotion from authority to signal based on freshness and authority status
    if evidence.authority_status == "revoked":
        state = AuthorityState.INADMISSIBLE
        reason = "Authority has been explicitly revoked."
    elif evidence.freshness_status == "expired":
        state = AuthorityState.REQUIRES_REVALIDATION
        reason = "Evidence has expired and requires revalidation."
    elif evidence.freshness_status == "stale":
        state = AuthorityState.SIGNAL_ONLY
        reason = "Evidence is stale; demoted to contextual signal only."
    elif evidence.authority_status == "unverified":
        state = AuthorityState.SIGNAL_ONLY
        reason = "Evidence is unverified; demoted to contextual signal only."
    else:
        state = AuthorityState.AUTHORITATIVE
        reason = None

    return AdmissibilityResult(
        evidence_id=evidence.evidence_id,
        authority_state=state,
        freshness_status=evidence.freshness_status,
        authority_status=evidence.authority_status,
        demotion_reason=reason,
        mapped_action=AUTHORITY_TO_ACTION[state],
    )
