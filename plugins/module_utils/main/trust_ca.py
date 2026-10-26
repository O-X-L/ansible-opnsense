from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.trust import \
    TRUST_SUBJECT_FIELDS, TRUST_FIELDS_TRANSLATE
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.trust import BaseTrust


class Ca(BaseTrust):
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
        'ca_list': 'ca_list',
    }
    API_KEY_PATH = 'ca'
    API_CONT = 'ca'
    FIELDS_IMMUTABLE = ['ca', 'key_type', 'digest', 'lifetime', 'ocsp_uri', *TRUST_SUBJECT_FIELDS]
    FIELDS_ALL = [*BaseTrust.FIELDS_CHANGE, *FIELDS_IMMUTABLE]
    FIELDS_TRANSLATE = TRUST_FIELDS_TRANSLATE
    FIELDS_TYPING = {
        'select': ['ca', 'key_type', 'digest', 'country'],
    }
    KIND = 'CA'

    def build_request(self) -> dict:
        request = self._base_build_request()

        if not self.exists:
            request[self.API_KEY_PATH]['action'] = 'internal'
            return request

        # the API re-imports the existing certificate & key on update
        #   using the 'internal' action would generate a new CA!
        detail = self._get_detail()
        request[self.API_KEY_PATH]['action'] = 'existing'
        request[self.API_KEY_PATH]['crt_payload'] = detail['crt_payload']
        request[self.API_KEY_PATH]['prv_payload'] = detail['prv_payload']
        return request

    def delete(self) -> None:
        # the API does not check if the CA is still in use by certificates or services
        if int(self.entry.get('refcount', 0)) > 0:
            self.m.fail_json(
                f"The CA '{self.entry['description']}' is still referenced {self.entry['refcount']} time(s) "
                '(certificates/services) - remove these references first!'
            )

        self._base_delete()
