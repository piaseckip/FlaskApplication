#!/usr/bin/env python3
from website import create_app

app = create_app()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0",port=5000)
    # app.run(host="0.0.0.0",debug=True)