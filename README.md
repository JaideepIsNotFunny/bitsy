# bitsy

This project provides a Python library to access/modify a numpy array bit-wise, like a stream of bits which can be accessed in FIFO manner only.

## Getting Started


### Prerequisites

The prerequisites are :
* Python 3 (or more)
* Numpy

You can download python from [here](https://www.python.org/downloads/). And to install numpy run the following command in command prompt.
```
pip intall numpy
```

### Installing

To install the package on your machine use the following command.

```
pip install bitsy
```


## Examples

To use the library you need to import it. And then you can declare an empty bitstream object or instantiate it with a numpy array.
```
import numpy 
import bitsy 
```

The numpy array used must be of dtype = 'uint8'/ 'uint16'/ 'uint32'.
```
arr = numpy.array([255,5,31], dtype='uint8')
```

Declare the bit streams.
```
bs = bitsy.bitstream(arr) #bitstream initialized with arr
bs2 = bitsy.bitstream() #empty bitstream
```

Print the bit streams.
```
bs.show()
```

Output :
```
0b11111111
0b101
0b11111
```

Read from bitstream and write in other.
```
five_bits = bs.read(5)
print(bin(five_bits))
bs2.write(5,five_bits)
```

Output :
```
0b11111
```

Now the bit streams are : 
```
bs.show()
print(" ")
bs2.show()
```

Output:
```
0b111
0b101
0b11111

0b11111
```



## Authors

* **[Jaideep Sagar](https://github.com/JaideepSagar1997)**


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

