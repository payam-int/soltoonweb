from django.forms.widgets import ChoiceWidget, Select
from django.templatetags.static import static


class ChooseUniformWidget(Select):
    template_name = 'website/widgets/uniform_select.html'

    def __init__(self, attrs=None, choices=(), postfix='a'):
        super().__init__(attrs, choices)
        self.postifx = postfix

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'chooseUniform'

        for item in context['widget']['optgroups']:
            item[1][0]['attrs']['data-img-src'] = static('website/img/uniform{0!s}-{1}.svg'.format(item[1][0]['value'] + 1, self.postifx))
        return context
