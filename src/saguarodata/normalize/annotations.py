"""Literal operational context, independent of biological status inference."""
import re

ANNOTATION_FIELDS=('tag_only','off_plot','not_measured','needs_review')
ANNOTATION_METHOD='exact_operational_phrases_v1'

def observation_annotations(note):
    token=re.sub(r'\s+',' ',str(note or '').strip().casefold()).replace('–','-').replace('—','-')
    tags={'tag only':('tag_only',),'off plot':('off_plot',),'not measured':('not_measured',),
          'off plot - not measured':('off_plot','not_measured'),'need check':('needs_review',)}.get(token,())
    return {field:field in tags for field in ANNOTATION_FIELDS}

def verification_status(value):
    token=re.sub(r'\s+',' ',str(value or '').strip().casefold())
    return {'yes':'yes','no':'no','not found':'not_found','':'not_recorded'}.get(token,'unrecognized')
