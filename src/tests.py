import unittest
from model import EventPlanner
from mockIntranet import MockIntranet
from mockData import events, students
from checkers import check_autologin, check_hour_format, execRegex, check_activity_format

class TestCheckersFunctions(unittest.TestCase):
    def test_exec_regex_error(self):
        self.assertFalse(execRegex(r'azeasqd', 'https://localhost:8000'))

    def test_exec_regex_good(self):
        self.assertEqual(execRegex(r'https', 'https://localhost:8000'), True)

    def test_check_autologin_good_short(self):
        self.assertEqual(check_autologin('auth-abcdef123456789abcdef'), 'https://intra.epitech.eu/auth-abcdef123456789abcdef')

    def test_check_autologin_good_medium(self):
        self.assertEqual(check_autologin('http://intra.epitech.eu/auth-abcdef123456789abcdef'), 'https://intra.epitech.eu/auth-abcdef123456789abcdef')

    def test_check_autologin_good_long(self):
        self.assertEqual(check_autologin('intra.epitech.eu/auth-abcdef123456789abcdef'), 'https://intra.epitech.eu/auth-abcdef123456789abcdef')

    def test_check_autologin_error_hexa(self):
        self.assertFalse(check_autologin('auth-abcdefg123456789abcdef'))

    def test_check_autologin_error_format(self):
        self.assertFalse(check_autologin('-abcdef123456789abcdef'))

    def test_check_hour_format_good(self):
        self.assertEqual(check_hour_format('10:00:00'), True)

    def test_check_hour_format_error_seconds(self):
        self.assertFalse(check_hour_format('10:00:70'))
    
    def test_check_hour_format_error_minutes(self):
        self.assertFalse(check_hour_format('10:70:10'))

    def test_check_hour_format_error_hour(self):
        self.assertFalse(check_hour_format('70:00:00'))

    def test_check_hour_format_error_format(self):
        self.assertFalse(check_hour_format('abcd'))
        self.assertFalse(check_hour_format('10'))
        self.assertFalse(check_hour_format('10:20'))
        self.assertFalse(check_hour_format(':20:20'))
        self.assertFalse(check_hour_format(':::'))
        self.assertFalse(check_hour_format('"1"2"3"2"3"'))

    def test_check_activity_format_error1(self):
        self.assertFalse(check_activity_format('module/2021/W-ADM-007/acti-505014'))

    def test_check_activity_format_error2(self):
        self.assertFalse(check_activity_format('/2021/W-ADM-007/acti-505014'))

    def test_check_activity_format_error3(self):
        self.assertFalse(check_activity_format('module/2021/W-ADM-007/truc-505014'))

    def test_check_activity_format_error4(self):
        self.assertFalse(check_activity_format('module/2021/B-CNA-410/acti-505014/'))

    def test_check_activity_format_error5(self):
        self.assertFalse(check_activity_format('je/suis/un/crapo'))

    def test_check_activity_format_good(self):
        self.assertEqual(check_activity_format('/module/2021/W-ADM-007/LYN-4-1/acti-509029/'), True)

class TestModelIntranet(unittest.TestCase):
    def test_registration_good(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', ['wac1', 'wac2', 'msc1', 'msc2', 'premsc'], '2021')
        self.assertEqual(te, students)

    def test_registration_error_promotion_none(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', None, '2021')
        self.assertEqual(te, None)

    def test_registration_error_promotion_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', [], '2021')
        self.assertEqual(te, None)

    def test_registration_error_event_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration('', ['wac1', 'wac2'], '2021')
        self.assertEqual(te, None)
    
    def test_registration_error_event_none(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(None, ['wac1', 'wac2'], '2021')
        self.assertEqual(te, None)

    def test_registration_error_year_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration('', ['wac1', 'wac2'], '')
        self.assertEqual(te, None)

    def test_registration_error_year_wrong(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration('', ['wac1', 'wac2'], 0)
        self.assertEqual(te, None)

    def test_registration_error_year_negative(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration('', ['wac1', 'wac2'], -2021)
        self.assertEqual(te, None)


    def test_planify_session_good(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions('module/2021/W-ADM-007/LYN-0-1/acti-505014', ['2022-04-04'], ['10:10:10'])
        self.assertEqual(te, events)

    def test_planify_session_error_date_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions('/module/2021/W-ADM-007/LYN-0-1/acti-505014/', [], ['10:10:10'])
        self.assertEqual(te, None)

    def test_planify_session_error_hour_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions('/module/2021/W-ADM-007/LYN-0-1/acti-505014/', ['2022-04-04'], [])
        self.assertEqual(te, None)

    def test_planify_session_errors_none(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions('/module/2021/W-ADM-007/LYN-0-1/acti-505014/', None, None)
        self.assertEqual(te, None)

    def test_planify_session_errors_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions('/module/2021/W-ADM-007/LYN-0-1/acti-505014/', [], [])
        self.assertEqual(te, None)

if __name__ == '__main__':
    unittest.main()