from waitress import serve
from sicomec.wsgi import application

if __name__ == '__main__':
    print("Servidor SICOMEC iniciado...")
    serve(application, host='0.0.0.0', port=8000)
