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
"""
    Domain data schemas
"""
from datetime import datetime

from pydantic import BaseModel


class Update(BaseModel):
    """
        User's update schema used in domain
    """
    text: str
    date: datetime


class User(BaseModel):
    """
        User personal info schema used in domain
    """
    telegram_id: int
    first_name: str
    last_name: str | None


class Summary(BaseModel):
    last_day_i_did: str
    today_i_will_do: str
    any_blockers: str
