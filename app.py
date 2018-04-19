from flask import Flask, render_template, url_for, request
from Dfs import Dfs
from bfs import Bfs

peta1 = {'K': set(['M']),
         'M': set(['T', 'S','K','N']),
         'N': set(['M']),
         'S': set(['M', 'T', 'R']),
         'T': set(['M', 'S', 'U']),
         'R': set(['S', 'U']),
         'U': set(['T', 'R']),}


app = Flask(__name__)

dfs = Dfs('M', 'U', peta1)
bfs = Bfs('M', 'U', peta1)

@app.route('/dfs')
def dfs_searching():
    hasil = dfs.proses_searching()
    return render_template('index.html',Hasil =hasil )


@app.route('/bfs')
def bfs_searching():
    hasil = bfs.proses_searching()
    return render_template('index.html', Hasil=hasil)


# Debug = True -> Agar auto relod server
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
