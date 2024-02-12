import curses
from curses import wrapper
from curses import textpad
import time
import random



def get_string():
	with open("text.txt", 'r') as f:
		txt = f.read().split('\n\n')
		l = len(txt)

	return txt[random.randint(0, l-1)]


def start_screen(stdscr):
	hello_message = "Welcome to the Konsole type!"
	press_message = "press any key to begin!"
	hint_messages = "press Esc to exit"

	stdscr.clear()
	maxY, maxX = stdscr.getmaxyx()

	stdscr.addstr(maxY//3, (maxX-len(hello_message))//2, hello_message.upper())
	stdscr.addstr(maxY//3+1, (maxX-len(press_message))//2, press_message)
	stdscr.addstr(maxY//3+4, (maxX-len(hint_messages))//2, hint_messages)


	stdscr.refresh()
	stdscr.getkey()


def time_format(delta_time):
	delta_time = int(delta_time)
	m = delta_time//60
	s = delta_time%60
	res=""
	if m < 10:
		res+="0"+str(m)
	else:
		res+=str(m)

	res+=':'
	if s < 10:
		res+="0"+str(s)
	else:
		res+=str(s)

	return res



def display_wpm_acc(stdscr, wpm=0, acc=0, start_time=0):
	maxY, maxX = stdscr.getmaxyx()

	textpad.rectangle(stdscr, 1, 25, 4, maxX-25)
	end_time = time.time()
	delta = end_time - start_time
	stdscr.addstr(2, 27, f"WPM: {wpm}  ACC: {acc}%"  +       " "*(maxX-86)            + f"TIME: {time_format(delta)}")


def display_text(stdscr, target_text, current_text, wpm=0, acc=0, current_row=0, start_time=0):
	maxY, maxX = stdscr.getmaxyx()
	lengthOftexts = sum([len(s) for s in target_text])

	display_wpm_acc(stdscr, wpm, max(100-round(acc/lengthOftexts*100), 0), start_time)
	
	for ind in range(len(target_text)):
		cp = 0
		if ind > current_row:
			cp = 9
		stdscr.addstr(6+ind, (maxX-len(target_text[ind]))//2, target_text[ind], curses.color_pair(cp))

	for i in range(len(current_text)):
		for j in range(len(current_text[i])):

			cp = 11 # green color 
			if current_text[i][j] != target_text[i][j]:
				cp = 197 # red color

			if current_text[i][j] == ' ' and cp == 197:
				current_text[i][j] = "@"
			stdscr.addstr(6+i, (maxX-len(target_text[i]))//2+j, current_text[i][j], curses.color_pair(cp))


def isfinish(current_text, target_text):
	for idx, text in enumerate(target_text):
		if "".join(current_text[idx]) != text:
			return False
	return True


def calculate_acc(current_text, target_text):

	cnt = 0
	for i in range(len(current_text)):
		for j in range(len(current_text[i])):
			if current_text[i][j] != target_text[i][j]:
				cnt+=1
	return cnt


def wpm_test(stdscr):
	target_text = get_string().split('\n') # сам текст

	current_text = [[] for _ in range(len(target_text))] # текущий текст (надо умножить его количество строк в самом предлодения сверху)

	acc = 0
	wpm = 0
	typed_word = 0
	current_row = 0

	start_time = time.time()
	stdscr.nodelay(True)

	
	while True:

		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((typed_word // (time_elapsed/60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm, acc,  current_row, start_time) # вывод текста на экран
		stdscr.refresh()

		
		if isfinish(current_text, target_text):
			stdscr.nodelay(False)
			break
		

		try:
			key = stdscr.getkey()
			if ord(key) == 27:
				stdscr.nodelay(False)
				break
		except:
			continue


		if key in ("KEY_BACKSPACE", '\b', '\x7f'):
			if len(current_text[current_row]) == 0 and current_row > 0:
				current_row-=1
			if len(current_text[current_row]) > 0:
				current_text[current_row].pop()

		elif key =='\n' or (key==' ' and len(current_text[current_row]) == len(target_text[current_row])):
			if current_row < len(target_text)-1:
				current_row+=1


		elif len(current_text[current_row]) < len(target_text[current_row]):
			current_text[current_row].append(key)
			typed_word+=1
			acc = max(acc, calculate_acc(current_text, target_text))


def main(stdscr):

	stdscr.clear()
	curses.start_color()
	curses.use_default_colors()
	for i in range(0, 255):
		curses.init_pair(i + 1, i, -1)
	
	start_screen(stdscr)

	while True:

		wpm_test(stdscr)

		stdscr.addstr(10, 0, "THE END! press any key to continue...")

		

		try:
			key = stdscr.getkey()
			if ord(key) == 27:
				break
		except:
			continue

	
wrapper(main)