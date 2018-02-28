#!/usr/bin/python3
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

"""A script to test different meson build configurations.

This script will build one more configurations of a meson based project,
testing for the configurations and build steps and print the results.
"""

from typing import Dict, List, Optional
import argparse
import json
import os
import shutil
import subprocess

import appdirs
import attr

CONFIG_DIR = appdirs.AppDirs('meson_test', 'dcbaker')
CONFIG = Dict[str, Dict[str, str]]


@attr.s
class Build:

    name: str = attr.ib()
    path: str = attr.ib()
    options: Dict[str, str] = attr.ib()

    def configure(self) -> bool:
        res = subprocess.run(
            ['meson', self.path] +
            ['-D{}={}'.format(k, v) for k, v in self.options.items()])
        return res.returncode == 0

    def build(self) -> bool:
        res = subprocess.run(['ninja', '-C', self.path])
        return res.returncode == 0

    def clean(self) -> None:
        if os.path.exists(self.path):
            shutil.rmtree(self.path)


@attr.s
class Result:

    name: str = attr.ib()
    configure: Optional[bool] = attr.ib(default=None)
    build: Optional[bool] = attr.ib(default=None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project')
    parser.add_argument('--build-dir', action='store', default='build-test')
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--test', action='append', default=[])
    args = parser.parse_args()

    results: List[Result] = []

    config_file = os.path.join(CONFIG_DIR.user_config_dir, args.project)
    with open(f'{config_file}.json') as f:
        config: CONFIG = json.load(f)

    if args.test:
        config = {n: v for n, v in config.items() if n in args.test}

    for name, options in config.items():
        result = Result(name)
        results.append(result)
        build = Build(name, os.path.join(args.build_dir, name), options)

        if args.clean:
            build.clean()

        result.configure = build.configure()
        if not result.configure:
            continue

        result.build = build.build()

    for r in results:
        print(str(r))


if __name__ == '__main__':
    main()
