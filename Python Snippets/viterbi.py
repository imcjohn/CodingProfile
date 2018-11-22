import numpy

from collections import defaultdict
from channel import ChannelEncoder, ChannelDecoder

class ConvolutionalEncoder(ChannelEncoder):

    def __init__(self, G):
        super(ChannelEncoder, self).__init__()
        self.G = G
        self.r, self.K = G.shape

    def encode(self, received_voltages):
        # TODO: Your code here
        out=[]
        r=[0] * (self.K - 1) + list(received_voltages)
        r= r + (self.K - len(r) % self.K) * [0]
        for i in range(0,len(received_voltages)):
            cur=r[i:i+self.K]
            bits=self.G.dot(numpy.flip(cur,axis=0))
            for b in bits % 2:
                out.append(b)
        return out

class ViterbiDecoder(ChannelDecoder):

    def __init__(self, G):
        super(ChannelDecoder, self).__init__()
        self.G = G
        self.r, self.K = G.shape
        self.n_states = 2**(self.K-1)      # number of states
        self.states = range(self.n_states) # the states themselves

        # States are kept as integers, not binary strings or arrays.
        # For instance, the state "10" would be kept as "2", "11" as
        # 3, etc.

        # self.predecessor_states[s] = (s1, s2), where s1 and s2 are
        # the two predecessor states for state s (i.e., the two states
        # that have edges into s in the trellis).
        self.predecessor_states = [((2*s+0) % self.n_states, (2*s+1) % self.n_states) for s in self.states]

        # self.expected_parity[s1][s2] = the parity when transitioning
        # from s1 to s2 ('None' if there is no transition from s1 to
        # s2).  This is set up as a dictionary in init, for
        # efficiency.  For inefficiency, you could call
        # calculate_expected_parity() each time.
        self.expected_parity = defaultdict(lambda:defaultdict(float))
        for (s1, s2) in [(s1, s2) for s1 in self.states for s2 in self.states]:
            self.expected_parity[s1][s2] = self.calculate_expected_parity(s1, s2) if s1 in self.predecessor_states[s2] else None

        # Your code will update these variables
        self.PM = None
        self.Predecessor = None

    def calculate_expected_parity(self, from_state, to_state):

        # x[n] comes from to_state
        # x[n-1] ... x[n-k-1] comes from from_state
        x = ((to_state >> (self.K-2)) << (self.K-1)) + from_state

        # Turn the state integer into an array of bits, so that we can
        # xor (essentially) with G

        z = ViterbiDecoder.int_to_bit_array(x, self.K)
        return self.G.dot(z) % 2

    # Converts integers to bit arrays.  Useful if you find it
    # difficult to operate with states that are named as integers
    # rather than bit sequences.  You will likely not need to call
    # this function at all.
    @staticmethod
    def int_to_bit_array(i, length):
        return numpy.array([int(q) for q in (length-len(bin(i)[2:]))*'0'+bin(i)[2:]])

    def viterbi_step(self, n, received_voltages):
        # TODO: Your code here
        for state in self.states:
            s1,s2=self.predecessor_states[state]
            #print('At tick',n,'trying recieved voltage',received_voltages,'relative to expected state',self.expected_parity[s1][state])
            b1=self.branch_metric(self.expected_parity[s1][state],received_voltages)
            #print('At tick',n,'trying recieved voltage',received_voltages,'relative to expected state',self.expected_parity[s2][state])
            b2=self.branch_metric(self.expected_parity[s2][state],received_voltages)
            PM1=b1+self.PM[s1,n-1]
            PM2=b2+self.PM[s2,n-1]
            if (PM1 < PM2):
                #print('Assigning Parity value PM1',PM1,'to state',state,'in column',n)
                self.PM[state,n]=PM1
                self.Predecessor[state,n]=s1
            else:
                #print('Assigning Parity value PM2',PM2,'to state',state,'in column',n)
                self.PM[state,n]=PM2
                self.Predecessor[state,n]=s2
    
    def HD(self,a,b):
        e=list(a)
        r=list(b)
        c=0
        for i in range(0,len(e)):
            if (r[i] != e[i]):
                c=c+1
        return c

    def branch_metric(self, expected, received, soft_decoding=False):
        # TODO: Your code here
        a=[]
        b=[]
        for i in range(0,len(expected)):
            if (expected[i] > 0.5):
                a.append(1)
            else:
                a.append(0)
            if (received[i] > 0.5):
                b.append(1)
            else:
                b.append(0)
        return self.HD(a,b) #there are many many more efficent ways to implement this function

    def most_likely_state(self, n):
        # TODO: Your code here
        best=1000000000
        bstate=None
        for state in self.states:
            if (self.PM[state][n] < best):
                best=self.PM[state][n]
                bstate=state
        return bstate

    def traceback(self,s,n):
        # TODO: Your code here
        c=n
        bits=[]
        state=s
        while (c != 0):
            prev=self.Predecessor[state,c]
            #print(self.int_to_bit_array(state,self.K-1))
            if (prev > state or (prev==state==0)): #this meant you either went up the trellis, or went from 0 to 0
                bits.append(0)
            else:
                bits.append(1) # any time you go down the tree or stay even on something other than 0, bit has to be a 1
            state=prev
            c=c-1
#        bits=bits[(self.K-1):]
        l=list(numpy.flip(bits,axis=0))
        return numpy.array(l)
        
    def decode(self, received_voltages):

        max_n = (len(received_voltages) // self.r) + 1

        # self.PM is the trellis itself; rows are states, columns are
        # time.  self.PM[s,n] is the metric for the most-likely path
        # through the trellis arriving at state s at time n.
        self.PM = numpy.zeros((self.n_states, max_n))

        # at time 0, the starting state is the most likely, the other
        # states are "infinitely" worse.
        self.PM[1:self.n_states,0] = 1000000

        # self.Predecessor[s,n] = predecessor state for s at time n.
        self.Predecessor = numpy.zeros((self.n_states,max_n), dtype=numpy.int)

        # Viterbi Algorithm:
        n = 0
        for i in range(0, len(received_voltages), self.r):
            n += 1
            # Fill in the next columns of PM, Predecessor based
            # on info in the next r incoming parity bits
            self.viterbi_step(n, received_voltages[i:i+self.r])

        # Find the most-likely ending state, and traceback to
        # reconstruct the message.
        s = self.most_likely_state(n)
        result = self.traceback(s,n)
        #print(self.PM[s,n])
        return result