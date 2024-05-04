from django.urls import path
from . import views

app_name = 'recipe'
urlpatterns = [
    path('', views.view_recipe, name='view_recipes'),
    path('mine/', views.view_my_recipes, name='view_my_recipes'),
    path('detail/<int:recipe_primary_key>/', views.view_recipe_detail, name='view_recipe_detail'),
    path('create/', views.create_recipe, name="create_recipe"),
    path('update/<int:recipe_primary_key>/', views.update_recipe, name="update_recipe"),
    path('delete/<int:recipe_primary_key>/', views.delete_recipe, name="delete_recipe"),
    path('<int:recipe_primary_key>/ingredient/create/', views.create_ingredient, name="create_ingredient"),
    path('<int:recipe_primary_key>/ingredient/update/<int:ingredient_primary_key>/', views.update_ingredient, name="update_ingredient"),
    path('<int:recipe_primary_key>/ingredient/delete/<int:ingredient_primary_key>/', views.delete_ingredient, name="delete_ingredient"),
    path('<int:recipe_primary_key>/instructions/create/', views.create_instructions, name="create_instructions"),
    path('<int:recipe_primary_key>/instructions/update/<int:instructions_primary_key>/', views.update_instructions, name="update_ingredient"),
    path('<int:recipe_primary_key>/instructions/delete/<int:instructions_primary_key>/', views.delete_instructions, name="delete_ingredient"),
]
