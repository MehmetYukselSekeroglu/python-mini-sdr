from rtlsdr import RtlSdr




def list_of_device_in_system_id() -> dict:
    device_list = RtlSdr.get_device_serial_addresses()
    
    if len(device_list) == 0:
        return {
            "success" : "false",
            "message" : "no devices found"
        }    
    else:
        return {
            "success": "true",
            "data": device_list
        }
    

    
