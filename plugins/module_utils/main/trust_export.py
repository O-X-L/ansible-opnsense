from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust_ca import Ca
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust_cert import Cert


class Export:
    # see: OPNsense/Trust/Api/CaController.php & CertController.php - generateFileAction
    TARGETS = {
        'ca': Ca,
        'cert': Cert,
    }
    FORMATS = {
        'ca': ['crt', 'prv'],
        'cert': ['crt', 'prv', 'csr', 'pkcs12'],
    }
    FORMATS_PRIVATE = ['prv', 'pkcs12']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.target = self.TARGETS[self.p['target']](module=module, result=result, session=self.s)
        self.uuid = None

    def check(self) -> None:
        if self.p['format'] not in self.FORMATS[self.p['target']]:
            self.m.fail_json(
                f"The format '{self.p['format']}' is not supported for the target '{self.p['target']}' - "
                f"supported are: {', '.join(self.FORMATS[self.p['target']])}"
            )

        matching = [
            entry for entry in self.target.search_call()
            if entry['descr'] == self.p['description']
        ]
        if len(matching) == 0:
            self.m.fail_json(f"The {self.target.KIND} '{self.p['description']}' was not found!")

        if len(matching) > 1:
            self.m.fail_json(
                f"Multiple {self.target.KIND} entries with the description '{self.p['description']}' exist!"
            )

        self.uuid = matching[0]['uuid']

    def process(self) -> None:
        response = self.s.post(cnf={
            'module': self.target.API_MOD,
            'controller': self.target.API_CONT,
            'command': 'generate_file',
            'params': [self.uuid, self.p['format']],
            'data': {'password': self.p['password']} if self.p['format'] == 'pkcs12' else None,
        })

        # PKCS#12 is binary - the API delivers it base64-encoded
        payload = response.get('payload_b64' if self.p['format'] == 'pkcs12' else 'payload', '')
        if response.get('status') != 'ok' or payload in [None, '']:
            self.m.fail_json(
                f"Failed to export the '{self.p['format']}' of the {self.target.KIND} '{self.p['description']}'"
                f"{': ' + response['error'] if response.get('error') else ' - it might not exist for this entry'}"
            )

        self.r['uuid'] = self.uuid
        self.r['payload'] = payload
