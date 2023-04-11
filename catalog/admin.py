from django.contrib import admin
from .models import Author,Genre,Book,BookInstance,Language

# Register your models here.


# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display=('title','author','display_genre')
    
#     def display_genre(self):
#         return ", ".join(genre.name for genre in self.genre.all()[:3])
#     display_genre.short_description='Genre'
class BooksInstanceInline(admin.TabularInline):
        model=BookInstance   

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# @admin.register(Author)
# class BookAdmin(admin.ModelAdmin):
#     """Administration object for Book models.
#     Defines:
#      - fields to be displayed in list view (list_display)
#      - adds inline addition of book instances in book view (inlines)
#     """
#     list_display = ('title', 'author', 'display_genre')
#     # inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter=('status','due_back')
    fieldsets = (
        (None, {
            "fields": ('book','imprint','id')            
        }),
            
            ('Availabitly',{'fields':('status','due_back')
        }),
    )


class BooksInstanceInline(admin.TabularInline):
    model=BookInstance
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author','display_genre')
    def display_genre(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all())

    display_genre.short_description = 'Genre'

    inlines=[BooksInstanceInline]
    
    