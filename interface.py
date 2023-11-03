import threading
import time
import curses
from shared_resources import add_log, log_buffer, log_lock, start_event
from strategies.strategy1 import strategy1
from strategies.strategy2 import strategy2



def main(stdscr):
    global strategies_active
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.refresh()

    t1 = threading.Thread(target=strategy1)
    t2 = threading.Thread(target=strategy2)

    t1.daemon = True
    t2.daemon = True

    t1.start()
    t2.start()

    while True:
        height, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, "=" * width)
        title = "Multi Strategy Automated Trading System by Lange Invest"
        stdscr.addstr(1, (width - len(title)) // 2, title)
        stdscr.addstr(2, 0, "=" * width)

        menu_title = "============== Menu =============="
        stdscr.addstr(6, (width - len(menu_title)) // 2, menu_title)
        stdscr.addstr(7, (width - len("| 1. Go Live                     |")) // 2, "| 1. Go Live                     |")
        stdscr.addstr(8, (width - len("| 2. Status Report               |")) // 2, "| 2. Status Report               |")
        stdscr.addstr(9, (width - len("| 3. Performance Report          |")) // 2, "| 3. Performance Report          |")
        stdscr.addstr(10, (width - len("| q. Quit                        |")) // 2, "| q. Quit                        |")
        stdscr.addstr(11, (width - len("=================================")) // 2, "=================================")


        if start_event.is_set():
            stdscr.addstr(15, 0, f"Recent Logs:".ljust(width))

            with log_lock:
                for i, log_line in enumerate(list(log_buffer)[-5:]):
                    stdscr.addstr(16 + i, 0, log_line[:width])

        stdscr.refresh()

        choice = stdscr.getch()

        if choice == ord('1'):
            start_event.set()
            stdscr.addstr(13, 0, "System is Live".ljust(width))
            stdscr.addstr(13, 0, "System is Live".ljust(width))
        elif choice == ord('2'):
            stdscr.addstr(13, 0, "Status Report".ljust(width))
        elif choice == ord('3'):
            stdscr.addstr(13, 0, "Performance Report".ljust(width))
        elif choice == ord('q'):
            stdscr.nodelay(False)  # Make getch() blocking temporarily
            stdscr.addstr(13, 0, "Are you sure you want to quit (yes/no)?".ljust(width))
            stdscr.refresh()
            confirmation = stdscr.getch()
            if confirmation == ord('y'):
                break
            elif confirmation == ord('n'):
                stdscr.addstr(13, 0, "".ljust(width))  # Clear the quit message
            stdscr.nodelay(True)  # Make getch() non-blocking again

        stdscr.refresh()
        time.sleep(0.1)

if __name__ == '__main__':
    curses.wrapper(main)
