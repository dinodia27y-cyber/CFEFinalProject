import random
import tkinter as tk


countries = []
score = 0
question_queue = []
question_index = 0
total_questions = 10
current_question = None
current_mode = 'mix up'
image_cache = {}
MAX_OPTIONS = 4


def pick_unique(items, count):
    pool = list(items)
    chosen = []
    while pool and len(chosen) < count:
        selection = random.choice(pool)
        chosen.append(selection)
        pool.remove(selection)
    return chosen


FACT_FILES = {
    'United States': 'facts/US.txt',
    'Japan': 'facts/JP.txt',
    'United Kingdom': 'facts/GB.txt',
    'Mexico': 'facts/MX.txt',
    'Canada': 'facts/CA.txt',
    'India': 'facts/IN.txt',
    'France': 'facts/FR.txt',
    'Turkey': 'facts/TR.txt',
    'China': 'facts/CN.txt',
    'Saudi Arabia': 'facts/SA.txt',
    'Argentina': 'facts/AR.txt',
    'Belgium': 'facts/BE.txt',
    'South Africa': 'facts/ZA.txt',
    'Cuba': 'facts/CU.txt',
    'New Zealand': 'facts/NZ.txt',
    'Niger': 'facts/NE.txt',
    'Greece': 'facts/GR.txt',
    'Iraq': 'facts/IQ.txt',
    'Bangladesh': 'facts/BD.txt',
    'Hong Kong': 'facts/HK.txt',
    'Angola': 'facts/AO.txt',
    'Bahamas': 'facts/BS.txt',
    'Montenegro': 'facts/ME.txt',
    'United Arab Emirates': 'facts/AE.txt',
    'Jordan': 'facts/JO.txt',
    'Nicaragua': 'facts/NI.txt'
}


FLAG_IMAGES = {
    'United States': 'data/easy/US.png',
    'Japan': 'data/easy/JP.png',
    'United Kingdom': 'data/easy/GB.png',
    'Mexico': 'data/easy/MX.png',
    'Canada': 'data/easy/CA.png',
    'India': 'data/easy/IN.png',
    'France': 'data/easy/FR.png',
    'Turkey': 'data/standard/TR.png',
    'China': 'data/standard/CN.png',
    'Saudi Arabia': 'data/standard/SA.png',
    'Argentina': 'data/standard/AR.png',
    'Belgium': 'data/standard/BE.png',
    'South Africa': 'data/standard/ZA.png',
    'Cuba': 'data/advanced/CU.png',
    'New Zealand': 'data/advanced/NZ.png',
    'Niger': 'data/advanced/NE.png',
    'Greece': 'data/advanced/GR.png',
    'Iraq': 'data/advanced/IQ.png',
    'Bangladesh': 'data/advanced/BD.png',
    'Hong Kong': 'data/advanced/HK.png',
    'Angola': 'data/expert/AO.png',
    'Bahamas': 'data/expert/BS.png',
    'Montenegro': 'data/expert/ME.png',
    'United Arab Emirates': 'data/expert/AE.png',
    'Jordan': 'data/expert/JO.png',
    'Nicaragua': 'data/expert/NI.png'
}


EASY = ['United States', 'Japan', 'United Kingdom', 'Mexico', 'Canada', 'India', 'France']
STANDARD = ['Turkey', 'China', 'Saudi Arabia', 'Argentina', 'Belgium', 'South Africa']
ADVANCED = ['Cuba', 'New Zealand', 'Niger', 'Greece', 'Iraq', 'Bangladesh', 'Hong Kong']
EXPERT = ['Angola', 'Bahamas', 'Montenegro', 'United Arab Emirates', 'Jordan', 'Nicaragua']

MODE_GROUPS = {
    'mix up': EASY + STANDARD + ADVANCED + EXPERT,
    'easy': EASY,
    'standard': STANDARD,
    'advanced': ADVANCED,
    'expert': EXPERT
}


def read_fact(path):
    with open(path, 'r') as file:
        return file.read().strip()


def load_data(choice):
    countries.clear()
    for name in MODE_GROUPS[choice]:
        fact_path = FACT_FILES[name]
        countries.append({'country': name, 'fact': read_fact(fact_path)})


def show_screen(screen):
    screen.tkraise()


def update_score():
    global score
    score += 1
    score_label.config(text='Score: ' + str(score))


def handle_answer(answer):
    global current_question, question_index
    if current_question is None:
        return

    guess = str(answer).strip().lower()
    is_correct = guess == current_question['country'].lower()
    if is_correct:
        update_score()
        header = 'Nice job!'
    else:
        header = 'Not quite.'

    message = header + '\n\nCorrect answer: ' + current_question['country'] + '\n\n' + current_question['fact']
    question_index += 1
    show_fact_screen(message)
    current_question = None


def make_answer_handler(value):
    def handler():
        handle_answer(value)
    return handler


def go_back_to_quiz():
    show_screen(quiz_screen)
    ask_question()


def finish_game():
    result_label.config(text='Final Score: ' + str(score) + '/' + str(len(question_queue)))
    show_screen(result_screen)


def start_game():
    global score, question_index, current_question, question_queue, image_cache

    load_data(current_mode)
    score = 0
    question_index = 0
    current_question = None
    image_cache = {}
    question_queue = pick_unique(countries, min(total_questions, len(countries)))

    if not question_queue:
        show_screen(start_screen)
        return

    score_label.config(text='Score: 0')
    show_screen(quiz_screen)
    ask_question()


def show_flag_picture(name):
    if name not in image_cache:
        image_cache[name] = tk.PhotoImage(file=FLAG_IMAGES[name], master=window)

    photo = image_cache[name]
    picture_label.config(image=photo)
    picture_label.image = photo


def show_fact_screen(text):
    fact_message.config(text=text)
    show_screen(fact_screen)


def build_options(correct_country):
    pool = [entry['country'] for entry in countries if entry['country'] != correct_country]
    distractors = pick_unique(pool, min(MAX_OPTIONS - 1, len(pool)))
    options = distractors
    insert_at = random.choice(range(len(options) + 1))
    options.insert(insert_at, correct_country)
    return options


def ask_question():
    global current_question

    if question_index >= len(question_queue):
        finish_game()
        return

    current_question = question_queue[question_index]
    question_label.config(text='Question ' + str(question_index + 1) + '/' + str(len(question_queue)))

    if current_mode in ('advanced', 'expert'):
        for button in option_buttons:
            button.pack_forget()
        answer_entry.delete(0, tk.END)
        answer_entry.pack(pady=5)
        submit_button.pack(pady=5)
    else:
        answer_entry.pack_forget()
        submit_button.pack_forget()
        options = build_options(current_question['country'])
        for idx in range(len(option_buttons)):
            if idx < len(options):
                name = options[idx]
                button = option_buttons[idx]
                button.config(text=name, state='normal', command=make_answer_handler(name))
                button.pack(pady=5)
            else:
                option_buttons[idx].pack_forget()

    show_flag_picture(current_question['country'])


def go_home():
    show_screen(start_screen)


def submit_typing():
    text = answer_entry.get().strip()
    answer_entry.delete(0, tk.END)
    handle_answer(text)


def build_window():
    global window, start_screen, quiz_screen, fact_screen, result_screen
    global question_label, picture_label, option_buttons, score_label, fact_message, result_label
    global answer_entry, submit_button, mode_entry

    window = tk.Tk()
    window.title('Flag-Find Frenzy')
    window.geometry('1000x800')

    start_screen = tk.Frame(window)
    quiz_screen = tk.Frame(window)
    fact_screen = tk.Frame(window)
    result_screen = tk.Frame(window)

    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    for frame in (start_screen, quiz_screen, fact_screen, result_screen):
        frame.grid(row=0, column=0, sticky='nsew')

    title = tk.Label(start_screen, text='Flag-Find Frenzy', font=('Arial', 24))
    title.pack(pady=20)
    names = tk.Label(start_screen, text='Group: Hudson McEntire, Yuval Dinodia, Aarush Yelimeli')
    names.pack(pady=10)

    mode_label = tk.Label(start_screen, text='Type Mode (mix up, easy, standard, advanced, expert)')
    mode_label.pack()
    mode_entry = tk.Entry(start_screen, width=20)
    mode_entry.insert(0, current_mode)
    mode_entry.pack(pady=6)

    picture_label = tk.Label(quiz_screen)
    picture_label.pack(pady=12)
    question_label = tk.Label(quiz_screen, text='Question 0', font=('Arial', 16))
    question_label.pack(pady=10)

    button_frame = tk.Frame(quiz_screen)
    button_frame.pack(pady=15)
    option_buttons = [tk.Button(button_frame, text='', width=30) for _ in range(MAX_OPTIONS)]

    answer_entry = tk.Entry(quiz_screen, width=30)
    submit_button = tk.Button(quiz_screen, text='Submit', command=submit_typing)

    score_label = tk.Label(quiz_screen, text='Score: 0', font=('Arial', 14))
    score_label.pack(pady=8)

    fact_title = tk.Label(fact_screen, text='Fun Fact', font=('Arial', 18))
    fact_title.pack(pady=10)
    fact_message = tk.Label(fact_screen, text='', wraplength=500, justify='left')
    fact_message.pack(padx=20, pady=15)
    tk.Button(fact_screen, text='Next Question', command=go_back_to_quiz).pack(pady=8)

    result_label = tk.Label(result_screen, text='', font=('Arial', 18))
    result_label.pack(pady=15)
    tk.Button(result_screen, text='Play Again', command=go_home).pack(pady=8)

    def set_mode_and_start():
        global current_mode
        entry_text = mode_entry.get().strip().lower()
        if entry_text not in MODE_GROUPS:
            entry_text = 'mix up'
        current_mode = entry_text
        start_game()

    tk.Button(start_screen, text='Start', width=20, command=set_mode_and_start).pack(pady=12)
    tk.Button(start_screen, text='Quit', width=20, command=window.destroy).pack(pady=4)

    show_screen(start_screen)
    window.mainloop()


build_window()
