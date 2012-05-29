from django.template import Context, loader
from django.http import HttpResponse

# Create your views here.

#def newRun(request):
#	return HttpResponse("Uploading a new run")
	
def newRun(request):
	t = loader.get_template('qpcr/new_run.html')
	c = Context({
	})
	
	return HttpResponse(t.render(c))
