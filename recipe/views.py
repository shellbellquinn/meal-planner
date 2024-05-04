from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Category, Recipe, Instructions, Ingredient
from .forms import RecipeForm, IngredientForm, InstructionForm

#view user recipes in view_my_recipes.html
@login_required
def view_my_recipes(request):
    recipes = Recipe.objects.filter(created_by=request.user)

    return render(request, 'recipe/view_my_recipes.html', {
    'title': 'My Recipes',
    'recipes': recipes,
})

#view recipes in view_recipe.html
@login_required 
def view_recipe(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories= Category.objects.all()
    recipes = Recipe.objects.all()

    if category_id:
        recipes = recipes.filter(category_id=category_id)
       
    if query:
        recipes = recipes.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'recipe/view_recipe.html', {
        'title': 'Recipes',
        'recipes': recipes,
        'categories': categories,
    })

#view recipe details
@login_required
def view_recipe_detail(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
    instructions = Instructions.objects.filter(recipe_id=recipe_primary_key)
    return render(request, 'recipe/view_recipe_details.html', {
        'title': 'Recipe Details',
        'recipe': recipe,
        'ingredients': ingredients,
        'instructions': instructions,
    })
    
#create a new recipe
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
        'submitmessage': 'Submit and Procceed to Next Step: Add Ingredients'
    })

#update recipe
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

#delete recipe
@login_required
def delete_recipe(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    recipe.delete()

    messages.success(request, 'Recipe deleted')
    return(redirect('core:home'))

#create ingredients associated with recipe
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
        'submitmessage': 'Submit and Procceed to Next Step: Add Instructions'
    })

#update ingredient
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

#delete ingredient
@login_required
def delete_ingredient(request, recipe_primary_key, ingredient_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_primary_key, recipe_id=recipe.id)
    ingredient.delete()

    messages.success(request, 'Ingredient deleted')
    return(redirect('core:home'))

#create instructions for recipe
@login_required
def create_instructions(request, recipe_primary_key):
    if request.method == 'POST':
        form = InstructionForm(request.POST)

        if form.is_valid():
            instructions = form.save(commit=False)
            instructions.recipe_id = recipe_primary_key
            instructions.save()
            
            messages.success(request, "Instructions Added")
        else:
            messages.error(request, "Failed to add instructions")
    else:
        form = InstructionForm()
    return render(request, 'recipe/forms.html', {
        'title': 'Add Instructions',
        'form': form,
        'submitmessage': 'Submit and Save Recipe'
    })

#edit instructions
@login_required
def update_instructions(request, recipe_primary_key, instructions_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    instructions = get_object_or_404(Instructions, pk=instructions_primary_key, recipe_id=recipe.id)

    if request.method == 'POST':
        form = InstructionForm(request.POST, instance=instructions)

        if form.is_valid():
            form.save()
            messages.success(request, "Instructions updated")
        else:
            messages.error(request, "Failed to update instructions")
    else:
        form = InstructionForm(instance=instructions)
    
    form = InstructionForm(instance=instructions)
    return render(request, 'recipe/forms.html', {
        'title': "Update Recipe Instructions",
        'form': form,
    })
    


#delete instructions
@login_required
def delete_instructions(request, recipe_primary_key, instructions_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    instructions = get_object_or_404(Instructions, pk=instructions_primary_key, recipe_id=recipe.id)
    instructions.delete()

    messages.success(request, 'Instructions deleted')
    return(redirect('core:home'))
    
