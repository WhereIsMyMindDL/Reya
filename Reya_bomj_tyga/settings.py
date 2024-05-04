
# ===================================== options ===================================== #

#------main-options------#
shuffle = False                                                     # True / False. если нужно перемешать кошельки
decimal_places = 7                                                  # количество знаков, после запятой для генерации случайных чисел
delay_wallets = [1, 2]                                              # минимальная и максимальная задержка между кошельками
delay_transactions = [3, 4]                                         # минимальная и максимальная задержка между транзакциями
RETRY_COUNT = 3                                                     # кол-во попыток при возникновении ошибок

#----Reya-options----#
module = 1                                                          # 1 - депозит-клейм буста, 2 - клейм буста

#------okex-options------#
amount = [35, 37]                                                   # минимальная и максимальная сумма на вывод
transfer_subaccount = False                                         # перевод эфира с суббакков на мейн, используется в Okex_withdrawal

class API:
    # okx API
    okx_apikey = ""
    okx_apisecret = ""
    okx_passphrase = ""

#------bot-options------#
bot_status = False                                                  # True / False
bot_token  = ''                                                     # telegram bot token
bot_id     = 0                                                      # telegram id
  
''' Modules: Okex_withdrawal, Reya '''

rotes_modules = [
            ['Okex_withdrawal'],
            ['Reya'],
]

# =================================== end-options =================================== #


