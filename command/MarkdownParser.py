import sys,re
def Heading(row,l):
    if l>0 and row[0]=='#':
        cnt=1
        while row[cnt]=='#':
            cnt+=1
        if row[cnt]==" ":
            row="<h%d>"%cnt+row[cnt+1:-4]+"</h%d>"%cnt
    return row

def List(row):
    spaces=List.spaces
    ans=re.match(r'^ *',row)
    scnt=ans.span()[1]
    uls=""
    while spaces!=[] and spaces[-1][0]>scnt:
        uls+=spaces.pop()[1]
    if spaces==[] or spaces[-1][0]==scnt:
        if row[scnt:scnt+2]=="- ":
            row="<li>"+row[scnt+2:-4]
            if spaces==[]:
                row="<ul>"+row
                spaces.append([scnt,"</ul>"])
                List.cnt=0
            row+="</li>"
        elif re.match(r'[1-9]+\. ',row[scnt:])!=None:
            row="<li>"+row[scnt+2:-4]
            if spaces==[]:
                row="<ol>"+row
                spaces.append([scnt,"</ol>"])
                List.cnt=0
            row+="</li>"
        elif spaces!=[] and scnt!=len(row):
            row=spaces.pop()[1]+row
            List.cnt=0
        elif spaces!=[] and scnt==len(row):
            List.cnt+=1
            if List.cnt>=2:
                row+=spaces.pop()[1]
                List.cnt=0
    elif spaces[-1][0]<scnt:
        if row[scnt:scnt+2]=="- ":
            row="<ul><li>"+row[scnt+2:-4]+"</li>"
            spaces.append([scnt,"</ul>"])
            List.cnt=0
        elif re.match(r'[1-9]+\. ',row[scnt:])!=None:
            row="<ol><li>"+row[scnt+2:-4]+"</li>"
            spaces.append([scnt,"</ol>"])
            List.cnt=0
        else:
            row=row[scnt:]
    List.spaces=spaces
    return uls+row
List.spaces=[]
List.cnt=0

def Link(row):
    ans=re.search(r"\[.+\]\(.+\)",row)
    if ans!=None:
        sl=ans.span()
        first=row[:sl[0]]
        second=row[sl[0]:sl[1]]
        last=row[sl[1]:]
        content=re.search(r"\[.+\]",second).span()
        link=re.search(r"\(.+\)",second).span()
        row=first+'<a href="%s">%s</a>'%(second[link[0]+1:link[1]-1],second[content[0]+1:content[1]-1])+last
    return row

def Img(row):
    ans=re.search(r"!\[.*\]\(.+\)",row)
    if ans!=None:
        sl=ans.span()
        first=row[:sl[0]]
        second=row[sl[0]:sl[1]]
        last=row[sl[1]:]
        content=re.search(r"\[.+\]",second).span()
        link=re.search(r"\(.+\)",second).span()
        row=first+'<img src="%s" alt="%s"/>'%(second[link[0]+1:link[1]-1],second[content[0]+1:content[1]-1])+last
    return row

fin_list=[]

def Size(row):
    global fin_list
    ans=re.search(r"<[0-9]+>",row)
    if ans!=None:
        sl=ans.span()
        first=row[:sl[0]]
        second='<font size="%s">'%row[sl[0]+1:sl[1]-1]
        last=row[sl[1]:]
        row=first+second+last
        fin_list.append("</font>")
    return row

def Color(row):
    global fin_list
    ans=re.search(r"<#[0-9a-fA-F]+>",row)
    if ans!=None:
        sl=ans.span()
        first=row[:sl[0]]
        second='<font color="%s">'%row[sl[0]+1:sl[1]-1]
        last=row[sl[1]:]
        row=first+second+last
        fin_list.append("</font>")
    colorTexts=["black","gray","silver","white","blue","navy","teal","green","lime","aqua","yellow","red","fuchsia","olive","purple","maroon"]
    for texts in colorTexts:
        ans=re.search("<%s>"%texts,row)
        if ans!=None:
            sl=ans.span()
            first=row[:sl[0]]
            second='<font color="%s">'%row[sl[0]+1:sl[1]-1]
            last=row[sl[1]:]
            row=first+second+last
            fin_list.append("</font>")
    return row

def Fin(row):
    global fin_list
    ans=re.search(r"</>",row)
    if ans!=None and fin_list!=[]:
        sl=ans.span()
        first=row[:sl[0]]
        second=fin_list.pop()
        last=row[sl[1]:]
        row=first+second+last
    return row

def main(rows):
    outs=[]
    for row in rows:
        l=len(row)
        row+="" if l==0 else "<br>"
        row=Heading(row,l)
    
        row=List(row)
        
        row=Color(row)
        row=Size(row)
        row=Fin(row)
    
        row=Img(row)
        row=Link(row)
    
        row=row.replace("  ","<br>")
        outs.append(row)

    while List.spaces!=[]:
        outs.append(List.spaces.pop()[1])
    for x in fin_list[::-1]:
        outs.append(x)
    return outs

if __name__=="__main__":
    if len(sys.argv)>=2:
        f = open(sys.argv[1], 'r')
        rows = f.readlines()
        f.close()
    else:
        rows=[s.rstrip("\r\n").rstrip("\n") for s in sys.stdin]

    for x in main(rows):
        print(x)
