from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Category, Recipe, Instructions, Ingredient
from .forms import RecipeForm, IngredientForm, InstructionForm

@login_required 
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            messages.success(request, 'Recipe created successfully')
        else:
            messages.error(request, 'Failed to create recipe, please check all fields and try again.')
    else:    
        form = RecipeForm()
    return render(request, 'recipe/forms.html', {
        'title': 'Create Recipe',
        'form': form,
    })

@login_required
def update_recipe(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            # Check if a new image has been uploaded and if it is different from the current image
            if 'image' in request.FILES:
                uploaded_image = request.FILES['image']
                if uploaded_image != recipe.image:  # Check if the uploaded image is different
                    recipe.image = uploaded_image
            form.save()  # Save the other fields
            messages.success(request, "Recipe updated successfully.")
        else:
            messages.error(request, "Failed to update recipe")
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipe/forms.html', {
        'title': 'Update Recipe',
        'form': form
    })

@login_required
def delete_recipe(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    recipe.delete()

    messages.success(request, 'Recipe deleted')
    return(redirect('core:home'))

@login_required
def create_ingredient(request, recipe_primary_key):
    if request.method == 'POST':
        form = IngredientForm(request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe_id = recipe_primary_key
            ingredient.save()
            
            messages.success(request, "Ingredient Added")
        else:
            messages.error(request, "Failed to add ingredient")
    else:
        form = IngredientForm()
    return render(request, 'recipe/forms.html', {
        'title': 'Add Ingredient',
        'form': form,
    })

@login_required
def update_ingredient(request, recipe_primary_key, ingredient_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_primary_key, recipe_id=recipe.id)

    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)

        if form.is_valid():
            form.save()
            messages.success(request, "Ingredient Updated")
        else:
            messages.error(request, "Failed to update ingredient")
    else:
        form = IngredientForm(instance=ingredient)
    
    form = IngredientForm(instance=ingredient)
    return render(request, 'recipe/forms.html', {
        'title': "Update Recipe Ingredient",
        'form': form,
    })
