from random import choice
import keyboard
import time
import os
from rich import print as rprint
from rich.console import Console
from commonEnglishWords import commonEnglishWordsArray
from progress.bar import ChargingBar



console = Console()
stringList: str = []

amountOfWords = 0

typedString: str = ''
mistakes: int = 0

def onKeyPress(event):
    global typedString, mistakes, stringToType
    
    if event.name in ['shift', 'alt', 'ctrl', 'tab', 'caps lock', 'enter']:
        pass
    elif event.name == 'space':
        typedString += ' '
    elif event.name == 'backspace':
        if typedString:
            typedString = typedString[:-1]
    else:
        if len(typedString) < len(stringToType):
            if event.name != stringToType[len(typedString)]:
                mistakes += 1
        typedString += event.name

def showStats(timeInterval, totalWords, totalMistakenWords):
    wpm = totalWords / (timeInterval / 60)
    
    if totalWords > 0:
        accuracy = ((totalWords - totalMistakenWords) / totalWords) * 100
        accuracy = max(accuracy, 0)  # Ensure accuracy is not negative
    else:
        accuracy = 100
    
    console.print(f"""
    [cyan1 bold]WPM[/cyan1 bold]: [cyan2 bold]{wpm:.1f}
""")
    with ChargingBar('Accuracy | ', empty_fill='·', color='cyan') as bar:
        for i in range(round(accuracy)):
            time.sleep(0.05)
            bar.next()


def main():
    global stringToType
    console.print(f"""
Choose a mode:
[red bold]0: Classic (30 random words)[/red bold]
[green bold]1: Custom amount of words[/green bold]
[blue bold]2: Custom text[/blue bold]
""")
    stringToType = ''
    while True:
        match input('Your choice [0, 1, 2]: '):
            case '0':
                for i in range(30):
                    stringToType += f'{choice(commonEnglishWordsArray)} '
                stringToType = stringToType[:-1]
                break
            case '1':
                for i in range(int(input('How much words do you what to type?\n'))):
                    stringToType += f'{choice(commonEnglishWordsArray)} '
                stringToType = stringToType[:-1]
                break
            case '2':
                stringToType = input('Enter your custom text:\n')
                break
            case _:
                console.print('[red bold]Choose a valid number![/red bold]')
    print(stringToType)
    keyboard.on_press(onKeyPress)
    startingTime = time.time()
    wordsTyped = len(stringToType.split())
    
    while 'Esc' not in typedString:
        if len(typedString) == len(stringToType):
            showStats(time.time() - startingTime, wordsTyped, mistakes)
            break
        else:
            if typedString == stringToType[0:len(typedString)]:
                dynamicString = f"[green]{typedString}[/green][bright_black]{stringToType.replace(stringToType[0:len(typedString)], '')}[/bright_black]"
            else:
                dynamicString = f"[red]{typedString}[/red][bright_black]{stringToType.replace(stringToType[0:len(typedString)], '')}[/bright_black]"
            
            os.system('cls' if os.name == 'nt' else 'clear')
            console.print(f'{dynamicString}\nMistakes : {mistakes}') 
            time.sleep(0.05)
    keyboard.unhook_all()

if __name__ == '__main__':
    main()
