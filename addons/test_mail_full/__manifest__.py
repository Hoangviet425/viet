# -*- coding: utf-8 -*-

{
    'name': 'Mail Tests (Full)',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 9876,
    'summary': 'Mail Tests: performances and tests specific to mail with all sub-modules',
    'description': """This module contains tests related to various mail features
and mail-related sub modules. Those tests are present in a separate module as it
contains models used only to perform tests independently to functional aspects of
real applications. """,
    'depends': [
        'mail',
        'mail_bot',
        'portal',
        'rating',
        # 'snailmail',
        'mass_mailing',
        'mass_mailing_sms',  # adds portal
        'phone_validation',
        'sms',
        'test_mail',
        'test_mail_sms',
        'test_mass_mailing',
    ],
    'data': [
        'data/mail_message_subtype_data.xml',
        'security/ir.model.access.csv',
        'security/ir_rule_data.xml',
        'views/test_portal_template.xml',
    ],
    'assets': {
        'web.assets_unit_tests': [
            'test_mail_full/static/tests/**/*',
            ('remove', 'test_mail_full/static/tests/tours/**/*'),
        ],
        'web.assets_tests': [
            'test_mail_full/static/tests/tours/**/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
