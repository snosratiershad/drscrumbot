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
"""Add message table

Revision ID: 1e33f7891a86
Revises: 684cae8ca49f
Create Date: 2025-09-25 19:26:19.413511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e33f7891a86'
down_revision: Union[str, Sequence[str], None] = '684cae8ca49f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "messages",
        # That's because sqlite doesn't incrementing BigInteger
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('from_user_id', sa.BigInteger()),
        sa.Column('chat_message_id', sa.BigInteger()),
        sa.Column('date', sa.DateTime()),
        sa.Column('text', sa.Text()),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.ForeignKeyConstraint(['from_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("messages")
