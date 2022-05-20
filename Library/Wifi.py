import wifi

def search():
    wifilist = []
    cells = wifi.Cell.all('wlan0')
    for cell in cells:
        wifilist.append(cell)
    return wifilist


def find_from_search_list(ssid):
    wifilist = search()
    for cell in wifilist:
        if cell.ssid == ssid:
            return cell
    return False


def find_from_saved_list(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)
    if cell:
        return cell
    return False


def connect(ssid, password=None):
    cell = find_from_search_list(ssid)

    if cell:
        savedcell = find_from_saved_list(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell

        # First time to conenct
        else:
            if cell.encrypted:
                if password:
                    scheme = add(cell, password)

                    try:
                        scheme.activate()

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        delete(ssid)
                        return False
                    return cell
                else:
                    return False
            else:
                scheme = add(cell)
                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    delete(ssid)
                    return False
                return cell
    return False


def add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme


def delete(ssid):
    if not ssid:
        return False

    cell = find_from_saved_list(ssid)
    if cell:
        cell.delete()
        return True
    return False