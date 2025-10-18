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
    Message templates used in responses
"""
WELCOME_MESSAGE: str = """
    Welcome to DrScrum, {full_name}!
"""
NON_TEXT_MESSAGE_ERROR_MESSAGE: str = """
    Error x-x I only understand text messages for now!
"""
MESSAGE_RECORD_FAILED_ERROR_MESSAGE: str = """
    Fatal x-x something is wrong with me, I couldn't record this message.
"""
UPDATE_MESSAGE: str = """
    Here's your updates:
**Last day I did**:
{last_day_i_did}

**Today I will do**:
{today_i_will_do}

**Blockers (if any)**:
{any_blockers}
"""
NOUPDATE_MESSAGE: str = """
    You don't have any recent update.
"""
CLEAR_MESSAGE: str = """
    Current session cleared.
"""
