#from django.template import Context, loader
#from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseServerError
from qpcr.models import Run, Reaction
from qpcr.forms import NewRunForm
import csv, cStringIO

# Create your views here.

#def newRun(request):
#	return HttpResponse("Uploading a new run")
	
# def newRun(request):
	# t = loader.get_template('qpcr/new_run.html')
	# c = Context({
	# })
	# return HttpResponse(t.render(c))

def run_ct_boxplot(request):
	return ''
	
def new_run(request):
	if request.method == 'POST':
		# Try to accept the file upload
		form = NewRunForm(request.POST, request.FILES)
		if form.is_valid():
			datafile = request.FILES['data']
			if datafile.size > 2*1024*1024:
				return HttpResponseServerError('Error: file too large')
			if not datafile.name.lower().endswith('.csv'):
				return HttpResponseServerError('Error: bad file name')
			name = datafile.name[:-4]
			io = cStringIO.StringIO(request.FILES['data'].read())
			reader = csv.DictReader(io)
			run = Run(name=name)
			run.save()
			for line in reader:
				reaction = Reaction(name=line['Well Name'], well=line['Well'], ct=line['Ct (dR)'], run=run)
				reaction.save()
			return redirect(run)
		else:
			#return HttpResponseServerError('Error: bad file')
			return render_to_response('qpcr/new_run.html', {
				'form': form
			}, context_instance=RequestContext(request))
	else:
		# Show the upload page
		form = NewRunForm()
		return render_to_response('qpcr/new_run.html', {
			'form': form
		}, context_instance=RequestContext(request))

