{
    'name': "Policies",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['mail', 'base', 'hr'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/rules.xml',
        'data/activity.xml',
        # 'views/result_link.xml',

    ],
    'demo': [],
    'summary': "logic_policies",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}
