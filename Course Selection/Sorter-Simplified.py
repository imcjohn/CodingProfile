# BB&N English Course Selection Sorting Program

'''JUICE'S ALGORITHM
*** Run it with a LOT of different variations (every class in every block)
*** Create a SCORE for each by adding up the choices
*** Minimize the total SCORE
'''

# kludgy way to work with 2 or 3
try:
    input=raw_input
except NameError:
    pass

###IAN's METHODS
def rules_to_dict(rules):
    #INPUT: Rules data in format class,block\n
    #OUTPUT: Dictionary of class:block
    rulesdict_out={}
    contnets=rules.split('\n')
    for rule in contnets:
        class_name,block=rule.split(',')
        class_name=class_name.rstrip(' ').lower()# make sure it's in the same format as the CSV
        rulesdict_out[class_name]=block.upper() # don't know what the block convention is upper, but let's go with it
    return rulesdict_out
###END OF IAN's METHODS 


class Student:
    # constants for class size range
    MAX_CLASS_SIZE = 15
    MIN_CLASS_SIZE = 9

    # constants for class score calculations
    FIRST_IMPORTANCE = 40
    SECOND_IMPORTANCE = 30 # importance for 3rd choice is 0
    GENDER_IMPORTANCE = 40
    BLOCK_IMPORTANCE = -1000000000 # can't have a class with the wrong block (not proud of this but it works)
    LARGE_CLASS_IMPORTANCE = -100
    SMALL_CLASS_IMPORTANCE = -100
    NOT_SELECETD_CLASS_IMPORTANCE = -100
    NO_PREFERENCE_IMPORTANCE = 0
    
    def __init__(self, name, gender, first, second, third, blocks):
        self.name = name
        self.gender = gender.strip()
        self.first = first
        self.second = second
        self.third = third
        self.block = blocks

    def is_male(self):
        return (self.gender.lower() == 'male' or self.gender.upper().strip() == 'M')

    def is_female(self):
        return (self.gender.lower() == 'female' or self.gender.upper().strip() == 'F')

    def is_other_gender(self):
        return (not self.is_male() and not self.is_female())

    def calculate_class_score(self, klass, klass_name,rules_dict):
        score = 0
        
        #first check block, most inflexible condition
        if (self.block[0].lower() != 'e') and (rules_dict[klass_name] != self.block): #if student has a specific english block (not both), AND that block isn't when this class is being held, can't have it
            return self.BLOCK_IMPORTANCE #INFLEXIBLE

        # prioritize class size
        if len(klass) > self.MAX_CLASS_SIZE: # deprioritize large class
            return self.LARGE_CLASS_IMPORTANCE
        if len(klass) < self.MIN_CLASS_SIZE: # prioritize small class
            score += self.SMALL_CLASS_IMPORTANCE
        score += 2 * (self.MAX_CLASS_SIZE - len(klass))**2 # prioritize smaller classes within range

        # prioritize first/second/third choice
        if klass_name == self.first: # prioritize first choice
            score += self.FIRST_IMPORTANCE
        elif klass_name == self.second: # prioritize second choice
            score += self.SECOND_IMPORTANCE
        elif self.first == "No Preference" or self.second == "No Preference" or self.third == "No Preference": # no prioritization for no preference
            score += self.NO_PREFERENCE_IMPORTANCE
        elif klass_name != self.third: # deprioritize non choice
            return self.NOT_SELECETD_CLASS_IMPORTANCE
        
        # prioritize gender balance
        males = len([1 for student in klass if student.is_male()]) # number of males
        females = len([1 for student in klass if student.is_female()]) # number of females
        if males > females:
            if self.is_male():
                score -= self.GENDER_IMPORTANCE # deprioritize males in male-heavy class
            else:
                score += self.GENDER_IMPORTANCE # prioritize females in male-heavy class
        elif females > males:
            if self.is_male():
                score += self.GENDER_IMPORTANCE # prioritize males in female-heavy class
            else:
                score -= self.GENDER_IMPORTANCE # deprioritize females in female-heavy class
    
        return score


def classSorter_Methodized(rules,indata,BAD_VALUE=5,outfile_name=None):
    outfile=outfile_name # I USE BOTH AND I REGRET THIS
    #first, load the rules file
    rules_dict=rules_to_dict(rules)
    # get data from csv
    firstLine = True
    students = []
    reader=indata.split('\n')
    for student_row_s in reader:
        student_row_s = student_row_s.strip(',')
        student_row=student_row_s.split(',') # no csv module needed!!! yay!
        student_row = [''] + student_row
        if firstLine: # skip first line (labels)
            firstLine = False
            continue
#        print(student_row)
        students.append(Student(student_row[1], student_row[2], student_row[3].rstrip(' ').lower(), student_row[4].rstrip(' ').lower(), student_row[5].rstrip(' ').lower(), student_row[6])) # strip spaces and make class names lower case because our entry person was very tired

    # count classes
    klass_names = []
    for student in students:
        klass_names.extend([student.first, student.second, student.third])
    for klass_name in klass_names:
        if klass_name == "No Preference":
            klass_names.remove(klass_name)

    klass_names_final = list(set(klass_names))

    # first sort
    klasses = []
    for class_name in klass_names_final:
        klasses.append([])
    for student in students:
        scores = []
        for i, klass in enumerate(klasses):
            scores.append(student.calculate_class_score(klass, klass_names_final[i],rules_dict)) # get scores for each student in each class

        klasses[scores.index(max(scores))].append(student) # choose class with highest score for student in class

    # resort (rearrange students and reevaluate scores)
    for i in range(100):
        for klass_out in klasses:
            temp_class = klass_out[:]
            for t,student in enumerate(temp_class):
                klass_out.pop(0)
                scores = []
                for i,klass in enumerate(klasses):
                    scores.append(student.calculate_class_score(klass, klass_names_final[i],rules_dict))            
                klasses[scores.index(max(scores))].append(student)

    # print classes in output file
    score = 0 # SCORE IS HOW MUCH THIS WORKED
    if outfile != None:
        outfile = open(outfile_name, "w") # clear previous text
        outfile.close()
        outfile = open(outfile_name, "a")
        outfile.write("SORTED BB&N ENGLISH COURSES (M/F/O)\n")
        outfile.write(str(rules_dict))
    for i, klass in enumerate(klasses):
        if outfile != None:
            outfile.write("\n\n\n{} ({}/{}/{})\n".format(klass_names_final[i], len([1 for student in klass if student.is_male()]), len([1 for student in klass if student.is_female()]), len([1 for student in klass if student.is_other_gender()])))
        for student in klasses[i]:
            student_choice = BAD_VALUE
            if student.first == klass_names_final[i] or student.first == "No Preference":
                student_choice = 1
            elif student.second == klass_names_final[i] or student.second == "No Preference":
                student_choice = 2
            elif student.third == klass_names_final[i] or student.third == "No Preference":
                student_choice = 3
            score = score + student_choice
            if outfile != None:
                outfile.write("\n" + student.name + " (" + student.gender + ") - " + str(student_choice) + " - (" + str(student.block) + ")")
    if outfile != None:
        outfile.write("\n\n")
        outfile.close()
    #print('THIS ITERATION\'S SCORE IS :'+str(score))
    return score


# -*- coding: utf-8 -*-
import sys
# Print iterations progress, mostly from https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = u'█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
from math import pow
CLASSDATA_OUT='out_Bestest_propersize.txt'
BESTEST_WAE=None
BESTEST_SCORE=10000 #all caps to remind myself how awful this solution is --- never forget (1/18/2018)
TOTAL_COUNT=0
TOTAL_ITERATIONS=0
def course_funnel(undone_list,done_string,list_size):
	global BESTEST_WAE
	global TOTAL_COUNT
	global TOTAL_ITERATIONS
	global BESTEST_SCORE
	if list_size != 0:
		latest=undone_list[0]
		undone_list=undone_list[1:]
		done_string=done_string+'\n'
		course_funnel(undone_list,done_string+latest+',A',list_size-1)
		course_funnel(undone_list,done_string+latest+',D',list_size-1)
	else:
		current_score=classSorter_Methodized(done_string[1:],csv_data)
		if current_score < BESTEST_SCORE:
			BESTEST_WAE=done_string[1:] # I'm in the dante's inferno class right now, and im pretty sure
			BESTEST_SCORE=current_score # theres a special circle in hell for people who use global variables in recursion
		TOTAL_COUNT=TOTAL_COUNT+1
		printProgressBar(TOTAL_COUNT, TOTAL_ITERATIONS, prefix = 'Progress:', suffix = 'Complete', bar_length = 40)

def ecfd(fNAME): #Eat Classes From Data (file)
    totL=[]
    opped=open(fNAME)
    dupmpe=opped.read()
    opped.close()
    splitted=dupmpe.split('\n')[1:]
    for line in splitted:
        uncsv=line.split(',')
        print(uncsv)
        uno=uncsv[3].strip().lower()
        dos=uncsv[4].strip().lower()
        tre=uncsv[5].strip().lower()
        if (uno not in totL):
            totL=totL+[uno]
        if (dos not in totL):
            totL=totL+[dos]
        if (tre not in totL):
            totL=totL+[tre]
            totS=''
    for piece in totL:
        totS=totS+piece+'\n'
        print(totL)
    return totS[:-1]
csv_path=input('Please type the CSV Filename, and press enter: ')
if ('.csv' not in csv_path):
	csv_path=csv_path+'.csv'
rules=ecfd(csv_path)
l=rules.split('\n')
totalClasses=len(l)
totalIterations=pow(2,totalClasses) # for progress bar
TOTAL_ITERATIONS=totalIterations # another solution I am not proud of
classes=[]
for rule in l:
	classname=rule.split(',')[0]
	classes=classes+[classname]
csv_handle=open(csv_path)
csv_data=csv_handle.read()
csv_handle.close() #memory efficency!
printProgressBar(0, totalIterations, prefix = 'Progress:', suffix = 'Complete', bar_length = 40)
course_funnel(classes,'',len(classes))
print('Sort is complete! Output is in the text file '+CLASSDATA_OUT + ' on your desktop')
str(classSorter_Methodized(BESTEST_WAE,csv_data,5,CLASSDATA_OUT))
