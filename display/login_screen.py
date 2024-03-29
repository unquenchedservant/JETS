import curses, sys
from utilities import login, menu as m, inputs
from display import main
import time

def menu(stdscr, main_pos):
    cursor_y = 2
    k = 0

    curses.curs_set(True)

    stdscr.clear()
    stdscr.refresh()
    valid_symbols = "!@#$%^&*()_-+={}[]"

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    title_str = "etsjets.org Login"
    user_label = "Username: "
    password_label = "Password: "
    x_pos_user = len(user_label) + 2
    x_pos_pass = len(password_label) + 2
    username = ""
    password_display = ""
    password = ""
    success = ""
    isError = False
    height, width = stdscr.getmaxyx()
    cursor_x = x_pos_user

    while(True):
        stdscr.clear()
        password_display = "*" * len(password)

        if isError == True and success == "Please enter a username":
            m.login_option(stdscr, user_label, 2, 2, cursor_y, True)
        else:
            m.login_option(stdscr, user_label, 2, 2, cursor_y, False)
        if isError == True and success == "Please enter a password":
            m.login_option(stdscr, password_label, 3, 2, cursor_y, True)
        else:
            m.login_option(stdscr, password_label, 3, 2, cursor_y, False)

        m.add_string(stdscr, username, 2, x_pos_user)
        m.add_string(stdscr, password_display, 3, x_pos_pass)

        m.title(stdscr, title_str)

        m.login_status(stdscr, isError, success, 4, curses.color_pair(2), curses.color_pair(4))



        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()

        if isError == False and success == "Successfully logged in! Returning to main menu...":
            time.sleep(5)
            main.start()
        k = stdscr.getch()

        if k == 27:
            main.start()
        elif k == 9:
            if cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_pass  + len(password)
            elif cursor_y == 3:
                cursor_y = 2
                cursor_x = x_pos_user + len(username)
        elif k == 10:
            if cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_pass
            elif cursor_y == 3:
                if len(username) == 0:
                    success = "Please enter a username"
                    cursor_y = 2
                    isError = True
                elif len(password) == 0:
                    success = "Please enter a password"
                    cursor_y = 3
                    isError = True
                else:
                    isLogged = login.set_login(username, password)
                    if isLogged:
                        success = "Successfully logged in! Returning to main menu..."
                        isError = False
                    else:
                        success = "Incorrect Login"
                        isError = True
        elif k == curses.KEY_UP or k == curses.KEY_DOWN:
            if cursor_y == 3:
                cursor_y = 2
                cursor_x = x_pos_user + len(username)
            elif cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_pass + len(password_display)
        elif k == curses.KEY_LEFT:
            if cursor_y == 2 and not cursor_x <= x_pos_user:
                cursor_x -= 1
            elif cursor_y == 3 and not cursor_x == x_pos_pass:
                cursor_x -= 1
        elif k == curses.KEY_RIGHT:
            if cursor_y == 2 and not cursor_x >= x_pos_user + len(username):
                cursor_x += 1
            elif cursor_y == 3 and not cursor_x >= x_pos_pass + len(password_display):
                cursor_x += 1
        elif cursor_y == 2:
            username = inputs.handler(username, k, x_pos_user, cursor_x)
            cursor_x = x_pos_user + len(username)
        elif cursor_y == 3:
            password = inputs.handler(password, k, x_pos_pass, cursor_x)
            cursor_x = x_pos_pass + len(password)

def start(main_pos):
    curses.wrapper(menu, main_pos)
