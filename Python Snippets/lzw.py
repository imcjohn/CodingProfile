import argparse
import array
import sys
if (sys.version_info[0] != 3):
    print("You must use Python 3 -- Exiting")
    sys.exit()

from bitstring import BitString

class LZW():

    def __init__(self, word_size=16):
        self.word_size = word_size

    def encode(self, message):
        message=''.join(message)
        # TODO: Your code here
        outputs=[]
        ###gen dict
        codewords={}
        for i in range(0,255):
            codewords[chr(i)]=i
        
        #start the actual loop
        cur=None
        ltr=''
        tail=0
        head=0
        codek=256
        while (head <= len(message)+1):
            #print(codek)
            curV=message[tail:head+1] #both inclusive cause my brain thinks like that
            if (curV in codewords): #no need to create new thing
                #print('g' + curV)
                cur=codewords[curV]
                ltr=curV
                head=head+1
            else:
                #print('Sending output '+ltr)
                outputs.append(cur) #send previous codeword
                #print('Adding codeword <'+curV+'> to codewords ')
                codewords[curV]=codek
                codek=codek+1
                if (codek > 2 ** self.word_size):
                    #clear it up!
                    print('REFRESH at '+str(codewords))
                    codewords={}
                    for i in range(0,255):
                        codewords[chr(i)]=i
                    codek=256
                head=head                
                tail=head
        if (head == len(message)): # means there's just one character waiting to be sent
            #print('SENDING CHAR')
            outputs.append(codewords[message[tail]])
        else:
            outputs.append(cur)
        # You will need to change this return statement to return a meaningful BitString
        #print(outputs)
        #print(codewords)
        B=BitString()
        B.pack_numbers(outputs,self.word_size)
        return B

    def decode(self, bits):
        # TODO: Your code here

        # You will need to change this return statement to return a meaningful string
        outputs=b.unpack_all_numbers(self.word_size)
        codewords={}
        for i in range(0,255):
            codewords[i]=chr(i)
        outs=codewords[outputs[0]]
        prev=codewords[outputs[0]]
        #### TODO: INITIAL SETUP FOR THESE
        codek=256
        for output in outputs[1:]:
            #print(codek)
            if (output in codewords): #standard resolve process
                # add old codeword to codek with the new letter
                res=codewords[output]
                codewords[codek]=prev+res[0]
                #print('adding <'+prev+res[0]+'> to dictionary')
                codek=codek+1 #TODO: IMPLEMENT DROP AND STUFF
                if (codek > 2 ** self.word_size):
                    print('REFRESH at '+str(codewords))
                    codewords={}
                    codek=256
                    for i in range(0,255):
                        codewords[i]=chr(i)
                # add new codeword to output and prev
                outs=outs+res
                prev=res
            else: #OH BOY WE'VE GOT A SPECIAL CASE
                codewords[codek]=prev+prev[0]
                #print('SC adding <'+prev+prev[0]+'> to dictionary')
                codek=codek+1
                res=codewords[output]
                outs=outs+res
                prev=res
                if (codek > 2 ** self.word_size):
                    print('REFRESH at '+str(codewords))
                    codewords={}
                    codek=256
                    for i in range(0,255):
                        codewords[i]=chr(i)
                # add new codeword to output and pre
        return outs

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='filename to compress or decompress', required=True)
    parser.add_argument('-d', '--decompress', help='decompress file', action='store_true')
    args = parser.parse_args()

    lzw = LZW()

    if not args.decompress:
        # read in the file
        f = open(args.filename, 'rb')
        compressed = [chr(k) for k in array.array("B", f.read())]
        f.close()
        # encode and output
        x = lzw.encode(compressed)
        new_filename = args.filename + '.encoded'
        x.write_to_file(new_filename)
        print("Saved encoded file as %s" % new_filename)

    else:
        b = BitString()
        b.read_in_file(args.filename)
        x = lzw.decode(b)
        new_filename = args.filename + '.decoded'
        with open(new_filename, "w") as f:
            f.write(x)
        print("Saved decoded file as %s" % new_filename)
