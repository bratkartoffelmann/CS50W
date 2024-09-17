from .models import Category

""" 
Custom functions to output sorted categories
"""
def custom_sort_key(category):
    # Check if the category type is "Others"
    if category.type == "Others":
        return (1, category.type)  # Place "Others" at the end
    return (0, category.type)      # Place other categories first

categories = Category.objects.all() # Retrieve
categories = sorted(categories, key=custom_sort_key) # Sorted


"""

"""