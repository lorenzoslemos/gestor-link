from gestor.gestor.wsgi import app

def handler(request, context):
    return application(request.environ, lambda status, headers: None)
