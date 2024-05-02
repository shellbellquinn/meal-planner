from django import forms
from . models import Recipe, Instructions, Ingredient

SELECT_AREA = 'form-select form-select-lg mb-3'
INPUT_CLASSES = 'form-control'
FOR_IMAGE = 'form-control-file'
TEXT_AREA = 'form-control'

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('category', 'name', 'description', 'image', 'cook_time', 'serving')
        widgets = {
            'category': forms.Select(attrs= {
                'class': SELECT_AREA
            }), 
            'name': forms.TextInput(attrs= {
                'class': INPUT_CLASSES,
                'placeholder': 'Enter recipe name'

            }),
            'image': forms.FileInput(attrs= {
                'class': FOR_IMAGE,
            }),              
            'description': forms.Textarea(attrs= {
                'class': TEXT_AREA,
                'placeholder':  "Enter description",
                'rows': '3',
            }),
            'serving': forms.TextInput(attrs= {
                'class': INPUT_CLASSES,
                'placeholder': 'Enter how many servings per recipe'
            }),        
            'cook_time': forms.TextInput(attrs= {
                'class': INPUT_CLASSES,
                'placeholder': 'Enter how long it takes to cook'
            }),            
        }

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instructions
        fields = ('step_number', 'instruction_text')
        widgets = {
            'step_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Enter step number',
                'type': 'number',
            }),
            'instruction_text': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Enter instructions',
            }),
        }
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'quantity', 'metric')
        widgets = {
            'name': forms.TextInput(attrs= {
                'class': INPUT_CLASSES,
                'placeholder': "Enter ingredient name",
            }),
            'quantity': forms.NumberInput(attrs= {
                'class': INPUT_CLASSES,
                'placeholder': "Enter an number"
            }),
            'metric': forms.Select(attrs={
                'class': SELECT_AREA,
            }),
        }
