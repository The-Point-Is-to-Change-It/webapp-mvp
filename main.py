# [START gae_python38_app]
from flask import Flask, request, render_template
from models import db

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Nice try Joe. No peaking!'

@app.route('/control', methods=['GET'])
def control_view():
    return render_template('control.html')

def to_dict(self):
    d = {}
    d['status'] = self.status
    return d

@app.route('/power', methods=['POST'])
def power():
    viewer = request.json['viewer']
    action = request.json['action']
    tv = db.collection(u'tv').document(u'tv')
    tv.set({
        u'status': action
    })
    tv = db.collection(u'tv')
    tv = tv.stream()
    for each in tv:
        print(each.to_dict()['status'])
    print(viewer, action)
    return 'success'

@app.route('/tv', methods=['POST'])
def tv():
    from datetime import datetime
    stamp = request.json['datetime']
    stamp = datetime.strptime(stamp, "%a, %d %b %Y %H:%M:%S %Z")
    print('stamp is ', stamp)
    now = datetime.now()
    print(stamp > now)
    tv = db.collection(u'tv')
    tv = tv.stream()
    tv_status = ''
    for each in tv:
        print(each.to_dict()['status'])
        tv_status = each.to_dict()['status']
    return str(tv_status)

@app.route('/data', methods=['POST', 'GET'])
def data():
    '''Test adding data to the firestore db'''
    name = request.form.get('name')
    if not name:
        name = request.json['name']
    doc_ref = db.collection(u'users').document(u'{}'.format(name))
    doc_ref.set({
        u'first': u'{}'.format(name.split(' ')[0]),
        u'last': u'{}'.format(name.split(' ')[1])
    })
    return 'Thanks!'

"""

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script>

            function sendAndRecieve(data=null, fill=null) {
                
                $.ajax({
                    type: 'POST',
                    url: '/data',

                    data: JSON.stringify(data) || JSON.stringify({'name':'jklads yajyyy'}),
                    contentType: 'application/json;charset=UTF-8',
                    success: function(data) {
                        $(fill).text(data);
                    },
                    error: function(data) {                        alert(data);
                        alert(data);
                    }
                });

            };
        </script>

"""



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
