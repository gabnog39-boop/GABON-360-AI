"""Réconciliation des paiements directs GABON 360.

Ce service constitue la frontière serveur entre un relevé/connecteur de paiement
officiel et les droits d'accès. Il est conçu pour être branché à la banque ou
Mobile Money de l'association sans exposer ses coordonnées dans l'APK.

Aucun paiement n'est inventé : seules les transactions fournies par le
connecteur officiel sont prises en compte.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Protocol

from .access_ai import AccessState, AutomaticAccessAI, AutomaticAccessStatus, PaymentEvidence


@dataclass(frozen=True)
class VerifiedPayment:
    user_id: str
    evidence: PaymentEvidence
    expires_at: datetime | None = None


class OfficialPaymentSource(Protocol):
    def verified_payments(self) -> Iterable[VerifiedPayment]:
        """Retourne uniquement les transactions confirmées par la source officielle."""


class AccessEntitlementStore(Protocol):
    def set_status(self, status: AutomaticAccessStatus) -> None:
        """Persiste l'état serveur de l'utilisateur."""


class PaymentAccessReconciler:
    def __init__(self, source: OfficialPaymentSource, store: AccessEntitlementStore):
        self.source = source
        self.store = store
        self.ai = AutomaticAccessAI()

    def run_once(self) -> list[AutomaticAccessStatus]:
        statuses: list[AutomaticAccessStatus] = []
        seen: set[str] = set()

        for payment in self.source.verified_payments():
            if payment.user_id in seen:
                continue
            seen.add(payment.user_id)
            status = self.ai.synchronize(
                user_id=payment.user_id,
                payment=payment.evidence,
                verified_by_gabon360=True,
                expires_at=payment.expires_at,
            )
            self.store.set_status(status)
            statuses.append(status)

        return statuses

    def deactivate_missing_users(
        self,
        known_user_ids: Iterable[str],
        active_user_ids: set[str],
    ) -> list[AutomaticAccessStatus]:
        statuses: list[AutomaticAccessStatus] = []
        for user_id in known_user_ids:
            if user_id in active_user_ids:
                continue
            status = AutomaticAccessStatus(
                user_id=user_id,
                enabled=False,
                state=AccessState.UNVERIFIED,
                reason="Accès automatiquement désactivé : aucun paiement direct vérifié actif.",
            )
            self.store.set_status(status)
            statuses.append(status)
        return statuses
