# Third-Party Imports
from fastapi import FastAPI, HTTPException
from mactools import MacAddress, get_oui_record
from mactools.tools_common import get_hex_value

app = FastAPI()

@app.get('/mac/{mac_address}')
async def read_mac_details(mac_address: str):
    """
    Processes and returns a variety of info regarding the MAC/OUI Provided
    """
    mac_hex_value = get_hex_value(mac_address)

    if mac_hex_value == -1:
        raise HTTPException(status_code=400, detail='Invalid format')

    # Attempt first to validate a full MAC address
    if mac_hex_value in [48, 64]:
        mac = MacAddress(mac_address)
        return {'mac': mac.colon,
                'vendor': mac.vendor,
                'oui': mac.oui,
                'binary': mac.binary,
                'decimal': mac.decimal,
                # 'address': mac.oui_record.get('address')
            }
    
    if mac_hex_value > 64:
        # Too long to be a MAC address
        raise HTTPException(status_code=400, detail='Too long to be a MAC address')
    
    if mac_hex_value < 24:
        # Too short to be an OUI
        raise HTTPException(status_code=400, detail='Too shot to be an OUI (shortest is 6 characters without delimiters such as XX:XX:XX)')
    
    # Check partials to see if it matches an 
    elif (oui_record := get_oui_record(mac_address)):
        return oui_record
