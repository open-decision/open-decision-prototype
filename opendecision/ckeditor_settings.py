CKEDITOR_BASEPATH = "static/ckeditor/ckeditor"
CKEDITOR_CONFIGS = {

    'default': {
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],



        'toolbar_NodeCreateToolbar': [
            {'name': 'document', 'items': ['Maximize','Undo', 'Redo']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'links', 'items': ['Link']},
            {'name': 'insert', 'items': ['HorizontalRule', 'Source']},
                        '/',

            {'name': 'styles', 'items': ['Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'opendecision', 'items': ['CreateToken', 'Abbr']},
        ],



        'toolbar': 'NodeCreateToolbar',
        'toolbarCanCollapse': True,
        'tabSpaces': 4,
        'tokenStart': '[[',
        'tokenEnd': ']]',
        'extraAllowedContent': 'abbr',
        'width': '100%',
        'extraPlugins': ','.join([
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            #'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'placeholder',
            'abbr',
            'token',
        ]),
    },

     'visualbuilder': {
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'height': 200,
        'width': 250,
    },
}
