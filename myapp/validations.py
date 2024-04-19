
def render_template(request, template_name):
    if request.method == 'GET':
        return render(request, template_name)
    else:
        return HttpResponse("Método HTTP no permitido")