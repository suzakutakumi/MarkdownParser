from types import MethodType
from flask import Flask,render_template,request
import sys
sys.path.append('../')
from command import MarkdownParser as MP
app = Flask(__name__)

@app.route('/')
def Index():
    return render_template("index.html")

@app.route('/test',methods=['GET','POST'])
def Test():
    data=request.get_data().decode()
    ans=MP.main(data.split('\n'))
    return '\n'.join(ans)

if __name__ == "__main__":
    app.run(debug=True)