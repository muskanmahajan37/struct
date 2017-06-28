# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
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

from generator_common.common import each_function, function_arguments


def generate(info, template):
    lines = []
    if_prefix = ''
    for function, function_info in each_function(info):
        arg_info = function_arguments(function_info)
        lines.append('    {}if function[\'type\'] == "{}":'.format(
            if_prefix, function))
        arg_prefix = 'f.{}_param'.format(info['Names'][function])

        for arg, arg_type in zip(arg_info['names'], arg_info['types']):
            if arg_type in ['float', 'double', 'int64', 'string']:
                lines.append(
                    '        {0}.{1} = function[\'args\'][\'{1}\']'.format(arg_prefix, arg))
            elif arg_type == 'bool':
                lines.append(
                    '        if function[\'args\'][\'{}\']:'.format(arg))
                lines.append(
                    '            {0}.{1} = True'.format(arg_prefix, arg))
                lines.append('        else:')
                lines.append(
                    '            {0}.{1} = False'.format(arg_prefix, arg))
                pass
            elif arg_type == 'Shape':
                lines.append('        {0}.{1}.dim.extend(function[\'args\'][\'{1}\'])'.format(
                    arg_prefix, arg))
            elif arg_type == 'repeated int64':
                lines.append(
                    '        {0}.{1}.extend(function[\'args\'][\'{1}\'])'.format(arg_prefix, arg))
            else:
                print('Unknown argument type [{}]'.format(arg_type))
                raise 'Unknown argument type [{}]'.format(arg_type)

            arg_suffix = '.dim' if type == 'Shape' else ''
        lines.append('        pass')
        if_prefix = 'el'
    return template.format(create_function_args='\n'.join(lines))
