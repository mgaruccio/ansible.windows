#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2015, Phil Schwartz <schwartzmx@gmail.com>
# Copyright: (c) 2015, Trond Hindenes
# Copyright: (c) 2015, Hans-Joachim Kliemeck <git@kliemeck.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: win_acl
short_description: Set file/directory/registry/Active Directory Object permissions for a system user or group
description:
- Add or remove rights/permissions for a given user or group for the specified
  file, folder, registry key or AppPool identifies.
options:
  path:
    description:
    - The path to the file or directory.
    type: str
    required: yes
  user:
    description:
    - User or Group to add specified rights to act on src file/folder,
      registry key, or active directory object.
    type: str
    required: yes
  state:
    description:
    - Specify whether to add C(present) or remove C(absent) the specified access rule.
    type: str
    choices: [ absent, present ]
    default: present
  type:
    description:
    - Specify whether to allow or deny the rights specified.
    type: str
    required: yes
    choices: [ allow, deny ]
  rights:
    description:
    - The rights/permissions that are to be allowed/denied for the specified
      user or group for the item at C(path).
    - If C(path) is a file or directory, rights can be any right under MSDN
      FileSystemRights U(https://msdn.microsoft.com/en-us/library/system.security.accesscontrol.filesystemrights.aspx).
    - If C(path) is a registry key, rights can be any right under MSDN
      RegistryRights U(https://msdn.microsoft.com/en-us/library/system.security.accesscontrol.registryrights.aspx).
    - If C(path) is an Active Directory Object, rights can be any right under MSDN
      ActiveDirectoryRights U(https://msdn.microsoft.com/en-us/library/System.DirectoryServices.ActiveDirectoryRights.aspx).
    type: str
    required: yes
  inherit:
    description:
    - Inherit flags on the ACL rules.
    - Can be specified as a comma separated list, e.g. C(ContainerInherit),
      C(ObjectInherit).
    - For more information on the choices see MSDN InheritanceFlags enumeration
      at U(https://msdn.microsoft.com/en-us/library/system.security.accesscontrol.inheritanceflags.aspx).
    - Defaults to C(ContainerInherit, ObjectInherit) for Directories.
    type: str
    choices: [ ContainerInherit, ObjectInherit ]
  propagation:
    description:
    - Propagation flag on the ACL rules.
    - For more information on the choices see MSDN PropagationFlags enumeration
      at U(https://msdn.microsoft.com/en-us/library/system.security.accesscontrol.propagationflags.aspx).
    - Propagation flags are not supported on Active Directory Objects
    type: str
    choices: [ InheritOnly, None, NoPropagateInherit ]
    default: "None"
notes:
- If adding ACL's for AppPool identities, the Windows Feature "Web-Scripting-Tools" must be enabled.
- If maniuplating active directory objects, the user must have AD permissions and the ActiveDirctory module must be available
seealso:
- module: ansible.windows.win_acl_inheritance
- module: ansible.windows.win_file
- module: ansible.windows.win_owner
- module: ansible.windows.win_stat
author:
- Phil Schwartz (@schwartzmx)
- Trond Hindenes (@trondhindenes)
- Hans-Joachim Kliemeck (@h0nIg)
'''

EXAMPLES = r'''
- name: Restrict write and execute access to User Fed-Phil
  ansible.windows.win_acl:
    user: Fed-Phil
    path: C:\Important\Executable.exe
    type: deny
    rights: ExecuteFile,Write

- name: Add IIS_IUSRS allow rights
  ansible.windows.win_acl:
    path: C:\inetpub\wwwroot\MySite
    user: IIS_IUSRS
    rights: FullControl
    type: allow
    state: present
    inherit: ContainerInherit, ObjectInherit
    propagation: 'None'

- name: Set registry key right
  ansible.windows.win_acl:
    path: HKCU:\Bovine\Key
    user: BUILTIN\Users
    rights: EnumerateSubKeys
    type: allow
    state: present
    inherit: ContainerInherit, ObjectInherit
    propagation: 'None'

- name: Remove FullControl AccessRule for IIS_IUSRS
  ansible.windows.win_acl:
    path: C:\inetpub\wwwroot\MySite
    user: IIS_IUSRS
    rights: FullControl
    type: allow
    state: absent
    inherit: ContainerInherit, ObjectInherit
    propagation: 'None'

- name: Deny Intern
  ansible.windows.win_acl:
    path: C:\Administrator\Documents
    user: Intern
    rights: Read,Write,Modify,FullControl,Delete
    type: deny
    state: present

- name: Grant GenericAll rights on OU to User Fred-Phil
  ansible.windows.win_acl:
    path: AD:\OU=test,DC=Contoso,DC=com
    user: Fred-Phil@constoso.com
    rights: GenericAll
    state: present
'''
