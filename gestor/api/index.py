from gestor.gestor.wsgi import application

def handler(request, context):
    return application(request.environ, lambda status, headers: None)
