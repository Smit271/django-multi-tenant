from django.apps import apps

# Lazy loading of app models
def get_app_model(app_name, model_name):
    try:
        return apps.get_model(app_name, model_name)
    except LookupError:
        return None

# Example: Accessing the 'MyApp' model named 'MyModel'
MyModel = get_app_model('core', 'DbDetails')

# Using the model in settings
if MyModel:
    MY_SETTING = list(MyModel.objects.all().values()) # Example query
else:
    MY_SETTING = []

def get_database_dict():
    return MY_SETTING