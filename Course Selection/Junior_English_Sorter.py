import ClassSorterMethodized
from displayFunctions import printProgressBar
import easygui # don't do this for macs
CLASSDATA_OUT='classdata_out.txt'
TOTAL_COUNT=0
def update_prog():
	global TOTAL_COUNT
	TOTAL_COUNT+=1
	printProgressBar(TOTAL_COUNT, totalIterations, prefix = 'Progress:', suffix = 'Complete', bar_length = 40)
def course_funnel(undone_list,done_string,list_size,best_score,best_way=None):
	if list_size != 0:
		latest=undone_list[0]
		undone_list=undone_list[1:]
		done_string=done_string+'\n'
		w1 = course_funnel(undone_list,done_string+latest+',A',list_size-1,best_score,best_way)
		w2 = course_funnel(undone_list,done_string+latest+',D',list_size-1,best_score,best_way)
		return min([w1,w2,(best_way,best_score)],key=lambda x: x[1])
	else:
		current_score=ClassSorterMethodized.classSorter_Methodized(done_string[1:],csv_data)
		update_prog() #progress bar uses global variable, so separated from main method
		return (done_string[1:],current_score)
#Simple helper method to deterine 
def ecfd(data): #Eat Classes From Data (file)
	totL=[]
	splitted=data.split('\n')[1:]
	totL=[line.split(',')[3:6] for line in splitted]
	totC=[j for i in totL for j in i] #concat sublists
	totL=list(set(totC)) #remove duplicates
	return totL

csv_path=path=easygui.fileopenbox('Please Select the Junior English Data',filetypes=["*.csv"])
csv_handle=open(csv_path)
csv_data=csv_handle.read()
csv_handle.close() #memory efficency!
classes=ecfd(csv_data)
totalIterations=2**len(classes) #rough estimate of how long the binary tree will take
printProgressBar(0, totalIterations, prefix = 'Progress:', suffix = 'Complete', bar_length = 40)
(best_way,best_score)=course_funnel(classes,'',len(classes),float('inf'))
print('Output is in '+CLASSDATA_OUT)
str(ClassSorterMethodized.classSorter_Methodized(best_way,csv_data,5,outfile_name=CLASSDATA_OUT))
