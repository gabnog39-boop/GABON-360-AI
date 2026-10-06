"""GABON 360 AI payment/access decision engine.

This module never trusts a client-side 'paid=true' flag. A production adapter must
supply a verified Google Play purchase/subscription state from the secure backend.
The engine converts verified billing state into an explicit entitlement decision.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class AccessState(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    EXPIRED = "expired"
    CANCELED = "canceled"
    REVOKED = "revoked"
    UNVERIFIED = "unverified"


@dataclass(frozen=True)
class BillingEvidence:
    provider: str
    product_id: str
    purchase_token: str
    state: AccessState
    expires_at: Optional[datetime] = None
    acknowledged: bool = False
    account_id: Optional[str] = None


@dataclass(frozen=True)
class AccessDecision:
    allowed: bool
    state: AccessState
    reason: str
    product_id: Optional[str] = None


class PaymentAccessAI:
    """Deterministic payment gate used by the access-control API.

    The 'AI' label refers to the policy/orchestration layer. It must not invent
    payment status; only verified billing evidence can unlock paid features.
    """

    def decide(self, evidence: Optional[BillingEvidence]) -> AccessDecision:
        if evidence is None:
            return AccessDecision(False, AccessState.UNVERIFIED,
                                  "Aucun achat vérifié n'est disponible.")
        if evidence.provider != "google_play":
            return AccessDecision(False, AccessState.UNVERIFIED,
                                  "Fournisseur de paiement non autorisé.", evidence.product_id)
        if not evidence.purchase_token:
            return AccessDecision(False, AccessState.UNVERIFIED,
                                  "Jeton d'achat manquant.", evidence.product_id)
        if evidence.state is not AccessState.ACTIVE:
            return AccessDecision(False, evidence.state,
                                  "Abonnement non actif.", evidence.product_id)
        if evidence.expires_at is not None:
            now = datetime.now(timezone.utc)
            expiry = evidence.expires_at
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if expiry <= now:
                return AccessDecision(False, AccessState.EXPIRED,
                                      "Abonnement expiré.", evidence.product_id)
        return AccessDecision(True, AccessState.ACTIVE,
                              "Accès autorisé par un achat vérifié.", evidence.product_id)


def subscription_entitlement(subscription_state: str, expiry_time: Optional[datetime],
                             product_id: str, purchase_token: str,
                             acknowledged: bool = False, account_id: Optional[str] = None) -> AccessDecision:
    """Map a Google Play subscription state into a safe access decision.

    The caller must obtain subscription_state/expiry_time from the Google Play
    Developer API on a secure backend; never pass untrusted client values here.
    """
    mapping = {
        "SUBSCRIPTION_STATE_ACTIVE": AccessState.ACTIVE,
        "SUBSCRIPTION_STATE_PENDING": AccessState.PENDING,
        "SUBSCRIPTION_STATE_CANCELED": AccessState.CANCELED,
        "SUBSCRIPTION_STATE_EXPIRED": AccessState.EXPIRED,
        "SUBSCRIPTION_STATE_PAUSED": AccessState.CANCELED,
    }
    state = mapping.get(subscription_state, AccessState.UNVERIFIED)
    return PaymentAccessAI().decide(BillingEvidence(
        provider="google_play",
        product_id=product_id,
        purchase_token=purchase_token,
        state=state,
        expires_at=expiry_time,
        acknowledged=acknowledged,
        account_id=account_id,
    ))
