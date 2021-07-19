#This code is written in a way to be as easy to alter as possible. 
#To shape the experiment differently it is enough to look (and change) the sections "SET AND ASSIGN", "LEVEL 5" and 'MAIN"

# ESCAPE

from psychopy import core, event
event.globalKeys.add(key='q', modifiers=['ctrl'], func=core.quit)


#2 IMPORT

import random
from psychopy.core import Clock, wait
from psychopy.event import waitKeys, getKeys
from psychopy.visual import Window, TextStim
from psychopy import gui



# SET AND ASSIGN

my_win = Window( [800, 400], units = 'pix' )
timer = Clock()

#instruction texts
instruction_welcome = "Welcome!\n\nIn the following you will be presented a series of words to reacto to by pressing 'left' (the f-key) or 'right' (the j-key). Each series will be preceded by an instruction page with information on which words to sort to which side. Please dont overthink it and press as fast as you can.\n \nPress any key to continue."
instruction1 = "Training A1 \n\nPress 'f' for negative words and 'j' for positive words. \n\nPress any key to start."
instruction2 = "Training A2 \n\nPress 'f' for gay words and 'j' for straight words. \n\nPress any key to start."
instruction3 = "Block A \n\nPress 'f' for negative or gay words. \npress 'j' for positive or straight words \n\nPress any key to start."
instruction4 = "Training B1 \n\nPress 'f' for negative words and 'j' for positive words. \n\nPress any key to start."
instruction5 = "Training B2 \n\nPress 'f' for straight words and 'j' for gay words. \n\nPress any key to start."
instruction6 = "Block B \npress 'f' for negative and straight. \npress 'j' for positive and gay \nPress any key to start."
instruction7 = "Thanks for participating \n\nPress any key to end the experiment."

#lists for stimuli
#can be as long as necessary, but should all be equally for all conditions to display stimuli from all lists the same amount on average
list_cue_pos = ["Love", "Trust", "Happiness", "Sun"] #positive cue words. 
list_cue_neg = ["Hate","Sadness", "Hurtful", "Poison"] #negative cue words
list_biasA = ["Fabulous", "Queer", "Pink", "Rainbow"] #bias words A (here stereotypically male homosexual)
list_biasB = ["Barbecue", "Bro", "Jesus", "Pick-Up Artist"] #bias words B (here stereotypically male heterosexual)

#parameters, set as needed
waittime_ins = 0.6 #time period for empty canvas after instruction page
waittime_correct_false = 0.4 #time period for the display of correct/false feedback
repeats_per_block = 4 
repeats_per_training = 3

#  DEF LEVEL 1

#this creates a gui box
def gui_box():
    global sbj_nr, handedness, exp_order
    myDlg = gui.Dlg(title="Roman Fleischmann IAT")
    myDlg.addText('Subject info')
    myDlg.addField('Subject Nr:', 1)
    myDlg.addField('Handedness:', choices=["righthanded", "lefthanded"])
    myDlg.addText('Experiment Info')
    myDlg.addField('Order:', choices=["Bias A - Bias B", "Bias B - Bias A"])

    ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:  # or if ok_data is not None
        print(ok_data)
    else:
        print('user cancelled')
    
    sbj_nr = int(myDlg.data[0])
    handedness = str(myDlg.data[1])
    exp_order = str(myDlg.data[2])

#this creates a file to write in
def startfile():
    global data_out
    data_out = open('IAT_Results.txt', 'w', encoding='utf-8')
    data_out.write( '\t'.join( [ "subject", "handedness", "key", "correct/false", "condition", "stim", "type", "time"] ) + "\n" )

#this sets the name for the condition and the pool the stimulus for this condition is chosen from
def set_pool_condition(pool, condition_name = 'lorem ipsum'):
    global list_pool, condition
    list_pool = pool
    condition = condition_name

#this chooses random stim for each round from the defined pool. It also checks which type the chosen stimulus is, that being the list the stimulus is from
def set_stim():
    global stim, stim_type
    stim = random.choice(list_pool)
    if stim in list_cue_pos:
        stim_type = 'cue_pos'
    elif stim in list_cue_neg:
        stim_type = 'cue_neg'
    elif stim in list_biasA:
        stim_type = 'biasA'
    elif stim in list_biasB:
        stim_type = 'biasB'

# this prompts the randomly chosen stimuli in each round, it also resets the clock
def prompt_stim ():
    text = TextStim( my_win, stim , height = 100 )
    text.draw()
    my_win.flip()
    global timer
    timer = Clock()

# prompts empty screen for t seconds
#this is the only short function left, but as it gets called 4 times and has a very self-explanatory name i found the code to be more readable with this function than without

def prompt_empty(t):
    my_win.flip()
    wait(t)

# this prompts the instruction
def prompt_instr (instruction = instruction1):
    text = TextStim( my_win, instruction , height = 30 )
    text.draw()
    my_win.flip()
    waitKeys()
    
#this prompts the feedback and writes everything to the file
def prompt_feedback (feedback1 = "false", feedback2 = 'false', col = "red"):
    text = TextStim( my_win, feedback1 , height = 80, color = col )
    text.draw()
    my_win.flip()
    wait(waittime_correct_false)
    global correct_false 
    correct_false = feedback2
    data_out.write( '\t'.join( [str(sbj_nr), str(handedness), str(pressed_key_lr), str(correct_false), str(condition), str(stim),  str(stim_type), str(trial_time)] ) + "\n" )

# DEF LEVEL 2 (functions that need to call functions from Level 1)

# this checks if a stimuli is in a defined bias-list or a defined cue-list. it then calls the correct feedback which includes writing everything to the file
def check(cue, bias):
    if stim in cue:
        print ('check: correct \n(stim is a cue)')
        prompt_feedback("correct", 'correct', "green")
    elif stim in bias:
        print('check: correct \n(stim is a bias)')
        prompt_feedback("correct", 'correct', "green")
    else:
        print('check: incorrect')
        prompt_feedback("false", 'false', "red")

# this starts the experiment by initializing the txt file and triggering the gui box
def start_experiment():
    gui_box()
    startfile()
    prompt_empty(waittime_ins)
    prompt_instr(instruction_welcome)
    
#this ends the experiment by closing the file and prompting a goodbye
def end_experiment():
    data_out.close()
    prompt_empty(waittime_ins)
    prompt_instr(instruction = instruction7)

# DEF LEVEL 3 (functions that need to call functioins from level 2 and lower)

# this checks if key are pressed. j calls check with 'right' arguments, f calls check with 'left' arguments. Other keys call a miss
def keypress (left_cue, right_cue,left_bias, right_bias):
    pressed_key = waitKeys()
    global trial_time, pressed_key_lr
    trial_time = timer.getTime()
    print('condition is:', condition)
    print('stimulus is:', stim)
    if 'j' in pressed_key:
        pressed_key_lr = 'right'
        print('right key pressed')
        check(right_cue, right_bias)
    elif 'f' in pressed_key:
        pressed_key_lr = 'left'
        print('left key pressed')
        check (left_cue, left_bias)
    else: 
        pressed_key_lr = 'other'
        prompt_feedback("miss", 'miss', "red")
        print ('other key pressed than "j" or "f" key pressed')
    print('trial time is', trial_time, '\n---------------')

# DEF LEVEL 4 (functoins that need to call functions from level 3 and lower)

# this is one combines alle of the above into one block. 
def block (instr, pool, left_cue, right_cue, left_bias, right_bias, repeat, condition_name = 'no name'):
    prompt_instr(instr)
    prompt_empty(waittime_ins)
    set_pool_condition(pool, condition_name)
    count = 0
    while count < repeat:
        set_stim()
        prompt_stim()
        keypress(left_cue, right_cue, left_bias, right_bias)
        count+= 1
    prompt_empty(waittime_ins)


# DEF LEVEL 5 (functions that need to call functions from level 4 and lower)

# the whole structure of this code is built to be as easy to adapt for other needs as possible. This pays off here in level 5 most visibly: 
#The "block" function allows for free manipulation of the experiments structure and easy adding of more or different blocks or conditions
#the structure of arguments of the block function is as follows:
# 1. argument: Which instructions to display
# 2. argument: pool from which the stimulus is chosen. This can be as many lists as necessary, in paranthesis combined with a +
# 3. argument: cue for the left side
# 4. argument: cue for the right side
# 5. argument: bias for the left side
#6. argument: bias for the right side
#7. argument: how often the block is repeated (can be set in the parameters seperately for training and main block)
# 8. argument: name for the condition to be written into the file

# this one combines two trainings and one block into one condition. 

def exec_condition_a ():
    #trainingsblock1: neg left <--> pos right
    block(instruction1, (list_cue_neg + list_cue_pos), list_cue_neg, list_cue_pos, list_biasA, list_biasB, repeats_per_training, condition_name = 'training1')
    #trainingsblock2: biasA left <--> biasB right
    block(instruction2, (list_biasA + list_biasB), list_cue_neg, list_cue_pos, list_biasA, list_biasB, repeats_per_training, condition_name = 'training2')
    #block1: neg / biasA left <-->   pos / biasB right
    block(instruction3, (list_cue_neg + list_cue_pos + list_biasA + list_biasB), list_cue_neg, list_cue_pos, list_biasA, list_biasB, repeats_per_block, condition_name = 'main1')

def exec_condition_b ():
    #trainingsblock3: neg left <--> pos right
    block(instruction4, (list_cue_neg + list_cue_pos), list_cue_neg, list_cue_pos, list_biasA, list_biasB, repeats_per_training, condition_name = 'training3')
    #trainingsblock4: biasB left <--> biasA right
    block(instruction5, (list_biasA + list_biasB), list_cue_neg, list_cue_pos, list_biasB, list_biasA, repeats_per_training, condition_name = 'training4')
    #block2: neg / biasA left <-->  pos / biasB right
    block(instruction6, (list_cue_neg + list_cue_pos + list_biasA + list_biasB), list_cue_neg, list_cue_pos, list_biasB, list_biasA, repeats_per_block, condition_name = 'main2')

  
  
# MAIN (EXECUTION)
#this allows the instructor to chose freely in which order the conditions will be executed
#functions  "start experiment" or "end experiment" are rather short, but make it very clear for anyone who wants to alter this code what is going on, without reading a lot of code.

start_experiment()

if exp_order == 'Bias A - Bias B':
    exec_condition_a()
    exec_condition_b()
else:
   exec_condition_b()
   exec_condition_a()
   
end_experiment()    


