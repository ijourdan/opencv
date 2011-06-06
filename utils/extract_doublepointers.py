#! /usr/bin/env python
"""
This script checks the OpenCV headers to find methods that take double pointers
to OpenCV data structures as in/out parameters.

These methods need a special treatment and therefore SWIG typemaps are generated.
"""

import sys

def convert_name(str):
    count = 0
    if (str[0:2] == "_p"):
        p,s = convert_name(str[2:])
        return(('*' + p),s)
    return ('',str[1:])


if (sys.argv.__len__() < 1):
    sys.exit(1)

infile = open(sys.argv[1],'r')

lines = infile.readlines()

infile.close()

foundit = 0
mytypes = []

for line in lines:
    if (foundit == 0):
        if (line.find('TYPES TABLE (BEGIN') > -1):
            foundit = 1
    else:
        if (line.find('TYPES TABLE (END)') > -1):
            foundit = 0
        else:
            stuff = line.split()
            if (stuff.__len__() >= 3):
                if (stuff[0] == "#define"):
                    mytypes.append(stuff[1][8:])

for mytype in mytypes:
    p,s = convert_name(mytype)
    if (p.__len__() >= 2):
        print '%typemap(in)',s,p,'{ $*1_ltype buffer; if ((SWIG_ConvertPtr($input, (void **) &buffer, $*1_descriptor, 1)) == -1) return 0; $1=&buffer; };'
        #rez = "" + s + " " + p + 'getPtrTo' + s + '( ' +  s +  ' ' + p[1:] + 'input)'
        #sys.stdout.write(rez)
        #sys.stdout.write('\n{\n\t' + s + ' ' + p + 'rez = new ' + s + p[1:] + '();')
        #sys.stdout.write('\n\t*rez =input;\n\treturn(rez);\n}\n')
        #sys.stdout.write(rez)
        #sys.stdout.write(';\n')


#    else:
#        print '/* No conversions needed for type ', s, ' */'


