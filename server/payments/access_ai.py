"""GABON 360 AI — accès payant géré directement par GABON 360.

Le paiement commercial n'est PAS lié à Google Play.
GABON 360 est une association : les utilisateurs règlent directement sur
le compte officiel / les moyens de paiement officiellement déclarés par
l'association. L'accès n'est activé qu'après vérification côté serveur.

Les coordonnées bancaires ou numéros de paiement ne sont jamais codés en dur
dans l'application. Ils doivent être configurés côté administration sécurisée.
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


class PaymentChannel(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"
    OTHER_OFFICIAL = "other_official"


@dataclass(frozen=True)
class PaymentEvidence:
    channel: PaymentChannel
    reference: str
    amount: int
    currency: str
    paid_at: datetime
    account_id: Optional[str] = None
    receipt_url: Optional[str] = None


@dataclass(frozen=True)
class AccessDecision:
    allowed: bool
    state: AccessState
    reason: str
    product_id: Optional[str] = None


class DirectGabon360PaymentAI:
    """Contrôle déterministe des accès payants après validation de GABON 360.

    Une preuve déclarée par le client ne suffit jamais à elle seule.
    Un administrateur autorisé ou un connecteur officiel doit confirmer le
    paiement reçu sur le compte de l'association.
    """

    def decide(
        self,
        evidence: Optional[PaymentEvidence],
        verified_by_gabon360: bool,
        product_id: str,
        expires_at: Optional[datetime] = None,
    ) -> AccessDecision:
        if evidence is None:
            return AccessDecision(
                False, AccessState.UNVERIFIED,
                "Aucun paiement direct vérifié par GABON 360."
            )

        if not evidence.reference:
            return AccessDecision(
                False, AccessState.UNVERIFIED,
                "Référence de paiement manquante.", product_id
            )

        if evidence.amount <= 0 or not evidence.currency:
            return AccessDecision(
                False, AccessState.UNVERIFIED,
                "Montant ou devise de paiement invalide.", product_id
            )

        if not verified_by_gabon360:
            return AccessDecision(
                False, AccessState.PENDING,
                "Paiement déclaré mais encore en attente de vérification par GABON 360.",
                product_id
            )

        if expires_at is not None:
            expiry = expires_at
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if expiry <= datetime.now(timezone.utc):
                return AccessDecision(
                    False, AccessState.EXPIRED,
                    "Droit d'accès expiré.", product_id
                )

        return AccessDecision(
            True, AccessState.ACTIVE,
            "Accès autorisé après paiement direct vérifié par GABON 360.",
            product_id
        )


def direct_payment_entitlement(
    channel: str,
    reference: str,
    amount: int,
    currency: str,
    paid_at: datetime,
    product_id: str,
    verified_by_gabon360: bool = False,
    account_id: Optional[str] = None,
    receipt_url: Optional[str] = None,
    expires_at: Optional[datetime] = None,
) -> AccessDecision:
    """Construit une décision d'accès à partir d'un paiement direct.

    Les coordonnées du compte de GABON 360 ne sont pas stockées ici.
    Elles doivent rester dans la configuration sécurisée de l'association.
    """
    try:
        payment_channel = PaymentChannel(channel)
    except ValueError:
        return AccessDecision(
            False, AccessState.UNVERIFIED,
            "Canal de paiement non autorisé.", product_id
        )

    evidence = PaymentEvidence(
        channel=payment_channel,
        reference=reference,
        amount=amount,
        currency=currency,
        paid_at=paid_at,
        account_id=account_id,
        receipt_url=receipt_url,
    )
    return DirectGabon360PaymentAI().decide(
        evidence=evidence,
        verified_by_gabon360=verified_by_gabon360,
        product_id=product_id,
        expires_at=expires_at,
    )


@dataclass(frozen=True)
class AutomaticAccessStatus:
    user_id: str
    enabled: bool
    state: AccessState
    reason: str


class AutomaticAccessAI:
    """Synchronise automatiquement l'accès selon les paiements vérifiés.

    Cette IA ne considère jamais une simple déclaration client comme un paiement.
    Elle agit uniquement sur l'état de paiement vérifié par GABON 360.
    """

    def synchronize(
        self,
        user_id: str,
        payment: Optional[PaymentEvidence],
        verified_by_gabon360: bool,
        expires_at: Optional[datetime] = None,
    ) -> AutomaticAccessStatus:
        if not user_id:
            raise ValueError("user_id requis")

        if payment is None or not verified_by_gabon360:
            return AutomaticAccessStatus(
                user_id=user_id,
                enabled=False,
                state=AccessState.PENDING if payment else AccessState.UNVERIFIED,
                reason="Accès désactivé ou maintenu bloqué jusqu'à vérification du paiement GABON 360.",
            )

        if expires_at is not None:
            expiry = expires_at
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if expiry <= datetime.now(timezone.utc):
                return AutomaticAccessStatus(
                    user_id=user_id,
                    enabled=False,
                    state=AccessState.EXPIRED,
                    reason="Accès automatiquement désactivé : droit expiré.",
                )

        return AutomaticAccessStatus(
            user_id=user_id,
            enabled=True,
            state=AccessState.ACTIVE,
            reason="Accès automatiquement activé : paiement vérifié par GABON 360.",
        )
