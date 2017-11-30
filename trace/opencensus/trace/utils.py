# Copyright 2017, OpenCensus Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

UTF8 = 'utf-8'

# Max length is 128 bytes for a truncatable string.
MAX_LENGTH = 128


def _get_truncatable_str(str_to_convert):
    """Truncate a string if exceed limit and record the truncated bytes
    count.
    """
    str_bytes = str_to_convert.encode(UTF8)
    str_len = len(str_bytes)

    truncated_byte_count = 0

    if str_len > MAX_LENGTH:
        truncated_byte_count = str_len - MAX_LENGTH
        str_bytes = str_bytes[:MAX_LENGTH]

    truncated = str_bytes.decode(UTF8)

    result = {
        'value': truncated,
        'truncated_byte_count': truncated_byte_count,
    }
    return result