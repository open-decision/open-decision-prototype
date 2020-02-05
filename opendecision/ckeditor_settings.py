CKEDITOR_BASEPATH = "static/ckeditor/ckeditor"
CKEDITOR_CONFIGS = {

    'default': {
        'skin': 'bootstrapck',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],



        'toolbar_NodeCreateToolbar': [

            {'name': 'document', 'items': ['Source', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo', 'Maximize']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'insert',
             'items': ['Table', 'HorizontalRule', 'Smiley', 'SpecialChar']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'view', 'items': [
                'Preview',
                'Maximize',
                ]},
                '/',
            {'name': 'opendecision', 'items': ['CreateToken', 'Abbr', 'CreatePlaceholder']},
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
