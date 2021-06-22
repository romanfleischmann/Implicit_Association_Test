# ESCAPE
from psychopy import core, event
event.globalKeys.add(key='q', modifiers=['ctrl'], func=core.quit)


#2 IMPORT

import random
from psychopy.core import Clock, wait
from psychopy.event import waitKeys, getKeys
from psychopy.visual import Window, TextStim


# SET AND ASSIGN

my_win = Window( [800, 400], units = 'pix' )

instruction1 = "this is training 1 \npress 'f' for negative and 'j' for positive. \npress with any key to start"
instruction2 = "this is training 2 \npress 'f' for gay and 'j' for straight. \npress any key to start"
instruction3 = "this is the main block 1 \npress 'f' for negative and gay. \npress 'j' for positive and straight \npress any key to start"
instruction4 = "this is training 3 \npress 'f' for negative and 'j' for positive. \npress with any key to start"
instruction5 = "this is training 4 \npress 'f' for straight and 'j' for gay. \npress any key to start"
instruction6 = "this is the main block 2 \npress 'f' for negative and straight. \npress 'j' for positive and gay \npress any key to start"

stim = None

list_pos = ["pos1", "pos2", "pos3", "pos4"]
list_neg = ["neg1","neg2", "neg3", "neg4"]
list_biasA = ["gay1", "gay2", "gay3", "gay4"]
list_biasB = ["str1", "str2", "str3", "str4"]

timer = Clock()

waittime_ins = 1
waittime_right_false = 0.5
repeats_per_block = 8
repeats_per_training = 5

times_condition_a = [] #negative left, positive right, gay left, straight right
times_condition_b = [] #negative left, positive right, straight left, gay right

times_training_a = []
times_training_b = []

counter_right = 0
counter_false = 0


#  DEF LEVEL 1

#this defines the pool from which the stimuli are randomly chosen
def set_pool(pool):
    global list_pool
    list_pool = pool

#this chooses random stim for each round from the defined pool
def set_stim():
    global stim 
    stim = random.choice(list_pool)

# this prompts the randomly chosen stimuli in each round, it also resets the clock
def prompt_stim ():
    text1 = TextStim( my_win, stim , height = 100 )
    text1.draw()
    my_win.flip()
    timer = Clock()

# prompts empty screen for t seconds
def prompt_empty(t):
    my_win.flip()
    wait(t)

# this prompts the instruction
def prompt_instr (instruction = instruction1):
    text1 = TextStim( my_win, instruction , height = 30 )
    text1.draw()
    my_win.flip()
    waitKeys()
    
#this prompts "false" and adds +1 to the false counter
def prompt_false ():
    text2 = TextStim( my_win, "false" , height = 80, color = "red" )
    text2.draw()
    my_win.flip()
    wait(waittime_right_false)
    global counter_false 
    counter_false = counter_false + 1

#this prompts "right" and adds +1 to the right counter
def prompt_right ():
    text2 = TextStim( my_win, "right" , height = 80 , color = "green")
    text2.draw()
    my_win.flip()
    wait(waittime_right_false)
    global counter_right
    counter_right = counter_right + 1

# DEF LEVEL 2

# this checks if a stimuli is in a defined bias-list or a defined neg_pos-list. it then calls add_right  or calls prompt_false. it also appends time to condition list
def check(neg_pos, bias, condition):
    if stim in neg_pos:
        print ('stim is a neg_pos')
        prompt_right()
    elif stim in bias:
        print('stim is a bias')
        condition.append(timer.getTime())
        prompt_right()
    else:
        prompt_false()

# DEF LEVEL 3

# this checks if key are pressed. j calls check with 'right' arguments, f calls check with 'left' arguments. Other keys call prompt_false
def keypress (left_neg_pos, right_neg_pos,left_bias, right_bias, condition_kp):
    pressed_key = waitKeys()
    if 'j' in pressed_key:
        print('right key pressed')
        check(right_neg_pos, right_bias, condition = condition_kp)
    elif 'f' in pressed_key:
        print('left key pressed')
        check (left_neg_pos, left_bias, condition = condition_kp)
    else: 
        prompt_false()
        print ('false key pressed')

# DEF LEVEL 4

# this is one combines alle of the above into one block. 
def block (instr, set_pool1, keypress1, keypress2, keypress3, keypress4, keypress5, repeat = 5):
    prompt_instr(instr)
    prompt_empty(waittime_ins)
    set_pool(set_pool1)
    count = 0
    while count < repeat:
        set_stim()
        prompt_stim()
        keypress(keypress1, keypress2, keypress3, keypress4, keypress5)
        count+= 1

# DEF LEVEL 5

# this one combines two trainings and one block into one condition. the conditions are seperate, so the order can be easily changed if necessary
def exec_condition_a ():
    #trainingsblock1 neg - pos, not written
    block(instruction1, (list_neg + list_pos), list_neg, list_pos, list_biasA, list_biasB, times_training_a, repeats_per_training)
    #trainingsblock2 biasA - biasB  written to times_training_a
    block(instruction2, (list_biasA + list_biasB), list_neg, list_pos, list_biasA, list_biasB, times_training_a, repeats_per_training)
    #block1 neg / biasA -  pos / biasB, written to times_condition_a
    block(instruction3, (list_neg + list_pos + list_biasA + list_biasB), list_neg, list_pos, list_biasA, list_biasB, times_condition_a, repeats_per_block)

def exec_condition_b ():
    #trainingsblock3 neg - pos, not written
    block(instruction4, (list_neg + list_pos), list_neg, list_pos, list_biasA, list_biasB, times_training_b, repeats_per_training)
    #trainingsblock4 biasB - biasA  written to times_training_b
    block(instruction5, (list_biasA + list_biasB), list_neg, list_pos, list_biasB, list_biasA, times_training_b, repeats_per_training)
    #block2 neg / biasA -  pos / biasB, written to times_condition_b
    block(instruction6, (list_neg + list_pos + list_biasA + list_biasB), list_neg, list_pos, list_biasB, list_biasA, times_condition_b, repeats_per_block)

def print_res():
    print("training a:", times_training_a)
    print("training b:", times_training_b)
    print("condition a:", times_condition_a)
    print("condition b:", times_condition_b)
    print("counter right", counter_right)
    print ("counter false", counter_false)
  
  
# Main


#exec_condition_a()
#exec_condition_b()
print_res()
