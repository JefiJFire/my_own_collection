#!/usr/bin/python

# Copyright: (c) 2024
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Creates a text file with given content on a remote host

version_added: "1.0.0"

description:
    - This module creates a text file at the path specified by the C(path) parameter.
    - The file will contain the text specified by the C(content) parameter.
    - The module is idempotent: if the file already exists with the same content, no changes are made.

options:
    path:
        description: Absolute path to the file to create on the remote host.
        required: true
        type: str
    content:
        description: Text content to write into the file.
        required: true
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create a file with content
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/hello.txt
    content: "Hello, Netology!"
'''

RETURN = r'''
message:
    description: Status message describing what happened.
    type: str
    returned: always
    sample: 'File created successfully'
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    # Idempotency: if file exists with same content — do nothing
    if os.path.exists(path):
        with open(path, 'r') as f:
            existing = f.read()
        if existing == content:
            result['changed'] = False
            result['message'] = 'File already exists with the same content, no changes needed'
            module.exit_json(**result)

    # Check mode — report what would happen without doing it
    if module.check_mode:
        result['changed'] = True
        result['message'] = 'File would be created or updated (check mode)'
        module.exit_json(**result)

    # Create or overwrite the file
    try:
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
        result['message'] = 'File created successfully'
    except IOError as e:
        module.fail_json(msg='Failed to write file: {}'.format(str(e)), **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
