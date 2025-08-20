from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class HaproxyMailer(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addMailer',
        'del': 'delMailer',
        'set': 'setMailer',
        'search': 'searchmailers',
        'detail': 'getMailer',
        'toggle': 'toggleMailer',
    }
    API_KEY_PATH = 'mailer'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['enabled', 'description', 'mailservers', 'sender', 'recipient']
    FIELDS_ALL = ['name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'enabled': 'enabled',
        'description': 'description', 
        'name': 'name',
        'mailservers': 'mailservers',
        'sender': 'sender',
        'recipient': 'recipient'
    }
    FIELDS_TYPING = {
        'bool': ['enabled']
    }
    EXIST_ATTR = 'mailer'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.mailer = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['name']):
                self.m.fail_json('You need to provide a name to create a mailer!')

            if is_unset(self.p['mailservers']):
                self.m.fail_json('You need to provide mailservers to create a mailer!')

            if is_unset(self.p['sender']):
                self.m.fail_json('You need to provide a sender email to create a mailer!')

            if is_unset(self.p['recipient']):
                self.m.fail_json('You need to provide a recipient email to create a mailer!')

            # Basic email validation
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not re.match(email_pattern, self.p['sender']):
                self.m.fail_json(f"Sender '{self.p['sender']}' is not a valid email address!")

            if not re.match(email_pattern, self.p['recipient']):
                self.m.fail_json(f"Recipient '{self.p['recipient']}' is not a valid email address!")

        self._base_check()