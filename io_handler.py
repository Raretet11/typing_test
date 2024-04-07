import click
import os
from time import sleep
from typing import List
import settings

class IOHandler:
    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def __draw_progress_bar(self, max_value: int, current_value: int, length: int) -> None:
        progress = ""
        for i in range(length):
            if i < int(length * current_value / max_value):
                progress += "="
            else:
                progress += " "
        click.echo("[ %s ] %.2f%%" % (progress, current_value / max_value * 100))
    
    def show_text(self, text: str, next_symbol_index: int, colors: List[str]) -> None:
        self.clear_screen()
        self.__draw_progress_bar(len(text), next_symbol_index, settings.PROGRESS_BAR_LENGTH)
        symbols_in_line_amount: int = 0
        for i, char in enumerate(text):
            symbols_in_line_amount += 1
            click.echo(click.style(char, fg=colors[i]), nl=False)
            if symbols_in_line_amount >= settings.MAX_LINE_LENGTH:
                symbols_in_line_amount = 0
                click.echo()
        click.echo()
        click.echo(f"To exit type : '{settings.OUTPUT_SYMBOL}'\n")
        
    def get_user_input_char(self) -> str:
        c = click.getchar()
        return c
    
    def show_stat(self, total_time: float, errors_amount: int, text_len: int, last_ind: int) -> None:
        total_time_formated = click.style(str(round(total_time, 2)) + 's', fg=settings.IMPORTANT_INFORMATION_COLOR, bold=True)
        typing_speed_formated = click.style(round(last_ind / (total_time / 60), 2), fg=settings.IMPORTANT_INFORMATION_COLOR, bold=True)
        errors_amount_formated = click.style(errors_amount, fg=settings.BAD_INFORMATION_COLOR, bold=True)
        done_formated = click.style(str(round((last_ind / text_len) * 100.0, 2)) + '%', fg=settings.IMPORTANT_INFORMATION_COLOR, bold=True)
        click.echo(f'   Total time: {total_time_formated}')
        click.echo(f'   Typing speed: {typing_speed_formated} symbols per minute')
        click.echo(f'   Errors amount: {errors_amount_formated}')
        click.echo(f'   Done: {done_formated}')
        click.pause('\nPress any key to choose text again...')
        
    def show_all_texts(self, texts_path: List[str], texts_len: List[int]) -> None:
        click.echo('Hi there in this simple type speed checker')
        click.echo('To select text from the list, type its number: ')
        for i, text_path in enumerate(texts_path):
            i_formated: str = click.style(i, fg=settings.IMPORTANT_INFORMATION_COLOR, bold=True)
            text_name = text_path
            if '.' in text_name:
                text_name = text_name.split('.')[0]
            click.echo(f'{i_formated} - {text_name} : {texts_len[i]} symbols')

    def get_user_input_choose_text(self, texts_path: List[str]) -> str:
        c = click.prompt(f'Input text id (choose from 0 to {len(texts_path) - 1})')
        choosed_text_ind: int = -1
        if c.isdigit() and len(texts_path) > int(c) >= 0:
            choosed_text_ind = int(c)
        else:
            self.clear_screen()
            wrong_number_formated = click.style('wrong input', fg=settings.BAD_INFORMATION_COLOR, bold=True)
            click.echo(click.style(f'{wrong_number_formated}, try again!'))
            sleep(settings.WARNING_TIME)
        return choosed_text_ind