from .common import ApiEndpoint


class WalletApi(ApiEndpoint):
    @property
    def api_prefix(self):
        api_version = self.api_version
        assert api_version in (1, 2)

        if api_version == 1:
            return '/'
        elif api_version == 2:
            return '/api/wallet/'
        else:
            assert False

    def register(self, number_of_identities=1):
        req_data = {}
        if number_of_identities > 1:
            req_data["count"] = number_of_identities

        success, resp_data = self._post(self.api_prefix + 'register', data=req_data)
        if success:
            if 'address' in resp_data:
                return [resp_data['address']]
            elif 'addresses' in resp_data:
                return resp_data['addresses']

    def balance(self, address):
        request = {
            'address': address
        }
        success, data = self._post(self.api_prefix + 'balance', request)
        if success and 'balance' in data:
            return data['balance']

    def transfer(self, from_address, to_address, amount):
        request = {
            'from': from_address,
            'to': to_address,
            'amount': amount
        }
        success, _ = self._post(self.api_prefix + 'transfer', request)
        if success:
            return True
