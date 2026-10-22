from pkg import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=1, port=8000)