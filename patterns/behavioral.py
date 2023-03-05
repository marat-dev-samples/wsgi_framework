import json
from patterns.structural import redirect


class Subject:

    def __init__(self):
        self.observers = []

    def add_observers(self, obj_list):
        for observer in obj_list:
            self.observers.append(observer)


    def notify(self):
        for item in self.observers:
            item.update(self)

    
    def notify_contributors(self):
        # Handle content comment action
        for item in self.observers:
            item.update(self.contributors)


    def notify_author(self):
        # Set notification for author only
        for item in self.observers:
            item.update([self.author])
    

class Observer:

    def update(self, subject):
        """This method must be replaced with child class"""
        pass


class PrintNotifier(Observer):

    def update(self, users):
        for user in users:
            print(f'Notify-> {user.name}')


class SmsNotifier(Observer):

    def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    def update(self, subject):
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))


class TemplateView:
    template_name = 'template.html'
    redirect = None
    
    def get_context_data(self):
        """This method should be overwritten"""
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        
        # Possible error here
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        self.request = request
        return self.render_template_with_context()


class ApiListView(TemplateView):
    queryset = []

    def get_queryset(self, request):
        """This method should be overwritten"""
        return self.queryset

    def __call__(self, request):
        self.request = request
        return '200 OK', json.dumps(self.get_queryset())


class CreateView(TemplateView):
    """Create view enchanced with redirect feature"""
    template_name = ''
    redirect = None

    def create_obj(self, data):
        pass

    def __call__(self, request):
        self.request = request
        if request['type'] == 'POST':
            self.create_obj()
            context = self.get_context_data()
            if self.redirect:
                return redirect(self.redirect, **context)
            return self.render_template_with_context()
        else:
            return super().__call__(request)






