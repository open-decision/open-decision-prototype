CKEDITOR_BASEPATH = "static/ckeditor/ckeditor"
CKEDITOR_CONFIGS = {

    'default': {
        #'skin': 'bootstrapck',
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
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        'toolbarCanCollapse': True,
        'tabSpaces': 4,
        'tokenStart': '[[',
        'tokenEnd': ']]',
        'extraAllowedContent': 'abbr',
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
