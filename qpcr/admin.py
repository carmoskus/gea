from qpcr.models import SampleSet, Sample
from django.contrib import admin

#class SampleInline(admin.StackedInline):
class SampleInline(admin.TabularInline):
	model = Sample
	extra = 8

class SampleSetAdmin(admin.ModelAdmin):
	inlines = [SampleInline]

admin.site.register(SampleSet, SampleSetAdmin)
admin.site.register(Sample)

