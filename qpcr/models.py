from django.db import models
import re, sys

root = '/qpcr/'

reaction_regex = re.compile(r'(?P<age>\d+)(?P<primer>\D+)(?P<number>\d+)(?P<sex>\D+)(?P<replicate>\d+)')
		
# Create your models here.
class Experimenter(models.Model):
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name
	
class SampleSet(models.Model):
	name = models.CharField(max_length=200)
	date = models.DateField()
	
	def __unicode__(self):
		return self.name

class Sample(models.Model):
	name = models.CharField(max_length=200)
	TREATMENT_CHOICES = (
		(u'PN', u'Postnatal'),
		(u'V', u'Vehicle'),
		(u'TP', u'Vehicle'),
	)
	treatment = models.CharField(max_length=8, choices=TREATMENT_CHOICES)
	age = models.IntegerField()
	number = models.IntegerField()
	SEX_CHOICES = (
		(u'M', u'Male'),
		(u'F', u'Female'),
		(u'O', u'Other'),
		(u'?', u'Unknown'),
	)
	sex = models.CharField(max_length=8, choices=SEX_CHOICES)
	sampleset = models.ForeignKey(SampleSet)
	
	def __unicode__(self):
		return self.name
		
class Run(models.Model):
	name = models.CharField(max_length=200)
	sample_set = models.CharField(max_length=200, blank=True)
	
	def get_average(self):
		return AverageRun(self)
	
	def get_absolute_url(self):
		return root + "runs/%d/" %(self.id)
	
	def __unicode__(self):
		return "%s" %(self.name)

class Reaction(models.Model):
	name = models.CharField(max_length=200)
	well = models.CharField(max_length=200)
	ct = models.CharField(max_length=200)
	run = models.ForeignKey(Run)
	
	def extractInfo(self):
		# WARNING: will return stale data if reaction is changed after it is first called
		try:
			return self.info
		except AttributeError:
			pass
		match = reaction_regex.match(self.name)
		if match is None:
			return None
		treatment = 'PN'
		age = match.group('age')
		sex = match.group('sex')
		number = match.group('number')
		replicate = match.group('replicate')
		self.info = info = (treatment, age, sex, number, replicate)
		return info
	
	def __unicode__(self):
		return "%s = %s" %(self.name, self.ct)
		
class ReactionPair:
	def __init__(self, reaction1, reaction2):
		self.reaction1 = r1 = reaction1
		self.reaction2 = r2 = reaction2
		self.reactions = [r1, r2]
		# FIXME: handle type conversion errors
		r1ct = float(r1.ct)
		r2ct = float(r2.ct)
		self.mean = (r1ct + r2ct) / 2.0
		self.dCt = r1ct - r2ct
		# FIXME: check for inconsistencies between reactions
		info1 = reaction1.extractInfo()
		self.treatment = info1[0]
		self.age = info1[1]
		self.sex = info1[2]
		self.number = info1[3]
		
class AverageRun:
	def __init__(self, run):
		rs = run.reaction_set.all()
		self.reaction_info = reaction_info = []
		self.replicateGroups = replicateGroups = {} # map of tuples (treatment, age, sex, number) to [reaction]
		self.others = [] # [reaction]
		for reaction in rs:
			info = reaction.extractInfo()
			reaction_info.append(info)
			if info is not None:
				so_far = replicateGroups.get(info[0:4])
				if so_far is None:
					replicateGroups[info[0:4]] = [reaction]
				else:
					so_far.append(reaction)
			else:
				self.others.append(reaction)
		self.groups = {} # map of tuples (treatment, age, sex) to [reactionPair]
		for info, group in replicateGroups.iteritems():
			if len(group) == 2:
				# Have 2 replicates
				pair = ReactionPair(group[0], group[1])
				so_far = self.groups.get(info[0:3])
				if so_far is None:
					self.groups[info[0:3]] = [pair]
				else:
					so_far.append(pair)
			else:
				for reaction in group:
					self.others.append(reaction)

	def groups_by_rows(self):
		result = []
		lists = []
		for g,l in self.groups.iteritems():
			result.append(''.join(g).upper())
			lists.append(l)
		yield result
		for i in range(0, max(len(g) for g in lists)):
			result = []
			for l in lists:
				result.append(l[i])
			yield result
