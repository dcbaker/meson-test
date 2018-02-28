# Copyright © 2018 Intel Corporation
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

"""Tests run with pylint."""

import os
import tempfile

from meson_test import Build


class TestBuild:

    class TestClean:

        def test_remove_directory(self):
            with tempfile.TemporaryDirectory() as t:
                path = os.path.join(t, 'foo')
                os.mkdir(path)
                build = Build('foo', path, {})
                build.clean()
                assert not os.path.exists(path)

        def test_no_directory(self):
            with tempfile.TemporaryDirectory() as t:
                path = os.path.join(t, 'foo')
                build = Build('foo', path, {})
                build.clean()
