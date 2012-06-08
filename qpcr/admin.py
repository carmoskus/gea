from qpcr.models import SampleSet, Sample, Experimenter, Reaction, Run
from django.contrib import admin

#class SampleInline(admin.StackedInline):
class SampleInline(admin.TabularInline):
	model = Sample
	extra = 8

class SampleSetAdmin(admin.ModelAdmin):
	inlines = [SampleInline]

admin.site.register(SampleSet, SampleSetAdmin)
admin.site.register(Sample)
admin.site.register(Experimenter)

class ReactionInline(admin.TabularInline):
	model = Reaction
	extra=8

class RunAdmin(admin.ModelAdmin):
	inlines = [ReactionInline]

#admin.site.register(Reaction)
admin.site.register(Run, RunAdmin)

