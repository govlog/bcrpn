
#!/usr/bin/python

from decimal import Decimal,getcontext
import sys

getcontext().prec=1000

def __auto_scale(a,b):

    num_list=(str(a),str(b))
    float_prec=0
    int_prec=0

    for i in num_list:
        len_float=0
        len_int=0
        if '.' in i.rstrip('0').rstrip('.').lstrip('0'):
            (entier, flottant) = i.lstrip('0').split('.')
            len_float=len(flottant.rstrip('0'))
            if not entier.isdigit():
                len_float-=1

        elif i.lstrip('0').isdigit():
            len_int=len(i)
        else:
            len_int=0

        if len_float > float_prec:
            float_prec=len_float

        if len_int > int_prec:
            int_prec=len_int

    final_prec=str(float_prec+int_prec)

    return '.'+final_prec+'f'

a='98429842984298298429482984298424294829842980000000000000000000000000000000000042.6468471841'
b='100000000000000000000000000000000000000000000000000066600000000000013.111155454'

print format(Decimal(Decimal(a)*Decimal(b)),__auto_scale(a,b) ).rstrip('0').rstrip('.')
print Decimal(Decimal(a)*Decimal(b))

