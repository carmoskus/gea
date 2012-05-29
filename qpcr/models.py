from django.db import models

# Create your models here.
class Experimenter(models.Model):
	name=models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name
	
class Run(models.Model):
	name = models.CharField(max_length=200)
	
	def __unicode__(self):
		return "%s" %(self.name)
	
class Reaction(models.Model):
	name = models.CharField(max_length=200)
	ct = models.FloatField()
	run = models.ForeignKey(Run)
	
	def __unicode__(self):
		return "%s = %f" %(self.name, self.ct)
		
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
		

