import time

from fetch.ledger.api.wallet import WalletApi


class WalletApiExample(object):
    MAX_ITERATIONS = 20
    ITERATION_PERIOD_SECS = 0.5

    def __init__(self, host, port):
        self._api = WalletApi(host, port, 2)

    def _register(self, number_of_identities=1):
        addresses = self._api.register(number_of_identities=number_of_identities)

        if addresses is None:
            raise RuntimeError('Unable to request addresses from wallet API')

        for address in addresses:
            # wait for a positive balance to be created (sort of backed into the contract)
            balance = 0
            for n in range(self.MAX_ITERATIONS):
                balance = self._balance(address)
                if balance > 0:
                    break

                time.sleep(self.ITERATION_PERIOD_SECS)

            if balance == 0:
                raise RuntimeError('Failed to generate a balance from the registered account')

        return addresses

    def _balance(self, address):
        if address is None:
            return False

        # wait for a balance to be presented
        balance = None
        for n in range(self.MAX_ITERATIONS):
            balance = self._api.balance(address)

            # exit the loop if the balance has been retrieved
            if balance is not None:
                break

            # wait for the data to become available
            time.sleep(self.ITERATION_PERIOD_SECS)

        if balance is None:
            raise RuntimeError('Unable to request balance for address: ')

        return balance

    def _transfer(self, from_address, to_address, amount):
        if not self._api.transfer(from_address, to_address, amount):
            raise RuntimeError('Failed to submit the transfer transaction')


class SimpleBalanceRequest(WalletApiExample):
    def run(self, number_of_identities=1):
        # register with the ledger for an address
        addresses = self._register(number_of_identities=number_of_identities)

        for address in addresses:
            # check that we have been given a "valid" address
            balance = self._balance(address)
            print('Balance for address: {} is {}'.format(address, balance))


class SimpleTransferExchange(WalletApiExample):
    def run(self):
        # register with the ledger for an address
        addresses = self._register(number_of_identities=2)

        for address in addresses:
            # get the balances for the different accounts
            balance = self._balance(address)

            assert balance >= 1

            transfer_amount = max(balance // 10, 1)

            # determine the expected balances
            expected_balance = balance - transfer_amount

        # wait until the balances match

