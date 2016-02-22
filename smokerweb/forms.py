from django import forms
from smokerapi.models import Recipe

Class RecipeForm(forms.ModelForm):

  class Meta:
    model = Recipe
    fields = ('title','targetInternalTemp','maxAmbientTemp')
