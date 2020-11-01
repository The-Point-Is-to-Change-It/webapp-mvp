# [START gae_python38_app]
from flask import Flask, request, render_template
from models import db

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/control', methods=['GET'])
def control_view():
    return render_template('control.html')

@app.route('/data', methods=['POST'])
def data():
    """Test adding data to the firestore db"""
    name = request.form.get('name')
    doc_ref = db.collection(u'users').document(u'{}'.format(name))
    doc_ref.set({
        u'first': u'{}'.format(name.split(' ')[0]),
        u'last': u'{}'.format(name.split(' ')[1])
    })
    return 'Thanks!'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
