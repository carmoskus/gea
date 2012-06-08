import numpy.numarray as na
from qpcr.models import Run, AverageRun
import pylab
import scipy.stats as stats

def make_boxplot(averageRun):
	group_names = []
	group_values = []
	num_groups = 0
	for info, reactionPairs in sorted(averageRun.groups.iteritems(), cmp=lambda x,y:cmp(x[0], y[0])):
		group_names.append(''.join(info).upper())
		datalist = reduce(lambda x, y: x+y, [[float(rp.reaction1.ct), float(rp.reaction2.ct)] for rp in reactionPairs])
		print datalist
		group_values.append(na.array(datalist))
		num_groups += 1
		
	xlocations = na.array(range(num_groups))+0.5
	pylab.boxplot(group_values, positions=xlocations)
	pylab.xticks(xlocations, group_names)
	
def tb():
	run = Run.objects.get(pk=2)
	avRun = run.get_average()
	make_boxplot(avRun)
	pylab.show()

def make_bar_graph(averageRun):
	group_names = []
	group_means = []
	group_errors = []
	num_groups = 0
	for info, reactionPairs in averageRun.groups.iteritems():
		group_names.append(''.join(info).upper())
		data = na.array([r.mean for r in reactionPairs])
		group_means.append(stats.tmean(data))
		group_errors.append(stats.tsem(data))
		num_groups += 1
	xlocations = na.array(range(num_groups))+0.5
	
	width = 0.5
	pylab.bar(xlocations, group_means, width=width, yerr=group_errors)
	pylab.yticks(range(0,30,4))
	pylab.xticks(xlocations + width/2, group_names)
	pylab.xlim(0, xlocations[-1]+width*2)
	#pylab.title("Bar Graph")
	
	# Turn off ticks on top and right
	pylab.gca().get_xaxis().tick_bottom()
	#pylab.gca().get_yaxis().tick_left()
	
def test_bar_graph():
	run = Run.objects.get(pk=2)
	avRun = run.get_average()
	make_bar_graph(avRun)
	pylab.show()
	