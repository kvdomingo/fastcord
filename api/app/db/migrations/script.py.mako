"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union
from pathlib import Path

from alembic import op
import sqlalchemy as sa

from app.settings import settings
${imports if imports else ""}

MIGRATIONS_DIR = Path(__file__).resolve().parent
CURRENT_FILE = Path(__file__).stem


# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


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
