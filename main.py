from speed_tester import SpeedTester
from io_handler import IOHandler

IO_handler: IOHandler = IOHandler()
speed_tester: SpeedTester = SpeedTester(IO_handler)
speed_tester.choose_text()
