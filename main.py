from flask import Flask, render_template, make_response
import gsheet
import copy

app = Flask(__name__)


@app.route('/<email>')
def gmail(email):
    info = gsheet.getInfo(email)
    return render_template('vnl-signature.html', info=info)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)