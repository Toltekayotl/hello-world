import time
from bot_func import *
from bot_config import *
from pprint import pprint


try:
    # Загружаем конфигурацию из bot_config.py
    debug = DEBUG
    token = TOKEN['Token']

    # Отправляем себе личное сообщение при запуске
    send_telegram(TELEGRAM['user_id'], ' Bot started & load config\n')
    if debug:
        d = 'Debug: {}\nToken: {}\n'
        print(d.format(debug, token))
    # Создаем новый словарь operations
    token_operations_dict = OPERATIONS

    while True:
    
        # Задержка между итерациями в секундах
        timeout = 10
        # Получаем текущее время
        timestamp_now, dt_object_now = get_time_now()
        if debug:
            print(' * Date Time:', dt_object_now, '| Time Stamp:', timestamp_now)
        
        # Вызываем историю по адресу токена
        # token_call = Token(address=token)
        token_history = get_token_history('10')  # max 1000
        token_history_operations = token_history['operations']
        if debug:
            pprint(token_history)

        previous_operation_timestamp = token_operations_dict['operations'][0]['timestamp']
        last_operation_timestamp = token_history['operations'][0]['timestamp']
        
        # Проверяем кол-во операций в истории def 10 max 1k
        operations_count = len(token_history['operations']) - 1
        first_operation_timestamp = token_history['operations'][operations_count]['timestamp']
        
        # Если timestamp значения не совпадают
        if previous_operation_timestamp != last_operation_timestamp:
            # Значит была как минимум одна новая транзакция
            # Обновляем словарь
            token_operations_dict.update({'operations': [
                {'timestamp': first_operation_timestamp, 'transactionHash': ''}
            ]})
            if debug:
                print('NOW:', dt_object_now, 'FOUND new timestamp:', first_operation_timestamp)
                print(token_operations_dict)

            # сортировка по  возрастанию значения ключа timestamp
            # sorted(token_history_operations, key=lambda x: x['timestamp'])
            # Перебираем историю
            for operations in sorted(token_history_operations, key=lambda x: x['timestamp']):
                if debug:
                    print(operations['timestamp'])

                # Если время транзакции идентично времени предыдущей
                if operations['timestamp'] > previous_operation_timestamp:

                    if operations['from'] == TOKEN['Genesis Block']:
                        # Отсылаем инфу в телегу
                        tx_type = operations['type']
                        tx_value = int(operations['value'])
                        decimals = int(operations['tokenInfo']['decimals'])
                        div_dcm = int('1' + '0' * decimals)
                        h_tx_value = float(tx_value / div_dcm)
                        name = operations['tokenInfo']['name']
                        tx_from = operations['from']
                        tx_to = operations['to']
                        tx_hash = operations['transactionHash']

                        es_explore = 'https://etherscan.io/tx/' + tx_hash
                        ep_explore = 'https://ethplorer.io/tx/' + tx_hash

                        s = '✅ Minted {: .8f} {} to address: {}\n\n {}'
                        message = s.format(h_tx_value, name, tx_to, es_explore)
                        send_telegram(TELEGRAM['channel_id'], message)

                        # Обновляем словарь
                        token_operations_dict.update({'operations': [
                            {'timestamp': last_operation_timestamp, 'transactionHash': operations['transactionHash']}
                        ]})
                        if debug:
                            print(token_operations_dict['operations'][0]['transactionHash'])

                    if operations['to'] == TOKEN['Genesis Block']:
                        # Отсылаем инфу в телегу
                        tx_type = operations['type']
                        tx_value = int(operations['value'])
                        decimals = int(operations['tokenInfo']['decimals'])
                        div_dcm = int('1' + '0' * decimals)
                        h_tx_value = float(tx_value / div_dcm)
                        name = operations['tokenInfo']['name']
                        tx_from = operations['from']
                        tx_to = operations['to']
                        tx_hash = operations['transactionHash']

                        es_explore = 'https://etherscan.io/tx/' + tx_hash
                        ep_explore = 'https://ethplorer.io/tx/' + tx_hash

                        s = '🔥 Burned {: .8f} {} from address: {}\n\n {}'
                        message = s.format(h_tx_value, name,  tx_from, es_explore)
                        send_telegram(TELEGRAM['channel_id'], message)

                        # Обновляем словарь
                        token_operations_dict.update({'operations': [
                            {'timestamp': last_operation_timestamp, 'transactionHash': operations['transactionHash']}
                        ]})
                time.sleep(timeout)
        print('NOW:', dt_object_now, 'SEARCH for timestamp:', previous_operation_timestamp)
        print('-' * 15, '\n')
        time.sleep(timeout)

except KeyboardInterrupt:
    pass

except Exception as errex:
    send_telegram(TELEGRAM['user_id'], ' Bot stopped\nGeneral exception: [' + type(errex).__name__ + ']')
    print('General exception: [' + type(errex).__name__ + ']', errex)

exit()
