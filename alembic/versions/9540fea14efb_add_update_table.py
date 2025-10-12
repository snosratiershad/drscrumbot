# Copyright (C) 2025  Salar Nosrati-Ershad salar@roverc.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Add update table

Revision ID: 9540fea14efb
Revises: 1e33f7891a86
Create Date: 2025-09-27 23:13:25.623124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9540fea14efb'
down_revision: Union[str, Sequence[str], None] = '1e33f7891a86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "updates",
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("user_id", sa.BigInteger),
        sa.Column("text", sa.Text),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        "update_message",
        sa.Column("message_id", sa.Integer),
        sa.Column("update_id", sa.Integer),
        sa.ForeignKeyConstraint(["message_id"], ["messages.id"]),
        sa.ForeignKeyConstraint(["update_id"], ["updates.id"])
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("updates")
