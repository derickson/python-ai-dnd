import platform

if platform.system() == 'Linux':
    import sys
    import tty
    import termios
    
    def getch():
        """
        Read a single character of input from the console on Linux.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char
    
else:
    import msvcrt
    
    def getch():
        """
        Read a single character of input from the console on Windows.
        """
        char = msvcrt.getch()
        return char.decode('utf-8')
