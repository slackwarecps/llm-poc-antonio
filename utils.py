import datetime
import pytz


def filter_assistants(items):
    # Filtrar a lista para incluir apenas os itens com role="assistant"
    assistants = [item for item in items if item.get('role') == "assistant"]
    return assistants


def func_converteDataPochToBR(epochDate):

    # Epoch timestamp provided
    epoch_timestamp = epochDate  # 1704461349

    # Convert epoch to datetime in UTC
    utc_time = datetime.datetime.utcfromtimestamp(epoch_timestamp)

    # Define the timezone for São Paulo/Brazil
    saopaulo_tz = pytz.timezone('America/Sao_Paulo')

    # Convert UTC time to São Paulo time
    saopaulo_time = utc_time.replace(tzinfo=pytz.utc).astimezone(saopaulo_tz)

    # Format the time to the Brazilian format
    formatted_time = saopaulo_time.strftime('%d/%m/%Y %H:%M:%S')

    return formatted_time


def func_agora_epoch():
    tz_sao_paulo = pytz.timezone('America/Sao_Paulo')
    datetime_sao_paulo = datetime.datetime.now(tz_sao_paulo)
    return int(datetime_sao_paulo.timestamp())
