import time

import win32clipboard


def get_str_from_clipboard(f, last_data=''):
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    if data != last_data:
        f.write(data + '\n')

    return data


def main(interval_time=1.0):
    f = open('words.txt', 'w')
    t = time.time()
    last_data = ''

    while True:
        if time.time() - t >= interval_time:
            last_data = get_str_from_clipboard(f, last_data)
            if last_data == 'exit' == 'quit':
                break
            t = time.time()

    f.close()


main()
