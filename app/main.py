# Python Modules
from logging import basicConfig, getLogger, INFO
from os import makedirs, path

# Third-Party Imports
from fastapi import FastAPI, HTTPException, Request
from mactools import MacAddress, get_oui_record
from mactools.tools_common import get_hex_value

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Start the App and services
makedirs('logs', exist_ok=True)
basicConfig(filename=path.join('logs', 'main.log'), level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = getLogger(__name__)

logger.info('Initialing service Mactools-api.')

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

logger.info('Initialization completed, service running.')

@app.get('/mac/{mac_address}')
@limiter.limit("5/second")
async def read_mac_details(request: Request, mac_address: str):
    """
    Processes and returns a variety of info regarding the MAC/OUI Provided
    """
    ip, port = request.client
    log_result = lambda code, detail: logger.info(f'[{ip}:{port} - {mac_address} - {code} {detail}]')
    mac_hex_value = get_hex_value(mac_address)

    if mac_hex_value == -1:
        detail = 'Invalid format'
        log_result(400, detail)
        raise HTTPException(status_code=400, detail=detail)

    # Attempt first to validate a full MAC address
    if mac_hex_value in [48, 64]:
        mac = MacAddress(mac_address)
        log_result(200, 'Full MAC hit')
        return {'mac': mac.colon,
                'vendor': mac.vendor,
                'oui': mac.oui,
                'binary': mac.binary,
                'decimal': mac.decimal,
                # 'address': mac.oui_record.get('address')
            }
    
    if mac_hex_value > 64:
        # Too long to be a MAC address
        detail = 'Too long to be a MAC address'
        log_result(400, detail)
        raise HTTPException(status_code=400, detail=detail)
    
    if mac_hex_value < 24:
        # Too short to be an OUI
        detail = 'Too shot to be an OUI (shortest is 6 characters without delimiters such as XX:XX:XX)'
        log_result(400, detail)
        raise HTTPException(status_code=400, detail=detail)
    
    # Check partials to see if it matches an 
    elif (oui_record := get_oui_record(mac_address)):
        log_result(200, 'OUI Cache hit')
        return oui_record
        