import click
import os
from time import time
from typing import List

class SpeedTester:
    def __clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def __show_text(self, text: str, colors: List[str] = None) -> None:
        self.__clear_screen()
        for i, char in enumerate(text):
            current_color: str = 'white'
            if not (colors is None):
                current_color = colors[i]
            click.echo(click.style(char, fg=current_color), nl=False)
        click.echo()
        
    def __get_user_input_char(self) -> str:
        c = click.getchar()
        return c
    
    def __show_stat(self, total_time: float, error_amount: int) -> None:
        total_time_formated = click.style(round(total_time, 2), fg='green', bold=True)
        click.echo(f'Total time: {total_time_formated} s')
        click.echo(f'Errors amount: {error_amount}')
    
    def __handle_user_input(self, text_to_type: str) -> None:
        next_symbol_index: int = 0
        errors_amount: int = 0
        colors: List[str] = ['white' for i in range(len(text_to_type))]
        have_mistake_on_this_step: bool = False
        
        start_time: float = time()
        while next_symbol_index < len(text_to_type):
            c = self.__get_user_input_char()
            if text_to_type[next_symbol_index] != c:
                colors[next_symbol_index] = 'red'
                errors_amount += 1
                have_mistake_on_this_step = True
            else:
                colors[next_symbol_index] = 'green'
                if have_mistake_on_this_step:
                    colors[next_symbol_index] = 'yellow'
                next_symbol_index += 1
                have_mistake_on_this_step = False
            self.__show_text(text_to_type, colors)
        finish_time: float = time()

        self.__show_stat(finish_time - start_time, errors_amount)
        

    def run(self, text_to_type: str) -> None:
        self.__show_text(text_to_type)
        self.__handle_user_input(text_to_type)
