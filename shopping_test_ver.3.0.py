from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        new_recipe_button = Button(text='New Recipe')
        new_recipe_button.bind(on_press=self.go_to_new_recipe)
        recipe_book_button = Button(text='Recipe Book')
        recipe_book_button.bind(on_press=self.go_to_recipe_book)
        food_menu_button = Button(text='Food Menu')
        food_menu_button.bind(on_press=self.go_to_food_menu)
        shopping_cart_button = Button(text='Shopping Cart')
        shopping_cart_button.bind(on_press=self.go_to_shopping_cart)
        layout.add_widget(new_recipe_button)
        layout.add_widget(recipe_book_button)
        layout.add_widget(food_menu_button)
        layout.add_widget(shopping_cart_button)
        self.add_widget(layout)

    def go_to_new_recipe(self, instance):
        self.manager.current = 'new_recipe'

    def go_to_recipe_book(self, instance):
        self.manager.current = 'recipe_book'

    def go_to_food_menu(self, instance):
        self.manager.current = 'food_menu'

    def go_to_shopping_cart(self, instance):
        self.manager.current = 'shopping_cart'

class NewRecipeScreen(Screen):
    def __init__(self, **kwargs):
        super(NewRecipeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        self.recipe_name_input = TextInput(hint_text='Recipe Name')
        self.recipe_description_input = TextInput(hint_text='Recipe Description', multiline=True)
        
        ingredient_layout = BoxLayout(size_hint_y=None, height=40)
        self.ingredient_input = TextInput(hint_text='Add Ingredient')
        save_ingredient_button = Button(text='Add', size_hint_x=None, width=80)
        save_ingredient_button.bind(on_press=self.add_ingredient)
        ingredient_layout.add_widget(self.ingredient_input)
        ingredient_layout.add_widget(save_ingredient_button)
        
        self.ingredients_list = GridLayout(cols=1, size_hint_y=None)
        self.ingredients_list.bind(minimum_height=self.ingredients_list.setter('height'))
        ingredients_scroll = ScrollView(size_hint=(1, None), size=(400, 200))
        ingredients_scroll.add_widget(self.ingredients_list)
        
        save_button = Button(text='Save Recipe')
        save_button.bind(on_press=self.save_recipe)
        main_menu_button = Button(text='Main Menu')
        main_menu_button.bind(on_press=self.go_to_main_menu)
        
        layout.add_widget(self.recipe_name_input)
        layout.add_widget(self.recipe_description_input)
        layout.add_widget(ingredient_layout)
        layout.add_widget(ingredients_scroll)
        layout.add_widget(save_button)
        layout.add_widget(main_menu_button)
        self.add_widget(layout)

        self.ingredients = []

    def add_ingredient(self, instance):
        ingredient = self.ingredient_input.text.strip()
        if ingredient:
            self.ingredients.append(ingredient)
            ingredient_label = BoxLayout(size_hint_y=None, height=40)
            ingredient_text = Label(text=ingredient)
            remove_button = Button(text='Remove', size_hint_x=None, width=80)
            remove_button.bind(on_press=lambda x: self.remove_ingredient(ingredient_label, ingredient))
            ingredient_label.add_widget(ingredient_text)
            ingredient_label.add_widget(remove_button)
            self.ingredients_list.add_widget(ingredient_label)
            self.ingredient_input.text = ''

    def remove_ingredient(self, ingredient_layout, ingredient):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
            self.ingredients_list.remove_widget(ingredient_layout)

    def save_recipe(self, instance):
        recipe_name = self.recipe_name_input.text
        recipe_description = self.recipe_description_input.text
        if recipe_name and recipe_description:
            recipe = {
                'name': recipe_name,
                'description': recipe_description,
                'ingredients': self.ingredients.copy()
            }
            self.manager.recipe_book.append(recipe)
            self.recipe_name_input.text = ''
            self.recipe_description_input.text = ''
            self.ingredients.clear()
            self.ingredients_list.clear_widgets()
            self.manager.current = 'recipe_book'

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

class RecipeBookScreen(Screen):
    def __init__(self, **kwargs):
        super(RecipeBookScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')

        self.recipe_list = GridLayout(cols=1, size_hint_y=None)
        self.recipe_list.bind(minimum_height=self.recipe_list.setter('height'))
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(self.recipe_list)
        self.main_layout.add_widget(scroll_view)

        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        bottom_layout.add_widget(Label())
        self.main_menu_button = Button(text='Main Menu', size_hint=(None, None), size=(120, 50))
        self.main_menu_button.bind(on_press=self.go_to_main_menu)
        bottom_layout.add_widget(self.main_menu_button)
        self.main_layout.add_widget(bottom_layout)

        self.add_widget(self.main_layout)

    def on_enter(self):
        self.recipe_list.clear_widgets()
        for recipe in self.manager.recipe_book:
            recipe_name = recipe['name']
            btn = Button(text=recipe_name, size_hint_y=None, height=40)
            btn.bind(on_press=lambda instance, r=recipe: self.show_recipe_description(r))
            self.recipe_list.add_widget(btn)

    def show_recipe_description(self, recipe):
        self.current_recipe = recipe
        self.clear_widgets()
        description_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        name_label = Label(text=f"Recipe: {recipe['name']}", font_size='20sp', halign='center', size_hint_y=None, height=50)
        description_layout.add_widget(name_label)

        description_label = Label(text=f"Description: {recipe['description']}", font_size='16sp', halign='center', size_hint_y=None, height=80)
        description_layout.add_widget(description_label)

        ingredients_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        ingredients_label = Label(text="Ingredients:", font_size='16sp', halign='left', size_hint_y=None, height=30)
        ingredients_layout.add_widget(ingredients_label)

        ingredients_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        ingredients_list.bind(minimum_height=ingredients_list.setter('height'))

        for ingredient in recipe['ingredients']:
            ingredient_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            ingredient_text = Label(text=ingredient, font_size='14sp', halign='left', size_hint_x=0.8)
            ingredient_layout.add_widget(ingredient_text)
            ingredients_list.add_widget(ingredient_layout)

        ingredients_scroll = ScrollView(size_hint=(1, None), size=(400, 200))
        ingredients_scroll.add_widget(ingredients_list)

        ingredients_layout.add_widget(ingredients_scroll)
        description_layout.add_widget(ingredients_layout)

        add_to_food_menu_button = Button(text='Add to Food Menu', size_hint_y=None, height=50)
        add_to_food_menu_button.bind(on_press=lambda x: self.add_to_food_menu(recipe))
        description_layout.add_widget(add_to_food_menu_button)

        back_button = Button(text='Back to Recipe Book', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_back_to_recipe_book)
        description_layout.add_widget(back_button)

        self.add_widget(description_layout)

    def add_to_food_menu(self, recipe):
        if recipe not in self.manager.food_menu:
            self.manager.food_menu.append(recipe)
            for ingredient in recipe['ingredients']:
                if ingredient not in self.manager.shopping_cart:
                    self.manager.shopping_cart.append(ingredient)
        self.manager.current = 'food_menu'

    def remove_ingredient(self, ingredient_layout, ingredient):
        if ingredient in self.current_recipe['ingredients']:
            self.current_recipe['ingredients'].remove(ingredient)
            self.manager.shopping_cart.remove(ingredient)
            self.show_recipe_description(self.current_recipe)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

    def go_back_to_recipe_book(self, instance):
        self.clear_widgets()
        self.add_widget(self.main_layout)
        self.on_enter()

class FoodMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(FoodMenuScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.recipe_list = GridLayout(cols=1, size_hint_y=None)
        self.recipe_list.bind(minimum_height=self.recipe_list.setter('height'))
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(self.recipe_list)
        self.main_layout.add_widget(scroll_view)

        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        self.main_menu_button = Button(text='Main Menu', size_hint=(None, None), size=(120, 50))
        self.main_menu_button.bind(on_press=self.go_to_main_menu)
        bottom_layout.add_widget(self.main_menu_button)
        self.main_layout.add_widget(bottom_layout)
        self.add_widget(self.main_layout)

    def on_enter(self):
        self.recipe_list.clear_widgets()
        for recipe in self.manager.food_menu:
            recipe_name = recipe['name']
            btn = Button(text=recipe_name, size_hint_y=None, height=40)
            btn.bind(on_press=lambda instance, r=recipe: self.show_recipe_info(r))
            self.recipe_list.add_widget(btn)

    def show_recipe_info(self, recipe):
        self.clear_widgets()
        info_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        name_label = Label(text=f"Recipe: {recipe['name']}", font_size='20sp', halign='center', size_hint_y=None, height=50)
        info_layout.add_widget(name_label)

        description_label = Label(text=f"Description: {recipe['description']}", font_size='16sp', halign='center', size_hint_y=None, height=80)
        info_layout.add_widget(description_label)

        ingredients_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        ingredients_label = Label(text="Ingredients:", font_size='16sp', halign='left', size_hint_y=None, height=30)
        ingredients_layout.add_widget(ingredients_label)

        ingredients_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        ingredients_list.bind(minimum_height=ingredients_list.setter('height'))

        for ingredient in recipe['ingredients']:
            ingredient_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            ingredient_text = Label(text=ingredient, font_size='14sp', halign='left', size_hint_x=0.8)
            ingredient_layout.add_widget(ingredient_text)
            ingredients_list.add_widget(ingredient_layout)

        ingredients_scroll = ScrollView(size_hint=(1, None), size=(400, 200))
        ingredients_scroll.add_widget(ingredients_list)
        ingredients_layout.add_widget(ingredients_scroll)

        add_to_cart_button = Button(text='Add to Shopping Cart', size_hint_y=None, height=50)
        add_to_cart_button.bind(on_press=lambda x: self.add_to_shopping_cart(recipe))
        info_layout.add_widget(ingredients_layout)
        info_layout.add_widget(add_to_cart_button)

        back_button = Button(text='Back to Food Menu', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_back_to_food_menu)
        info_layout.add_widget(back_button)

        self.add_widget(info_layout)

    def add_to_shopping_cart(self, recipe):
        for ingredient in recipe['ingredients']:
            if ingredient not in self.manager.shopping_cart:
                self.manager.shopping_cart.append(ingredient)
        self.manager.current = 'shopping_cart'

    def remove_from_food_menu(self, ingredient):
        for recipe in self.manager.food_menu:
            if ingredient in recipe['ingredients']:
                recipe['ingredients'].remove(ingredient)
                self.manager.shopping_cart.remove(ingredient)
        self.on_enter()

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

    def go_back_to_food_menu(self, instance):
        self.clear_widgets()
        self.add_widget(self.main_layout)
        self.on_enter()

class ShoppingCartScreen(Screen):
    def __init__(self, **kwargs):
        super(ShoppingCartScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.shopping_list = GridLayout(cols=1, size_hint_y=None)
        self.shopping_list.bind(minimum_height=self.shopping_list.setter('height'))
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(self.shopping_list)
        self.layout.add_widget(scroll_view)

        bottom_layout = BoxLayout(size_hint_y=None, height=50)
        self.main_menu_button = Button(text='Main Menu', size_hint=(None, None), size=(120, 50))
        self.main_menu_button.bind(on_press=self.go_to_main_menu)
        bottom_layout.add_widget(self.main_menu_button)
        self.layout.add_widget(bottom_layout)
        self.add_widget(self.layout)

    def on_enter(self):
        self.shopping_list.clear_widgets()
        for item in self.manager.shopping_cart:
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            item_text = Label(text=item, size_hint_x=0.8)
            remove_button = Button(text='Remove', size_hint_x=None, width=80)
            remove_button.bind(on_press=lambda x, item=item: self.remove_item(item))
            item_layout.add_widget(item_text)
            item_layout.add_widget(remove_button)
            self.shopping_list.add_widget(item_layout)

    def remove_item(self, item):
        if item in self.manager.shopping_cart:
            self.manager.shopping_cart.remove(item)
            self.on_enter()

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

class RecipeBookApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.shopping_cart = []  # Initialize shopping cart
        self.sm.food_menu = []  # Initialize food menu
        self.sm.recipe_book = []
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(NewRecipeScreen(name='new_recipe'))
        self.sm.add_widget(RecipeBookScreen(name='recipe_book'))
        self.sm.add_widget(FoodMenuScreen(name='food_menu'))
        self.sm.add_widget(ShoppingCartScreen(name='shopping_cart'))
        return self.sm

if __name__ == '__main__':
    RecipeBookApp().run()
