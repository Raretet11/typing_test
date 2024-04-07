from io_handler import IOHandler
import settings
from typing import List
from time import time
from os import listdir
from os.path import join


class SpeedTester:
    def __init__(self, IO_handler: IOHandler) -> None:
        self.IO_Handler: IOHandler = IO_handler
        
    def __handle_user_input(self, text_to_type: str) -> None:
        next_symbol_index: int = 0
        errors_amount: int = 0
        colors: List[str] = [settings.DEFAULT_COLOR for i in range(len(text_to_type))]
        have_mistake_on_this_step: bool = False
        
        started: bool = False
        start_time: float = 0.0
        while next_symbol_index < len(text_to_type):
            c = self.IO_Handler.get_user_input_char()
            if c == settings.OUTPUT_SYMBOL:
                break
            if text_to_type[next_symbol_index] != c:
                colors[next_symbol_index] = settings.WRONG_LETTER_COLOR
                errors_amount += 1
                have_mistake_on_this_step = True
            else:
                colors[next_symbol_index] = settings.RIGHT_LETTER_COLOR
                if have_mistake_on_this_step:
                    colors[next_symbol_index] = settings.RIGHT_WITH_MISTAKE_LETTER_COLOR
                next_symbol_index += 1
                have_mistake_on_this_step = False
            if not started:
                start_time = time()
                started = True
            self.IO_Handler.show_text(text_to_type, next_symbol_index, colors)
        finish_time: float = time()

        total_time: float = 0.0
        if started:
            total_time = finish_time - start_time
            
        self.IO_Handler.show_stat(total_time, errors_amount, len(text_to_type), next_symbol_index)

    def __run_speed_test(self, text_to_type: str) -> None:
        self.IO_Handler.show_text(text_to_type, 0, [settings.DEFAULT_COLOR for i in range(len(text_to_type))])
        self.__handle_user_input(text_to_type)
        self.choose_text()
              
    def __find_all_texts_path(self) -> List[str]:
        return listdir(settings.TEXTS_FOLDER)
    
    def __get_text(self, path: str) -> str:
        text: str = ''
        with open(join(settings.TEXTS_FOLDER, path)) as f:
            for line in f.readlines():
                text += line
        return text
        
    def choose_text(self) -> None:
        texts_path: List[str] = self.__find_all_texts_path()
        len_text: List[int] = [len(self.__get_text(path)) for path in texts_path]
        self.IO_Handler.show_all_texts(texts_path, len_text)
        
        choosed_text_ind: int = -1
        while choosed_text_ind == -1:
            self.IO_Handler.clear_screen()
            self.IO_Handler.show_all_texts(texts_path, len_text)
            choosed_text_ind = self.IO_Handler.get_user_input_choose_text(texts_path)
        
        self.__run_speed_test(self.__get_text(texts_path[choosed_text_ind]))
        
