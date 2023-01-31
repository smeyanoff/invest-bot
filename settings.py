from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from tinkoff.invest import CandleInterval, Client

TOKEN = "YOUR_TOKEN"
ENVIRONMENT = 'sandbox'
if ENVIRONMENT == 'sandbox':
    ENVIRONMENT = INVEST_GRPC_API_SANDBOX
