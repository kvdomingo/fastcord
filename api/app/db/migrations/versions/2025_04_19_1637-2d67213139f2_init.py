"""init

Revision ID: 2d67213139f2
Revises:
Create Date: 2025-04-19 16:37:40.602526

"""

from collections.abc import Sequence
from pathlib import Path

import sqlalchemy as sa
from alembic import op

MIGRATIONS_DIR = Path(__file__).resolve().parent
CURRENT_FILE = Path(__file__).stem


# revision identifiers, used by Alembic.
revision: str = "2d67213139f2"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    with open(MIGRATIONS_DIR / f"{CURRENT_FILE}.up.sql") as f:
        sql = f.read()

    conn = op.get_bind()
    conn.execute(sa.text(sql))


def downgrade() -> None:
    """Downgrade schema."""
    with open(MIGRATIONS_DIR / f"{CURRENT_FILE}.down.sql") as f:
        sql = f.read()

    conn = op.get_bind()
    conn.execute(sa.text(sql))
