import sys
f = open(sys.argv[1], 'r')
rows = f.readlines()
f.close()

i=0

for i,row in enumerate(rows):
    if row.find('#')==0:
        cnt=1
        while row.find('#',cnt)==cnt:
            cnt+=1
        if row[-1]=="\n":
            rows[i]="<h%d>"%cnt+row[cnt:-1]+"</h%d>\n"%cnt
        else:
            rows[i]="<h%d>"%cnt+row[cnt:]+"</h%d>"%cnt

f = open('test.html', 'w')

f.write('<html>\n<body>\n')
for row in rows:
    f.write(row)
f.write('</body>\n</html>')

f.close()