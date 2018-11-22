# BB&N English Course Selection Sorting Program

'''JUICE'S ALGORITHM
*** Run it with a LOT of different variations (every class in every block)
*** Create a SCORE for each by adding up the choices
*** Minimize the total SCORE
'''



###IAN's METHODS (you can tell cause they are super messy)
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
    MAX_CLASS_SIZE = 13
    MIN_CLASS_SIZE = 9

    # constants for class score calculations
    FIRST_IMPORTANCE = 40
    SECOND_IMPORTANCE = 30
    GENDER_IMPORTANCE = 20
    BLOCK_IMPORTANCE = -1000 # can't have a class with the wrong block
    LARGE_CLASS_IMPORTANCE = -100
    SMALL_CLASS_IMPORTANCE = 40
    NOT_SELECETD_CLASS_IMPORTANCE = -100
    NO_PREFERENCE_IMPORTANCE = 0
    
    def __init__(self, name, gender, first, second, third, blocks):
        self.name = name
        self.gender = gender
        self.first = first
        self.second = second
        self.third = third
        self.block = blocks

    def is_male(self):
        return (self.gender == 'Male' or self.gender == 'M')

    def is_female(self):
        return (self.gender == 'Female' or self.gender == 'F')

    def is_other_gender(self):
        return (not self.is_male() and not self.is_female())

    def calculate_class_score(self, klass, klass_name,rules_dict):
        score = 0
        
        #first check block, most inflexible condition
        if self.block != 'E' and (rules_dict[klass_name] != self.block): #if student has a specific english block (not both), AND that block isn't when this class is being held, can't have it
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


def classSorter_Methodized(rules,indata,sort_depth=12,BAD_VALUE=5,outfile_name=None):
    outfile=outfile_name # I USE BOTH AND I REGRET THIS
    #first, load the rules file
    rules_dict=rules_to_dict(rules)
    # get data from csv
    firstLine = True
    students = []
    reader=indata.split('\n')
    for student_row_s in reader:
        student_row=student_row_s.split(',') # no csv module needed!!! yay!
        if firstLine: # skip first line (labels)
            firstLine = False
            continue
#        print(student_row)
        students.append(Student(student_row[1], student_row[2], student_row[3].rstrip(' ').lower(), student_row[4].rstrip(' ').lower(), student_row[5].rstrip(' ').lower(), student_row[6])) # strip spaces and make class names lower cause because our entry person was very tired

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
    for i in range(sort_depth):
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
        outfile.write("SORTED BB&N ENGLISH COURSES (M/F/O)")
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
                outfile.write("\n" + student.name + " (" + student.gender + ") - " + str(student_choice))
    if outfile != None:
        outfile.write("\n\n")
        outfile.close()
    #print('THIS ITERATION\'S SCORE IS :'+str(score))
    return score
