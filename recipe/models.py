from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        #Fixing plural name in admin site
        verbose_name_plural = 'Categories'
        #Ording the name alphabetically
        ordering= ('name' ,)

    def __str__(self):
        return self.name
    
PREDEFINED_CATEGORIES = [
    "Appetizers and Snacks",
    "Entrees",
    "Baked Goods",
    "Salads and Sides",
    "Soups and Stews",
    "Not Specified"
]

@receiver(post_migrate)
def check_categories(sender, **kwargs):
    #check if the category table is empty
    if Category.objects.count() == 0:
        #if it is, populate with predifined categories
        for category_name in PREDEFINED_CATEGORIES:
            Category.objects.create(name=category_name)


class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipe_images', default='recipebookopen.svg', blank=True, null=True)
    description = models.TextField()
    cook_time = models.CharField(max_length=255)
    serving = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Instructions(models.Model):
    recipe = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveBigIntegerField()
    instruction_text = models.TextField()

    class Meta:
        ordering = ['step_number']

class Ingredient(models.Model):
    recipe = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=255)
    quantity = models.FloatField()

    GRAMS = 'GRAMS'
    LITERS = 'LITERS'
    TEASPOONS = 'TEASPOONS'
    TABLESPOONS = 'TABLESPOONS'
    CUPS = 'CUPS'
    OUNCES = 'OUNCES'
    POUNDS = 'POUNDS'
    KILOGRAMS = 'KILOGRAMS'
    MILLITTERS = 'MILLITTERS'
    UNITS = 'UNITS'
    DEFAULT = ' '

    METRIC_CHOICES = [
        (GRAMS, 'GRAMS'),
        (LITERS, 'LITERS'),
        (TEASPOONS, 'TEASPOONS'),
        (TABLESPOONS, 'TABLESPOONS'),
        (CUPS, 'CUPS'),
        (OUNCES, 'OUNCES'),
        (POUNDS, 'POUNDS'),
        (KILOGRAMS, 'KILOGRAMS'),
        (MILLITTERS, 'MILLITTERS'),
        (UNITS, 'UNITS'),
        (DEFAULT, ' ')
    ]

    metric = models.CharField(max_length=50, choices=METRIC_CHOICES, default=DEFAULT)
    def __str__(self):
        return f"{self.name} {self.quantity} {self.get_metric_display()}"





