from uuid import uuid4
from abc import ABC, abstractmethod


class MockOPNsenseController(ABC):
    """
    Very simple representation of the server-side logic of the OPNsense - so we can use it as testdata
    """

    RES_SUCCESS = {'status': 'ok'}
    RES_ERROR = {'status': 'error'}

    def __init__(self, key_path: list[str] = None):
        if key_path is None:
            self.key_path = []

        else:
            self.key_path = key_path
            self.key_path.reverse()

        self.state = {}

    @staticmethod
    def _new_uuid() -> str:
        return str(uuid4())

    @abstractmethod
    def commands(self) -> dict:
        return {
            'get': self._get,
            'add_item': self._add,
            'set_item': self._set,
            'del_item': self._del,
            'toggle_item': self._toggle,
            'reconfigure': self._reconfigure,
        }

    def route_kwargs(self, method) -> list:
        return {
            self._get: [],
            self._add: ['data'],
            self._set: ['uuid', 'data'],
            self._del: ['uuid'],
            self._toggle: ['uuid'],
            self._reconfigure: [],
        }[method]

    def pack_data(self, data: any) -> dict:
        """
        Pack 'data' inside the key_path 'keys' - example: "{'test': {'tests': {'test': <data> }}}"
        :param data: any
        :return: dict
        """
        out = data.copy()
        for k in self.key_path:
            out = {k: out}

        return out

    def unpack_data(self, packed: dict) -> (dict, any):
        """
        Unpack some data nested under the key_path 'keys' - example: "{'test': {'tests': {'test': <data> }}}"
        :param packed: dict
        :return: any
        """
        out = packed.copy()
        key_path = self.key_path.copy()
        key_path.reverse()
        for k in key_path:
            if k not in out:
                # post only has the deepest key
                break

            out = out[k]

        return out

    def _get(self) -> dict:
        return self.pack_data(self.state)

    def _add(self, data: dict) -> dict:
        self.state[self._new_uuid()] = self.unpack_data(data)
        return self.RES_SUCCESS

    def _set(self, uuid: str, data: dict):
        if uuid in self.state:
            self.state[uuid] = self.unpack_data(data)
            return self.RES_SUCCESS

        else:
            return self.RES_ERROR

    def _del(self, uuid: str) -> dict:
        if uuid in self.state:
            self.state.pop(uuid)
            return self.RES_SUCCESS

        else:
            return self.RES_ERROR

    def _toggle(self, uuid: str) -> dict:
        if uuid in self.state:
            is_enabled = str(self.state[uuid]['enabled']) == '1'
            self.state[uuid]['enabled'] = '0' if is_enabled else '1'
            return self.RES_SUCCESS

        else:
            return self.RES_ERROR

    def _reconfigure(self) -> dict:
        return self.RES_SUCCESS


class GenericTestdata(MockOPNsenseController):
    def __init__(self):
        super().__init__(key_path=['test', 'tests', 'test'])

    def commands(self) -> dict:
        return {
            'get': self._get,
            'add_test': self._add,
            'set_test': self._set,
            'del_test': self._del,
            'toggle_test': self._toggle,
            'reconfigure': self._reconfigure,
        }
