from flask import Flask, request, render_template, abort, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio', methods=['GET'])
def serve_audio():
    song = request.args.get('song')
    if song + ".mp3" in os.listdir('songs'):

        path = 'songs/' + song + '.mp3'

        range_header = request.headers.get('Range', None)
        if range_header:
            from flask import make_response

            size = os.path.getsize(path)
            byte_range = range_header.replace('bytes=', '').split('-')

            start = int(byte_range[0])
            end = int(byte_range[1]) if byte_range[1] else size - 1
            length = end - start + 1

            with open(path, 'rb') as f:
                f.seek(start)
                data = f.read(length)

            response = make_response(data)
            response.headers.add('Content-Range', f'bytes {start}-{end}/{size}')
            response.headers.add('Accept-Ranges', 'bytes')
            response.headers.add('Content-Length', str(len(data)))
            response.headers.add('Content-Type', 'audio/mpeg')
            return response

        return send_from_directory('songs', song + ".mp3", mimetype="audio/mpeg")

    else:
        return abort(404, description="Song Not Found")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)