from uuid import uuid4

import pytest

from start_os.core.tenant import (
    MissingOrganizationContext,
    PermissionDenied,
    RequestContext,
)


def test_organization_context_must_be_explicit() -> None:
    context = RequestContext(user_id=uuid4())

    with pytest.raises(MissingOrganizationContext):
        context.require_organization()


def test_organization_context_is_returned_when_present() -> None:
    organization_id = uuid4()
    context = RequestContext(user_id=uuid4(), organization_id=organization_id)

    assert context.require_organization() == organization_id


def test_permission_check_is_explicit() -> None:
    context = RequestContext(
        user_id=uuid4(),
        permissions=frozenset({"cases.read"}),
    )

    context.require_permission("cases.read")

    with pytest.raises(PermissionDenied):
        context.require_permission("cases.manage")
