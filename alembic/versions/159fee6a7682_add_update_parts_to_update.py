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
"""Add update parts to update

Revision ID: 159fee6a7682
Revises: bf865b98e6dc
Create Date: 2025-10-21 15:48:45.577884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '159fee6a7682'
down_revision: Union[str, Sequence[str], None] = 'bf865b98e6dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('updates', sa.Column('last_day_i_did', sa.Text))
    op.add_column('updates', sa.Column('today_i_will_do', sa.Text))
    op.add_column('updates', sa.Column('any_blockers', sa.Text))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("updates", "last_day_i_did")
    op.drop_column("updates", "today_i_will_do")
    op.drop_column("updates", "any_blockers")
