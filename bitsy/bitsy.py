import math
import numpy as np
import re




class bitstream:
    def __init__(self,array = None):

        if(str(locals()['array']) == 'None'):
            self.array_unit_size = 8
            self.array_type = 'uint'
            self.valid = True
            self.read_index = 0
            self.r_bit_index = 0
            self.write_index = 0
            self.w_bit_index = 0
            
            self.array = np.zeros((8),dtype = 'uint8')
            self.capacity = 8*self.array_unit_size
            self.size = 0

        else:
            self.array_unit_size = int(re.search(r'\d+',str(array.dtype)).group())
            self.array_type = re.findall('[a-zA-Z]+',str(array.dtype))[0]
            if(not(math.floor(math.log(self.array_unit_size,2)) == math.log(self.array_unit_size,2)) or not(self.array_type == 'uint')):
                print('Error : Array must be of valid dtype (uint) ',self.array_type,' ',math.log(self.array_unit_size,2))
                self.valid = False
                return
            if(len(array.shape)>1):
                print(array.shape)
                print('Error : Array must be one dimensional')
                self.valid = False
                return
            
            self.valid = True
            self.read_index = 0
            self.r_bit_index = 0
            array_size = 2**math.ceil(math.log(len(array)+1,2))

            self.array = np.zeros((array_size),dtype = array.dtype)
            self.array[0:len(array)] = array

            self.capacity = array_size * self.array_unit_size
            self.write_index = len(array)
            self.w_bit_index = 0
            self.size = len(array)*self.array_unit_size

    """
    def size(self):
        ri = self.read_index
        wi = self.write_index
        if(self.read_index> self.write_index):
            wi = wi + len(self.array)
        count = (wi - ri -1)*self.array_unit_size
        count = count + self.w_bit_index + (self.array_unit_size - self.r_bit_index + 1)

        return count
    """

    def get_next(self, number_of_bits):
        if ((not self.valid) or self.is_empty()):
            print('Error : Either stream doesnt have enough bits or stream does not contain valid data')
            return
        if ((number_of_bits > self.size)):
            number_of_bits = self.size
        rbi = self.r_bit_index
        ri = self.read_index
        s = self.size

        if (self.r_bit_index + number_of_bits - 1 < self.array_unit_size):
            #print('before : ',self.read_index, ' ', self.r_bit_index)
            mask = int(2 ** number_of_bits) - 1
            mask = mask << (self.r_bit_index)

            ans = (mask & self.array[self.read_index]) >> self.r_bit_index
            self.r_bit_index = (self.r_bit_index + number_of_bits) % self.array_unit_size

            if (self.r_bit_index == 0):
                self.read_index = (self.read_index + 1) % len(self.array)


            #print('after : ',self.read_index,' ',self.r_bit_index)
            #print(bin(ans))
        else:
            num_bits_frm_cur = self.array_unit_size - self.r_bit_index
            num_bits_frm_nxt = number_of_bits - num_bits_frm_cur

            ans1 = self.read(num_bits_frm_cur)
            if (not (self.r_bit_index == 0)):
                self.read_index = (self.read_index + 1) % len(self.array)
            ans2 = self.read(num_bits_frm_nxt)
            # ans = (ans2<<math.ceil(math.log(ans1+1,2))) + ans1

            ans = (ans2 << (num_bits_frm_cur)) + ans1
            #print(ans2 << (num_bits_frm_cur) ,'+', ans1)

        self.r_bit_index = rbi
        self.read_index = ri
        self.size = s
        return ans

    def read(self,number_of_bits):
        s = self.size

        if((not self.valid )or self.is_empty()):
            print('Error : Either stream doesnt have enough bits or stream does not contain valid data')
            return
        if((number_of_bits > self.size)):
            number_of_bits = self.size

        if(self.r_bit_index + number_of_bits-1 < self.array_unit_size):
            
            mask = int(2**number_of_bits) - 1
            mask = mask<<(self.r_bit_index)

            ans = (mask & self.array[self.read_index])>>self.r_bit_index
            self.r_bit_index = (self.r_bit_index + number_of_bits)%self.array_unit_size
            
            if(self.r_bit_index == 0):
                self.read_index = (self.read_index +1)%len(self.array)
            
            self.size = self.size -  number_of_bits
            #print(self.read_index,' ',self.r_bit_index)
            #print(bin(ans))
        else:
            num_bits_frm_cur = self.array_unit_size - self.r_bit_index
            num_bits_frm_nxt = number_of_bits - num_bits_frm_cur
            
            ans1 = self.read(num_bits_frm_cur)
            if(not(self.r_bit_index == 0)):
                self.read_index = (self.read_index +1)%len(self.array)
            ans2 = self.read(num_bits_frm_nxt)
            #ans = (ans2<<math.ceil(math.log(ans1+1,2))) + ans1

            ans = (ans2<<(num_bits_frm_cur)) + ans1
            
            
        
        s2 = self.size
        #print(s-s2,'removed : ',ans)
        return ans

    def write(self,number_of_bits,val):
        s = self.array_unit_size
        w = self.w_bit_index
        wi = self.write_index
        r = self.r_bit_index
        ri = self.read_index
        rb = ri*s + r
        wb = wi *s + w
        
        if(self.size+number_of_bits > self.capacity):
            a = self.array
            self.array = np.zeros((2*len(a)),dtype= a.dtype)
            self.capacity = 2*len(a)*s
            if(rb<wb):
                self.array[0:(wi-ri+1)] = a[r:(wi+1)]
                self.read_index = 0
                self.write_index = wi-ri
            else:
                self.array[0:wi]=a[0:wi]
                self.array[-(len(a) - ri):] = a[ri:]
                self.read_index = len(self.array) -(len(a) - ri)

        if(number_of_bits + self.w_bit_index -1 < self.array_unit_size):
            x = self.array[self.write_index]

            val = val << self.w_bit_index

            mask = 2**number_of_bits - 1

            mask = mask<<(self.w_bit_index)


            self.array[self.write_index]= (val & mask) + (x &(~mask))

            self.w_bit_index = (self.w_bit_index + number_of_bits)%self.array_unit_size
            if(self.w_bit_index == 0):
                self.write_index = (self.write_index +1)%len(self.array)
            
            self.size = self.size +  number_of_bits
        else:
            num_bits_in_cur = self.array_unit_size - self.w_bit_index
            num_bits_in_nxt = number_of_bits - num_bits_in_cur
            
            self.write(num_bits_in_cur, val)
            if(not(self.w_bit_index == 0)):
                self.write_index = (self.write_index +1)%len(self.array)
            val = val>>(num_bits_in_cur)
            self.write(num_bits_in_nxt,val )

    def read_from_end(self, number_of_bits):
        s = self.size

        if ((not self.valid) or self.is_empty()):
            print('Error : Either stream doesnt have enough bits or stream does not contain valid data')
            return
        if ((number_of_bits > self.size)):
            number_of_bits = self.size

        if (self.r_bit_index + number_of_bits - 1 < self.array_unit_size):

            mask = int(2 ** number_of_bits) - 1
            mask = mask << (self.r_bit_index)

            ans = (mask & self.array[self.read_index]) >> self.r_bit_index
            self.r_bit_index = (self.r_bit_index + number_of_bits) % self.array_unit_size

            if (self.r_bit_index == 0):
                self.read_index = (self.read_index + 1) % len(self.array)

            self.size = self.size - number_of_bits
            # print(self.read_index,' ',self.r_bit_index)
            # print(bin(ans))
        else:
            num_bits_frm_cur = self.array_unit_size - self.r_bit_index
            num_bits_frm_nxt = number_of_bits - num_bits_frm_cur

            ans1 = self.read(num_bits_frm_cur)
            if (not (self.r_bit_index == 0)):
                self.read_index = (self.read_index + 1) % len(self.array)
            ans2 = self.read(num_bits_frm_nxt)
            # ans = (ans2<<math.ceil(math.log(ans1+1,2))) + ans1

            ans = (ans2 << (num_bits_frm_cur)) + ans1

        s2 = self.size
        # print(s-s2,'removed : ',ans)
        return ans

    def write_in_front(self, number_of_bits, val):
        s = self.array_unit_size
        w = self.w_bit_index
        wi = self.write_index
        r = self.r_bit_index
        ri = self.read_index
        rb = ri * s + r
        wb = wi * s + w

        if (self.size + number_of_bits > self.capacity):
            a = self.array
            self.array = np.zeros((2 * len(a)), dtype=a.dtype)
            self.capacity = 2 * len(a) * s
            if (rb < wb):
                self.array[0:(wi - ri + 1)] = a[r:(wi + 1)]
                self.read_index = 0
                self.write_index = wi - ri
            else:
                self.array[0:wi] = a[0:wi]
                self.array[-(len(a) - ri):] = a[ri:]
                self.read_index = len(self.array) - (len(a) - ri)

        if (number_of_bits + self.w_bit_index - 1 < self.array_unit_size):
            x = self.array[self.write_index]

            val = val << self.w_bit_index

            mask = 2 ** number_of_bits - 1

            mask = mask << (self.w_bit_index)

            self.array[self.write_index] = (val & mask) + (x & (~mask))

            self.w_bit_index = (self.w_bit_index + number_of_bits) % self.array_unit_size
            if (self.w_bit_index == 0):
                self.write_index = (self.write_index + 1) % len(self.array)

            self.size = self.size + number_of_bits
        else:
            num_bits_in_cur = self.array_unit_size - self.w_bit_index
            num_bits_in_nxt = number_of_bits - num_bits_in_cur

            self.write(num_bits_in_cur, val)
            if (not (self.w_bit_index == 0)):
                self.write_index = (self.write_index + 1) % len(self.array)
            val = val >> (num_bits_in_cur)
            self.write(num_bits_in_nxt, val)

    def show(self):
        
        i = self.read_index
        
        while(True):
            x = self.array[i]
            if(i == self.read_index):
                x =  x >> self.r_bit_index
                
            print(bin(x))
            
            i=(i+1)%len(self.array)
            if((i == self.write_index)):
                x = self.array[self.write_index]
                if(not(self.w_bit_index == 0)):
                    x = (int(2**(self.w_bit_index)) - 1) & x
                    print(bin(x))
                break
                    
        
                
    def get_array(self):
        i = 0
        size = math.ceil(self.size/self.array_unit_size)

        ans = np.zeros((size),dtype = (str(self.array_type)+str(self.array_unit_size)))


        ri = self.read_index = 0
        rbi = self.r_bit_index = 0
        wi = self.write_index = len(ans)
        wbi = self.w_bit_index 

        for i in range(size-1):
            #print('unit size',self.array_unit_size)
            ans[i] = self.read(self.array_unit_size)
            #print(ans[i])
        ans[size - 1] = self.read(self.size)
        
        #self.array[0:len(ans)] = ans
        self.read_index = ri
        self.r_bit_index = rbi
        self.write_index = wi
        self.w_bit_index = wbi
        self.size = size * self.array_unit_size

        return ans

    def is_empty(self):
        return (self.size == 0)


"""
a = np.array([1,2,4,5],dtype='uint8')
bs = bitstream(a);

bs.show()
print(bs.read(3))
print(bs.read(3))
print(bs.read(3))

print("now")
bs.show()

ar = bs.get_array()

print(ar)

print("now")
bs.show()
"""