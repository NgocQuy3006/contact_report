{
    'name': 'Contact Excel Report',

    'version': '1.0',

    'depends': [
        'contacts',
        'report_xlsx',
        'web',
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/contact_report_view.xml',
        'views/contact_report_menu.xml',
    ],

    'assets': {

        'web.assets_backend': [

            'contact_excel_report/static/src/css/contact_report.css',

        ],
    },

    'installable': True,
}