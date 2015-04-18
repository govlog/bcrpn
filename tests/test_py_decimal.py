#!/usr/bin/python

from decimal import Decimal,getcontext
import sys

def get_prec(a,b):

    num_list=(str(a),str(b))
    float_prec=0
    int_prec=0

    for i in num_list:
        len_float=0
        if '.' in i.rstrip('.'):
            (entier, flottant) = i.split('.')
            len_int=len(entier)
            len_float=len(flottant.rstrip('0'))
        else:
            len_int=len(i)

        if len_float > float_prec:
            float_prec=len_float

        if len_int > int_prec:
            int_prec=len_int

    return float_prec+int_prec+1

a="9932123123.3"
b="45494895879875985797597595778957595797859785975987597597598759759579759579"

(new_prec)=str(float(a)*float(b)).split('+')

print "python result =>",result
print "precision     =>",new_prec

precision=get_prec(a,b)
print "precision =>",precision
getcontext().prec=get_prec(a,b)

tmp_result=str(Decimal(a)*Decimal(b))

print "current result",tmp_result

if '+' in tmp_result:
    (tmp,nprec)=tmp_result.split('+')
    print "new precision needed :",nprec
    getcontext().prec=nprec
    new_result=str(Decimal(a)*Decimal(b))

print new_result