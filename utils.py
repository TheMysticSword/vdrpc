supported_game_versions = ["2.4"]

def get_memory_addresses(game_version):
    memory_addresses = dict()

    if game_version == "2.4":
        memory_addresses["in_game"] = (0x238B35) # byte
        memory_addresses["in_secret_lab"] = (0x2276A2) # byte
        memory_addresses["in_custom_level"] = (0x227789) # byte
        memory_addresses["in_time_trial"] = (0x416938) # byte
        memory_addresses["room_name"] = (0x237B98) # string
        memory_addresses["gravitron_mode"] = (0x4168E8) # integer
        memory_addresses["gravitron_current_time"] = (0x416904) # integer
        memory_addresses["gravitron_best_time"] = (0x416910) # integer
        memory_addresses["custom_level_index"] = (0x416894) # integer
        memory_addresses["room_x"] = (0x41676C) # integer, 100 + actual room x
        memory_addresses["room_y"] = (0x416770) # integer, 100 + actual room y
        memory_addresses["trinkets"] = (0x2276A0) # byte array of size 100
        memory_addresses["deaths"] = (0x4167F4) # integer
        memory_addresses["timer_seconds"] = (0x416804) # integer
        memory_addresses["timer_minutes"] = (0x416808) # integer
        memory_addresses["timer_hours"] = (0x41680C) # integer
        memory_addresses["time_trial_par"] = (0x416970) # integer
    
    return memory_addresses

area_map = [
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 4, 4, 4, 4, 3, 3, 3, 3],
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 4, 4, 4, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 4, 4, 4, 5, 5, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 4, 4, 4, 4, 4, 4, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0],
    [0, 0, 6, 6, 6, 0, 0, 0, 0, 2, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0],
    [0, 0, 6, 6, 6, 0, 0, 0, 0, 2, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 4, 4, 4, 4, 4, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 4, 4, 4, 4, 4, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 4, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
area_names = [
    "Dimension VVVVVV",
    "Laboratory",
    "The Tower",
    "Warp Zone",
    "Space Station",
    "Dimension VVVVVV",
    "The Ship"
]

def get_room_area_id(room_x:int, room_y:int):
    if room_x >= 0 and room_x < 20 and room_y >= 0 and room_y < 20:
        return area_map[room_y][room_x]
    return -1

def get_area_name(area_id):
    if area_id >= 0 and area_id < len(area_names):
        return area_names[area_id]
    return "???"

def time_to_string(frames:int, always_show_minutes:bool = False):
    seconds = frames / 30

    c = int((seconds % 1) * 100)
    s = int(seconds % 60)
    m = int((seconds / 60) % 60)
    h = int(seconds / 3600)

    if h > 0:
        time_string = f"{h}:{str(m).zfill(2)}:{str(s).zfill(2)}"
        if frames != -1:
            time_string += f".{str(c).zfill(2)}"
        return time_string
    elif m > 0 or always_show_minutes or frames == -1:
        time_string = f"{m}:{str(s).zfill(2)}"
        if frames != -1:
            time_string += f".{str(c).zfill(2)}"
        return time_string
    else:
        return f"{s}.{str(c).zfill(2)}"
