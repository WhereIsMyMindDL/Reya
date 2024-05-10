import time
import json
from pyuseragents import random as random_ua
from requests import Session
import random
import ccxt
from loguru import logger
import requests
from eth_account.messages import encode_defunct

from settings import amount, decimal_places, transfer_subaccount, API, module
from help import Account, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data_withABI

send_list = ''

switch_cex = "okx"
proxy_server = ""
proxies = {
  "http": proxy_server,
  "https": proxy_server,
}
symbolWithdraw = "USDC"

reya_abi = json.loads('[{"inputs":[{"internalType":"address","name":"token_","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"CannotTransferOrExecuteOnBridgeContracts","type":"error"},{"inputs":[],"name":"InsufficientMsgValue","type":"error"},{"inputs":[],"name":"InvalidConnector","type":"error"},{"inputs":[],"name":"InvalidTokenAddress","type":"error"},{"inputs":[],"name":"InvalidTokenContract","type":"error"},{"inputs":[],"name":"MessageIdMisMatched","type":"error"},{"inputs":[],"name":"NoPendingData","type":"error"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"NoPermit","type":"error"},{"inputs":[],"name":"OnlyNominee","type":"error"},{"inputs":[],"name":"OnlyOwner","type":"error"},{"inputs":[],"name":"ZeroAddress","type":"error"},{"inputs":[],"name":"ZeroAddressReceiver","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"connector","type":"address"},{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"messageId","type":"bytes32"}],"name":"BridgingTokens","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"connector","type":"address"},{"indexed":false,"internalType":"bool","name":"status","type":"bool"}],"name":"ConnectorStatusUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newHook","type":"address"}],"name":"HookUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"claimer","type":"address"}],"name":"OwnerClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nominee","type":"address"}],"name":"OwnerNominated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"grantee","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"revokee","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"connecter","type":"address"},{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"messageId","type":"bytes32"}],"name":"TokensBridged","type":"event"},{"inputs":[{"internalType":"address","name":"receiver_","type":"address"},{"internalType":"uint256","name":"amount_","type":"uint256"},{"internalType":"uint256","name":"msgGasLimit_","type":"uint256"},{"internalType":"address","name":"connector_","type":"address"},{"internalType":"bytes","name":"execPayload_","type":"bytes"},{"internalType":"bytes","name":"options_","type":"bytes"}],"name":"bridge","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"bridgeType","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"connectorCache","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"connector_","type":"address"},{"internalType":"uint256","name":"msgGasLimit_","type":"uint256"},{"internalType":"uint256","name":"payloadSize_","type":"uint256"}],"name":"getMinFees","outputs":[{"internalType":"uint256","name":"totalFees","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role_","type":"bytes32"},{"internalType":"address","name":"grantee_","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role_","type":"bytes32"},{"internalType":"address","name":"address_","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"hook__","outputs":[{"internalType":"contract IHook","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"identifierCache","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nominee_","type":"address"}],"name":"nominateOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"nominee","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"siblingChainSlug_","type":"uint32"},{"internalType":"bytes","name":"payload_","type":"bytes"}],"name":"receiveInbound","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token_","type":"address"},{"internalType":"address","name":"rescueTo_","type":"address"},{"internalType":"uint256","name":"amount_","type":"uint256"}],"name":"rescueFunds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"connector_","type":"address"},{"internalType":"bytes32","name":"messageId_","type":"bytes32"}],"name":"retry","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role_","type":"bytes32"},{"internalType":"address","name":"revokee_","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"connectors","type":"address[]"},{"internalType":"bool[]","name":"statuses","type":"bool[]"}],"name":"updateConnectorStatus","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"hook_","type":"address"},{"internalType":"bool","name":"approve_","type":"bool"}],"name":"updateHook","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"validConnectors","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')

class Reya(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.session = Session()
        self.contract = self.get_contract(contract_address=self.w3.to_checksum_address("0x9239609eED7c40C6DDcEC25D247Ef205103590B6"), abi=reya_abi)
        self.session.headers['user-agent'] = random_ua()
        self.proxy = proxy
        if self.proxy != None:
            self.session.proxies.update({'http': "http://" + self.proxy})

    @retry
    def login(self):
        global send_list

        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'If-None-Match': 'W/"a0-hEXNx5MdEP2xb7/P220BHFCiDKY"',
            'Origin': 'https://reya.network',
            'Referer': 'https://reya.network/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        })

        response = self.session.get('https://api.reya.xyz/api/tos/latest-version', headers=self.session.headers).json()

        text = response['text']
        message = encode_defunct(text=text)
        text_signature = self.w3.eth.account.sign_message(message, private_key=self.private_key)
        signature_value = text_signature.signature.hex()

        files = {
            'signature': (None, signature_value),
            'walletAddress': (None, self.address),
            'message': (None, text),
            'version': (None, '2'),
            'referredByCode': (None, '8xvsy5nn'),
        }

        response = self.session.post('https://api.reya.xyz/api/owner/tos/add-signature', headers=self.session.headers, files=files).json()
        if response['signatureSavedSuccessfully']:
            logger.success(f'{self.address} - Успешно залогинился...')

    @retry
    def deposit(self):
        global send_list
        balance = self.get_balance('0x7F5c764cBc14f9669B88837ca1490cCa17c31607')
        balance_wei = balance['balance_wei']
        balance_eth = balance['balance']
        if self.check_allowance('0x7F5c764cBc14f9669B88837ca1490cCa17c31607', '0x9239609eED7c40C6DDcEC25D247Ef205103590B6') < balance_wei:
            logger.info(f'Reya: try approve token USDC.E...')
            send_list += self.approve(balance_wei, '0x7F5c764cBc14f9669B88837ca1490cCa17c31607', '0x9239609eED7c40C6DDcEC25D247Ef205103590B6')
            sleeping_between_transactions()

        response = requests.get('https://api.reya.xyz/api/socket/deposit-fees').json()
        value = int(response[1]['fees'])
        # print(json.dumps(response, indent=4))
        exacpayload = f'0xc06afe400000000000000000000000000000000000000000000000000000000000000001000000000000000000000000{self.address[2:]}0000000000000000000000000000000000000000000000000000000000000000'
        tx_data = get_tx_data_withABI(self, value=value)
        transaction = self.contract.functions.bridge(self.w3.to_checksum_address('0xCd2869d1eb1BC8991Bc55de9E9B779e912faF736'), balance_wei, 10000000, self.w3.to_checksum_address('0x6190855f54DeB642c410A2d642A993D454083736'), exacpayload, '0x').build_transaction(tx_data)

        logger.info(f'Reya: deposit {"{:0.9f}".format(balance_eth)} USDC.E')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'Reya: deposit {"{:0.9f}".format(balance_eth)} USDC.E : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}Reya: deposit {"{:0.9f}".format(balance_eth)} USDC.E - [tx hash]({self.scan + tx_hash})')
            logger.info(f'Жду депозита 40 сек...')
            time.sleep(40)

        else:
            logger.error(f'Reya: deposit {"{:0.9f}".format(balance_eth)} USDC.E : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}Reya: deposit {"{:0.9f}".format(balance_eth)} USDC.E - [tx hash]({self.scan + tx_hash})')

    @retry
    def daily_check(self):
        global send_list
        Reya.login(self)
        response = self.session.get(f'https://api.reya.xyz/api/xp/generate-game-boost-rate/{self.address}/child5', headers=self.session.headers).json()
        boostRate = response['boostRate']
        logger.success(f'{self.address} - Выпал буст {boostRate}X')
        response = self.session.get(f'https://api.reya.xyz/api/xp/get-referral-code/{self.address}', headers=self.session.headers).json()

        referralCode = response['referralCode']
        files = {
            'lockedInBoost': (None, boostRate),
            'referralURL': (None, ''),
        }

        response = self.session.post('https://api.reya.xyz/api/twitter/lock-game-boost-twitter-url', headers=self.session.headers, files=files).json()
        files = {
            'lockedInBoost': (None, boostRate),
            'referralURL': (None, f'https://reya.network/lge?referredBy={referralCode}'),
        }

        response = self.session.post('https://api.reya.xyz/api/twitter/lock-game-boost-twitter-url', headers=self.session.headers, files=files).json()
        response = self.session.get(f'https://api.reya.xyz/api/xp/lock-game-boost-rate/{self.address}', headers=self.session.headers)
        time.sleep(50)
        response = requests.get(f'https://api.reya.xyz/api/xp/xp-profile/{self.address}', headers=self.session.headers).json()
        xp_value = response['xp']['value']
        deposited = response['deposited']
        send_list += (f'\n{SUCCESS}Reya: {"{:0.2f}".format(xp_value)} XP | {"{:0.2f}".format(deposited)} USDC.E deposit | {boostRate}Boost')
        logger.success(f'{self.address} - {"{:0.2f}".format(xp_value)} XP | {"{:0.2f}".format(deposited)} USDC.E deposit | {boostRate}Boost')

    def main(self):
        global send_list
        send_list = ''
        if module == 1:
            Reya.login(self)
            Reya.deposit(self)
            Reya.daily_check(self)
        elif module == 2:
            Reya.daily_check(self)

        return send_list

class Okex(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.rpc = rpc
        self.Chain = 'Optimism (Bridged)'

    @retry
    def deposit_to_okex(self, addressokx):
        None

    def withdraw_from_okex(self):

        if transfer_subaccount:
            Okex.transfer_from_subaccount(self)
            print()
        delay = [3, 5]
        amount_to_withdrawal = round(random.uniform(amount[0], amount[1]), decimal_places)
        Okex.okx_withdraw(self, self.address, amount_to_withdrawal, 1)
        # Okex.choose_cex(self.address, amount_to_withdrawal, 1)
        time.sleep(random.randint(delay[0], delay[1]))
        self.wait_balance(int(amount_to_withdrawal * 0.8), rpc=self.rpc, contract_address=self.w3.to_checksum_address('0x7F5c764cBc14f9669B88837ca1490cCa17c31607'))
        # sleeping_between_transactions()
        return (f'\n{SUCCESS}OKx: Withdraw {"{:0.4f}".format(amount_to_withdrawal)} {symbolWithdraw}')

    def transfer_from_subaccount(self):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })

        list_sub = exchange.private_get_users_subaccount_list()
        for sub_data in list_sub['data']:
            name_sub = sub_data['subAcct']
            balance = exchange.private_get_asset_subaccount_balances({'subAcct': name_sub, 'ccy': symbolWithdraw})
            sub_balance = balance['data'][0]['bal']
            logger.info(f'OKx: {name_sub} balance : {sub_balance} {symbolWithdraw}')
            if float(sub_balance) > 0:
                transfer = exchange.private_post_asset_transfer(
                    {"ccy": symbolWithdraw, "amt": str(sub_balance), "from": '6', "to": '6', "type": "2",
                     "subAcct": name_sub})
                logger.success(f'OKx: transfer to main {sub_balance} {symbolWithdraw}')
            else:
                continue
        time.sleep(15)
        return True

    def okx_withdraw(self, address, amount_to_withdrawal, wallet_number):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })

        try:
            chainName = symbolWithdraw + "-" + self.Chain
            fee = Okex.get_withdrawal_fee(symbolWithdraw, chainName)
            exchange.withdraw(symbolWithdraw, amount_to_withdrawal, address,
                              params={
                                  "toAddress": address,
                                  "chainName": chainName,
                                  "dest": 4,
                                  "fee": fee,
                                  "pwd": '-',
                                  "amt": amount_to_withdrawal,
                                  "network": self.Chain
                              }
                              )
            logger.success(f'OKx: Вывел {amount_to_withdrawal} {symbolWithdraw}')
            return amount_to_withdrawal
        except Exception as error:
            logger.error(f'OKx: Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error}')

    def get_withdrawal_fee(symbolWithdraw, chainName):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })
        currencies = exchange.fetch_currencies()
        if chainName == 'Arbitrum':
            chainName = 'Arbitrum One'

        for currency in currencies:
            if currency == symbolWithdraw:
                currency_info = currencies[currency]
                network_info = currency_info.get('networks', None)
                if network_info:
                    for network in network_info:
                        network_data = network_info[network]
                        network_id = network_data['id']
                        if network_id == chainName:
                            withdrawal_fee = currency_info['networks'][network]['fee']
                            if withdrawal_fee == 0:
                                return 0
                            else:
                                return withdrawal_fee
        raise ValueError(f"не могу получить сумму комиссии, проверьте значения symbolWithdraw и network")



