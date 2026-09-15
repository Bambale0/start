from dataclasses import dataclass
from uuid import UUID


class MissingOrganizationContext(RuntimeError):
    """Raised when a tenant-bound operation lacks an organization context."""


class PermissionDenied(RuntimeError):
    """Raised when the active actor lacks a required permission."""


@dataclass(frozen=True, slots=True)
class RequestContext:
    user_id: UUID
    organization_id: UUID | None = None
    group_id: UUID | None = None
    permissions: frozenset[str] = frozenset()

    def require_organization(self) -> UUID:
        if self.organization_id is None:
            raise MissingOrganizationContext("organization context is required")
        return self.organization_id

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    def require_permission(self, permission: str) -> None:
        if not self.has_permission(permission):
            raise PermissionDenied(f"missing required permission: {permission}")
