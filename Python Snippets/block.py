import numpy, sys

from channel import ChannelEncoder, ChannelDecoder

'''
A linear block encoder is just one type of channel encoder; we'll look
at another in PS3.
'''
class BlockEncoder(ChannelEncoder):

    def __init__(self):
        super(BlockEncoder, self).__init__()

    '''
    Here, you should implement the linear encoder. The input, bits,
    will be a numpy array of integers (each integer is 0 or 1).
    '''
    def encode(self, A, bits):
        # TODO: Your code here
        (k,m)=A.shape
        #first generate matrix
        I=numpy.identity(k)
        G=numpy.insert(I,k,A.transpose(),axis=1) #might want to find a cleaner way to do this
        #then make the blocks of size k
        blocks=[]
        block=[]
        count=0
        for bit in bits:
            if (count == k):
                count=0
                blocks.append(numpy.array(block))
                block=[]
            block.append(bit)
            count=count+1
        blocks.append(numpy.array(block))
        out=[]
        for block in blocks:
            ll=list(block.dot(G) % 2)
            out = out + ll
        for i in range(0,len(out)):
            out[i]=int(out[i])
        return numpy.array(out)
class SyndromeDecoder(ChannelDecoder):

    def __init__(self):
        super(ChannelDecoder, self).__init__()

    '''
    Here you should implement the syndrome decoder.
    
    Please set up the syndrome table before you perform the decoding
    (feel free to set up a different function to do this).  This will
    result in a more organized design, and also a more efficient
    decoding procedure (because you won't be recalculating the
    syndrome table for each codeword).
    '''
    def gS(self,A):
        (k,m) = A.shape
        H=numpy.insert(A.transpose(),k,numpy.identity(m),axis=1)
        synd={}
        idd=numpy.identity(k+m)
        for i in range(0,len(idd)):
            synd[numpy.array_str(H.transpose()[i])] = idd[i]
        return synd,H,k,m
    def decode(self, A, bits):
        (synd,H,k,m) = self.gS(A)
        chunks=numpy.split(bits,len(bits)/(k+m))
        out=[]
        for chunk in chunks:
            syndrome = numpy.array_str(H.dot(chunk) % 2)
            if syndrome in synd:
                chunk = (synd[syndrome] + chunk) % 2
            out=out+list(chunk.astype(int))[:k]
        return numpy.array(out)