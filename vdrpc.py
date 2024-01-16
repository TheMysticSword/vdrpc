from threading import Thread

import pymem
import pymem.process
import time
from config import config
from utils import get_room_area_id, get_area_name, get_memory_addresses, supported_game_versions, time_to_string

if config['game_version'] not in supported_game_versions:
    print(f"Game version {config['game_version']} unsupported")
    while True:
        pass

addr = get_memory_addresses(config['game_version'])
emoji_trinket = "\U0001f7e3"
emoji_deaths = "\U0001f480"

from pypresence import Presence
try:
    RPC = Presence(config['client_id'])
    RPC.connect()
except Exception as e:
    print(e)
    while True:
        pass

def memory_loop(RPC:Presence):
    pm = pymem.Pymem("VVVVVV.exe")
    module = pymem.process.module_from_name(pm.process_handle, "vvvvvv.exe")
    module_addr = module.lpBaseOfDll

    while True:
        rpc_state = None
        rpc_details = None
        rpc_start = None
        rpc_end = None

        try:
            in_game = pm.read_bool(module_addr + addr["in_game"])
            if in_game:
                if pm.read_int(module_addr + addr["gravitron_mode"]) == 1:
                    best_time = pm.read_int(module_addr + addr["gravitron_best_time"])

                    rpc_state = "In the Super Gravitron"
                    rpc_details = f"Best Time: {time_to_string(best_time)}"
                elif pm.read_bool(module_addr + addr["in_secret_lab"]):
                    rpc_state = "Exploring Dimension VVVVVV"
                else:
                    game_time = pm.read_int(module_addr + addr["timer_seconds"]) + pm.read_int(module_addr + addr["timer_minutes"]) * 60 + pm.read_int(module_addr + addr["timer_hours"]) * 60 * 60
                    deaths = pm.read_int(module_addr + addr["deaths"])
                    trinkets = 0
                    for byte in pm.read_bytes(module_addr + addr["trinkets"], 100):
                        if byte == 1:
                            trinkets += 1
                    
                    current_room_name = pm.read_string(module_addr + addr["room_name"])
                    
                    playing_custom_level = pm.read_bool(module_addr + addr["in_custom_level"])
                    if not playing_custom_level:
                        rpc_state = "Exploring Dimension VVVVVV"
                        room_x = pm.read_int(module_addr + addr["room_x"])
                        room_y = pm.read_int(module_addr + addr["room_y"])
                        current_area_id = get_room_area_id(room_x - 100, room_y - 100)
                        if current_area_id == -1:
                            rpc_state = "Outside of Dimension VVVVVV"
                            rpc_details = current_room_name
                        elif current_area_id == 0:
                            pass
                        else:
                            current_area_name = get_area_name(current_area_id)
                            rpc_details = current_area_name
                            if len(current_room_name) > 0:
                                rpc_details = f"{current_area_name} - {current_room_name}"
                    else:
                        rpc_state = "Playing Custom Level"
                        if len(current_room_name) > 0:
                            rpc_details = f"Room: {current_room_name}"
                    
                    extra_info = f"{trinkets}{emoji_trinket} | {deaths}{emoji_deaths}"
                    if rpc_details:
                        rpc_details += f" ({extra_info})"
                    else:
                        rpc_details = extra_info
                    rpc_start = int(time.time()) - game_time

                    if pm.read_bool(module_addr + addr["in_time_trial"]):
                        rpc_state = "In a Time Trial"

                        par_time = pm.read_int(module_addr + addr["time_trial_par"])
                        rpc_end = int(time.time()) - game_time + par_time
            else:
                rpc_state = "In Menu"
            
            if RPC:
                RPC.update(state=rpc_state, details=rpc_details, start=rpc_start, end=rpc_end)

            time.sleep(15)
        except Exception as e:
            print("Error")
            print(e)
            break

memory_loop_thread = Thread(target=memory_loop, args=(RPC,), daemon=True)
memory_loop_thread.start()

while True:
    pass
