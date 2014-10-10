# -*- coding: utf-8 -*-
__author__ = 'mjabrzyk'

import pycountry
import sys, traceback

from sched.models import Resume

def create_linkedin_resume(resume_fields):

    def _get_field(key, dict_=resume_fields):
        try:
            val = dict_.get(key)
            if not bool(val):
                return u""
            else:
                return unicode(val)
        except KeyError:
            return u""

    resume = Resume()

    try:

        resume.name = u" ".join([_get_field(u"firstName"), _get_field(u"lastName")])

        if 'phoneNumbers' in resume_fields:
            try:
                resume.phone = _get_field('phoneNumber', resume_fields['phoneNumbers']['values'][0])
            except KeyError:
                pass

        if 'location' in resume_fields:
            # County from country code
            try:
                country_code = _get_field('code', resume_fields['location']['country']).upper()
                country = pycountry.countries.get(alpha2=country_code)
                resume.country = country.name
            except KeyError:
                pass
            # Place sliced to 50 characters (model has this limitation)
            try:
                city_location = _get_field('name', resume_fields['location'])
                resume.city = city_location[:49] + " " + resume.country
            except KeyError:
                pass

            # Official title (headline from linkedin)
            resume.summary_title = _get_field('headline')
            resume.url = _get_field('publicProfileUrl')

        if 'positions' in resume_fields:
            pos_values = resume_fields['positions']['values']
            company1 = resume_fields['positions']['values'][0]

            resume.company_name = _get_field('name',company1['company'])[:254]
            resume.company_summary = _get_field('industry',company1['company'])[:254]
            resume.role = _get_field('title',company1)
            resume.role_description =_get_field('summary',company1)

            resume.start_date_company = u"/".join([_get_field('month',company1['startDate']),
                                      _get_field('year',company1['startDate'])])
            # When it is current postion the endDate key not extsis
            try:
                resume.end_date_company = u"/".join([_get_field('month',company1['endDate']),
                                      _get_field('year',company1['endDate'])])
            except KeyError:
                pass
            resume.work_currently = bool(company1['isCurrent'])

            # Someone has more that 1 job so we set data for company two
            if int(_get_field('_total',resume_fields['positions']))>1:
                pos_values = resume_fields['positions']['values']
                company2 = resume_fields['positions']['values'][1]

                resume.company_name1 = _get_field('name',company2['company'])[:254]
                resume.company_summary1 = _get_field('industry',company2['company'])[:254]
                resume.role1 = _get_field('title',company2)
                resume.role_description1 =_get_field('summary',company2)

                resume.start_date_company1 = u"/".join([_get_field('month',company2['startDate']),
                                      _get_field('year',company2['startDate'])])
                # When it is current postion the endDate key not extsis
                try:
                    resume.end_date_company1 = u"/".join([_get_field('month',company2['endDate']),
                                      _get_field('year',company2['endDate'])])
                except KeyError:
                    pass
                resume.work_currently1 = bool(company2['isCurrent'])

            # Someone has more that 2 job so we set data for company three
            if int(_get_field('_total',resume_fields['positions']))>2:
                pos_values = resume_fields['positions']['values']
                company3= resume_fields['positions']['values'][2]

                resume.company_name2 = _get_field('name',company3['company'])[:254]
                resume.company_summary2 = _get_field('industry',company3['company'])[:254]
                resume.role2 = _get_field('title',company3)
                resume.role_description2 =_get_field('summary',company3)

                resume.start_date_company2 = u"/".join([_get_field('month',company3['startDate']),
                                      _get_field('year',company3['startDate'])])
                # When it is current postion the endDate key not extsis
                try:
                    resume.end_date_company2 = u"/".join([_get_field('month',company3['endDate']),
                                      _get_field('year',company3['endDate'])])
                except KeyError:
                    pass
                resume.work_currently2 = bool(company3['isCurrent'])


        if 'educations' in resume_fields:
            school1 = resume_fields['educations']['values'][0]

            resume.school_name = _get_field('schoolName',school1)[:254]
            resume.degree_description = _get_field('degree',school1)[:254]
            resume.start_date_school = _get_field('year',school1['startDate'])[:254]
            resume.grading = _get_field('fieldOfStudy',school1)[:254]
            try:
                resume.end_date_school = _get_field('year',school1['endDate'])[:254]
            except KeyError:
                pass

            # Someone has two degrees
            if int(_get_field('_total',resume_fields['educations']))>1:
                school2 = resume_fields['educations']['values'][1]

                resume.school_name1 = _get_field('schoolName',school2)[:254]
                resume.degree_description1 = _get_field('degree',school2)[:254]
                resume.start_date_school1 = _get_field('year',school2['startDate'])[:254]
                resume.grading_two = _get_field('fieldOfStudy',school2)[:254]
                try:
                    resume.end_date_school1 = _get_field('year',school2['endDate'])[:254]
                except KeyError:
                    pass

            # Someone has three degrees
            if int(_get_field('_total',resume_fields['educations']))>2:
                school3 = resume_fields['educations']['values'][2]

                resume.school_name2 = _get_field('schoolName',school3)[:254]
                resume.degree_description2 = _get_field('degree',school3)[:254]
                resume.start_date_school2 = _get_field('year',school3['startDate'])[:254]
                #resume.grading_two = _get_field('fieldOfStudy',school3)[:254]
                try:
                    resume.end_date_school2 = _get_field('year',school3['endDate'])[:254]
                except KeyError:
                    pass

        if 'skills' in resume_fields:
            skills = resume_fields['skills']['values']
            #resume.skills_one = _get_field('name',skills[0]['skill'])[:254]

            # Skills one
            if int(_get_field('_total',resume_fields['skills']))>1:
                resume.other_skills = _get_field('name',skills[0]['skill'])[:254]
            # Skills two
            if int(_get_field('_total',resume_fields['skills']))>2:
                resume.other_skills1 = _get_field('name',skills[1]['skill'])[:254]
            # skills_three
            if int(_get_field('_total',resume_fields['skills']))>3:
                resume.other_skills2 = _get_field('name',skills[2]['skill'])[:254]
            # skills_four
            if int(_get_field('_total',resume_fields['skills']))>4:
                resume.other_skills3 = _get_field('name',skills[3]['skill'])[:254]
            # skills_five
            if int(_get_field('_total',resume_fields['skills']))>5:
                resume.other_skills4 = _get_field('name',skills[4]['skill'])[:254]
            # skills_six
            if int(_get_field('_total',resume_fields['skills']))>6:
                resume.other_skills5 = _get_field('name',skills[5]['skill'])[:254]
            # skills_seven
            if int(_get_field('_total',resume_fields['skills']))>7:
                resume.skills_seven = _get_field('name',skills[6]['skill'])[:254]
            # skills_eight
            if int(_get_field('_total',resume_fields['skills']))>8:
                resume.skills_eight = _get_field('name',skills[7]['skill'])[:254]
            # skills_nine
            if int(_get_field('_total',resume_fields['skills']))>9:
                resume.skills_nine = _get_field('name',skills[8]['skill'])[:254]
            # skills_ten
            if int(_get_field('_total',resume_fields['skills']))>10:
                resume.skills_ten = _get_field('name',skills[9]['skill'])[:254]
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "EXCEPTION!!"
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        return None

    return resume