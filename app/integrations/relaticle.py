from __future__ import annotations

from app.crm_transfer import CRMTransferPayload


class RelaticleIntegrationNotAudited(RuntimeError):
    pass


class RelaticleClient:
    """Boundary for a future audited Relaticle integration.

    No endpoint, authentication scheme, entity name or payload shape may be
    assumed before the external repository/API is inspected and documented.
    """

    async def transfer_qualified_lead(self, payload: CRMTransferPayload) -> dict:
        raise RelaticleIntegrationNotAudited(
            "Relaticle integration is blocked until its real API contract is audited; "
            "no external request was sent."
        )
