import sys
import platform

MOUSE_MAP = {
    "1": "left",
    "2": "right",
    "3": "middle",
    "4": "x1",
    "5": "x2",
}

def linux(target_key):
    # may be slow
    import evdev
    from evdev import InputDevice, ecodes

    if target_key in MOUSE_MAP:
        btn_map = {
            "1": ecodes.BTN_LEFT,
            "2": ecodes.BTN_RIGHT,
            "3": ecodes.BTN_MIDDLE,
            "4": ecodes.BTN_SIDE,
            "5": ecodes.BTN_EXTRA
        }
        btn_code = btn_map[target_key]

        # Scan devices
        for path in evdev.list_devices():
            try:
                dev = InputDevice(path)
                if btn_code in dev.active_keys():
                    print("1")
                    return
            except Exception:
                continue
        print("0")
        return

    key_code = None
    if len(target_key) == 1 and target_key.isalnum():
        key_code = getattr(ecodes, f"KEY_{target_key.upper()}", None)
    else:
        key_code = getattr(ecodes, f"KEY_{target_key.upper()}", None)

    if key_code is None:
        print("-1")
        return

    for path in evdev.list_devices():
        try:
            dev = InputDevice(path)
            if key_code in dev.active_keys():
                print("1")
                return
        except Exception:
            continue
    print("0")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <ankey|1-5>")
        return

    target_key = sys.argv[1].lower()
    system = platform.system()

    if system == "Windows":
        import keyboard
        import mouse

        # Mouse check
        if target_key in MOUSE_MAP:
            btn_name = MOUSE_MAP[target_key]
            pressed = mouse.is_pressed(btn_name)
            print("1" if pressed else "0")
            return

        # Keyboard check
        try:
            pressed = keyboard.is_pressed(target_key)
            print("1" if pressed else "0")
        except Exception:
            print("-1")

    elif system == "Linux":
        linux(target_key)

    else:
        print(f"Unsupported platform: {system}")

if __name__ == "__main__":
    main()
