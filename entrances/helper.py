# -*- coding: utf-8 -*-
from entrances.models import Entrance, Apartment, MonthlyExpence
from dynamic_costs.models import DynamicCost, ApartmentDynamicCost
from nomenclatures.models import TaskType
from tasks.models import Task, PartialTaskPay
from django.utils.html import strip_tags
from django.db.models import Sum, Count
from django.utils.translation import ugettext as _
import xlwt
from vhodove.settings import MEDIA_ROOT
from django.contrib.auth.models import User
from isoweek import Week
from datetime import date
from django.utils.text import slugify
from unidecode import unidecode as _unidecode
import re


class IncomeToXls():

    def create_xls(self):
        horz_style_left = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;')
        horz_style = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;')

        wb = xlwt.Workbook()
        start_row = 1

        entrances = Entrance.objects.filter(active=True)
        task_default_fee = TaskType.objects.get(default_fee=True)
        years = Task.objects.filter(resolved_by_admin=True, task_type=task_default_fee).extra(select={"year": """strftime('%%Y', to_date)"""}).order_by('-year').values_list('year', flat=True).distinct()
        for year in years:
            sheet = wb.add_sheet(year)
            for i in range(1, 13):
                sheet.write(start_row, i, '%s.%s' % (i, year), horz_style)
                sheet.col(i).width = 256 * 9
            month_sums = {}

            sheet.write(start_row, 13, _('Total'), horz_style)
            for e in entrances:
                start_row += 1
                sheet.write(start_row, 0, e.title, horz_style_left)
                sheet.col(0).width = 256 * 50  # 50 characters
                for i in range(1, 13):
                    if e.tax_amount and e.tax_amount > 0:
                        tt = Task.objects.filter(task_type=task_default_fee, entrance=e, resolved_by_admin=True, to_date__year=year, to_date__month=i).aggregate(Count('id'))
                        if tt['id__count'] is None:
                            tt['id__count'] = 0

                        tt['id__count'] = tt['id__count'] * e.tax_amount

                        total_count = tt['id__count']
                    else:
                        try:
                            tt = Task.objects.get(task_type=TaskType.objects.get(home_manager_fee=True), entrance=e, resolved_by_admin=True, to_date__year=year, to_date__month=i)
                            total_count = tt.price
                        except:
                            total_count = 0
                    sheet.write(start_row, i, total_count, horz_style)
                    if i not in month_sums:
                        month_sums[i] = 0
                    if total_count:
                        month_sums[i] += total_count
                    sheet.col(i).width = 256 * 12

                sheet.row(start_row).height = 20 * 16
                rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
                sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style)

            start_row += 1
            sheet.write(start_row, 0, _('Total'), horz_style_left)
            for i in range(1, 13):
                sheet.write(start_row, i, month_sums.get(i), horz_style)
        if not years:
            sheet = wb.add_sheet('-')

        filename = '%s/tmp/income.xls' % (MEDIA_ROOT,)
        wb.save(filename)
        return filename

    def create_kasa_xls(self):
        _all = Entrance.objects.filter(active=True)

        wb = xlwt.Workbook()

        font_header = xlwt.Font()  # Create the Font
        font_header.name = 'Times New Roman'
        font_header.height = 14 * 20  # for 16 point

        header_style = xlwt.XFStyle()
        header_style.font = font_header

        horz_style = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;')
        horz_style_green = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_green')
        horz_style_yellow = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_yellow')
        horz_style_left = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;')
        horz_style_left_green = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_green')
        horz_style_left_yellow = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_yellow')
        horz_style_not_paid = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour silver_ega;')
        horz_style_no_border = xlwt.easyxf('font: height 320, name Arial, bold true; align: wrap on, vert centre, horiz center;')

        for obj in _all:

            #############################
            #  ## PRIHODI ######
            #############################
            title = re.sub("(?u)\W+", " ", obj.title)
            sheet = wb.add_sheet(title)
            sheet.col(0).width = 256 * 50  # 50 characters
            years = Task.objects.filter(resolved_by_admin=True).extra(select={"year": """strftime('%%Y', to_date)"""}).order_by('-year').values_list('year', flat=True).distinct()
            start_row = 2
            for year in years:
                start_row += 1
                sheet.write(start_row, 0, '%s %s' % (_('kasa'), year), horz_style)
                for i in range(1, 13):
                    sheet.write(start_row, i, '%s.%s' % (i, year), horz_style)
                    sheet.col(i).width = 256 * 9

                sheet.write(start_row, 13, _('Price'), horz_style)

                month_sums = {}
                task_types = Task.objects.filter(entrance=obj, resolved_by_admin=True, to_date__year=year, task_type__in=TaskType.objects.filter(can_pay=True)).values_list('task_type_id', flat=True)
                task_types = list(set(task_types))
                for t in task_types:
                    start_row += 1
                    task_type = TaskType.objects.get(id=t)
                    sheet.write(start_row, 0, task_type.title, horz_style_left_green)
                    for i in range(1, 13):
                        # tt = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=True, to_date__year=year, to_date__month=i, apartment_dynamic_cost_id__isnull=True).aggregate(Sum('price'))
                        tt = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=True, to_date__year=year, to_date__month=i).aggregate(Sum('price'))
                        tt1 = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=False, to_date__year=year, to_date__month=i).aggregate(Sum('partial_paid_total'))
                        price_total = 0
                        if tt['price__sum'] is None:
                            tt['price__sum'] = 0
                        if tt1['partial_paid_total__sum'] is None:
                            tt1['partial_paid_total__sum'] = 0
                        price_total = price_total + tt['price__sum'] + tt1['partial_paid_total__sum']
                        sheet.write(start_row, i, price_total, horz_style_green)
                        if i not in month_sums:
                            month_sums[i] = 0
                        month_sums[i] += price_total
                        sheet.col(i).width = 256 * 12

                    sheet.row(start_row).height = 20 * 16
                    rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
                    sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style_green)

                start_row += 1
                sheet.write(start_row, 0, _('Total income'), horz_style_left_green)
                for i in range(1, 13):
                    sheet.write(start_row, i, month_sums.get(i), horz_style_green)

                rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
                sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style_green)
                total_income_cell = "N%s" % (int(start_row) + 1)

                # ############################ RAZHODI
                month_sums = {}
                task_types = Task.objects.filter(entrance=obj, resolved_by_admin=True, to_date__year=year, task_type__in=TaskType.objects.filter(can_pay=False)).values_list('task_type_id', flat=True)
                task_types = list(set(task_types))
                for t in task_types:
                    start_row += 1
                    task_type = TaskType.objects.get(id=t)
                    sheet.write(start_row, 0, task_type.title, horz_style_left)
                    for i in range(1, 13):
                        # tt = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=True, to_date__year=year, to_date__month=i, apartment_dynamic_cost_id__isnull=True).aggregate(Sum('price'))
                        tt = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=True, to_date__year=year, to_date__month=i).aggregate(Sum('price'))
                        tt1 = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=False, to_date__year=year, to_date__month=i).aggregate(Sum('partial_paid_total'))
                        price_total = 0
                        if tt['price__sum'] is None:
                            tt['price__sum'] = 0
                        if tt1['partial_paid_total__sum'] is None:
                            tt1['partial_paid_total__sum'] = 0
                        price_total = price_total + tt['price__sum'] + tt1['partial_paid_total__sum']
                        sheet.write(start_row, i, price_total, horz_style)
                        if i not in month_sums:
                            month_sums[i] = 0
                        month_sums[i] += price_total
                        sheet.col(i).width = 256 * 12

                    sheet.row(start_row).height = 20 * 16
                    rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
                    sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style)

                start_row += 1
                sheet.write(start_row, 0, _('Total outcome'), horz_style_left_yellow)
                for i in range(1, 13):
                    sheet.write(start_row, i, month_sums.get(i), horz_style_yellow)

                rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
                sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style_yellow)
                total_outcome_cell = "N%s" % (int(start_row) + 1)

                start_row += 1
                sheet.write(start_row, 12, _('kasa'), horz_style_left)
                sheet.write(start_row, 13, xlwt.Formula("%s-%s" % (total_income_cell, total_outcome_cell)), horz_style)

                start_row += 3

        filename = '%s/tmp/kasi_vhodove.xls' % (MEDIA_ROOT)
        wb.save(filename)
        return filename

    def create_kasa_xls_summary(self):
        _all = Entrance.objects.filter(active=True)

        wb = xlwt.Workbook()

        font_header = xlwt.Font()  # Create the Font
        font_header.name = 'Times New Roman'
        font_header.height = 14 * 20  # for 16 point

        sheet = wb.add_sheet('Sheet')
        sheet.col(0).width = 256 * 50  # 50 characters
        start_row = 1

        horz_style_left = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;')

        for obj in _all:
            start_row = start_row + 1
            sheet.write(start_row, 0, obj.title, horz_style_left)
            sheet.write(start_row, 1, obj.kasa(), horz_style_left)


        filename = '%s/tmp/kasi_vhodove.xls' % (MEDIA_ROOT)
        wb.save(filename)
        return filename


class CashierIncomeToXls():
    def create_xls(self, user_id=None):
        wb = xlwt.Workbook()

        if(user_id):
            cashiers = User.objects.filter(id__in=[user_id])
        else:
            cashiers = User.objects.filter(groups__id__in=[1])

        year = date.today().year
        month = date.today().month

        for cashier in cashiers:
            sheet = wb.add_sheet("%s %s" % (cashier.first_name, cashier.last_name))
            start_row = 0
            sheet.write(start_row, 0, _('Ot data do data'))
            sheet.write(start_row, 1, _('Obshto subrani'))
            sheet.write(start_row, 2, _('Obshto vhodove'))
            sheet.write(start_row, 3, _('Obshto zatvoreni taskove'))
            sheet.write(start_row, 4, _('Obshto total_price_for_resolve'))
            sheet.write(start_row, 5, _('Razhodi'))
            sheet.write(start_row, 6, _('Za predavane'))

            total_income = 0
            total_outcome = 0
            entrances_count = []
            tasks_count = 0
            total_price_for_resolve = 0
            week_number = -1

            prihodi_ids = TaskType.objects.filter(can_pay=True).values_list('id', flat=True)
            cachier_partial_paid_ids = PartialTaskPay.objects.filter(assignee_id=cashier.id, created_at__year=year, created_at__month=month).values_list('task_id', flat=True)
            task_ids = Task.objects.filter(assignee_id=cashier.id, updated_at__year=year, updated_at__month=month).values_list('id', flat=True)
            all_ids = list(cachier_partial_paid_ids) + list(task_ids)

            tasks = Task.objects.filter(id__in=all_ids).order_by('updated_at').values('id', 'entrance', 'assignee_id', 'task_type_id', 'updated_at', 'price', 'partial_paid_total', 'price_for_resolve', 'resolved', 'resolved_by_admin', 'task_type__can_pay_partial')
            if tasks:
                for t in tasks:
                    t['partial_collected'] = None
                    if t['task_type__can_pay_partial'] is True:
                        t['partial_collected'] = PartialTaskPay.objects.filter(task_id=t['id'], created_at__month=month, assignee=cashier)

                    if(week_number != t['updated_at'].isocalendar()[1]):
                        if week_number != -1:
                            start_row += 1
                            sheet.write(start_row, 0, '%s - %s' % (Week(year, week_number).monday(), Week(year, week_number).sunday()))
                            sheet.write(start_row, 1, total_income)
                            sheet.write(start_row, 2, len(list(set(entrances_count))))
                            sheet.write(start_row, 3, tasks_count)
                            sheet.write(start_row, 4, total_price_for_resolve)
                            sheet.write(start_row, 5, total_outcome)
                            sheet.write(start_row, 6, total_income - total_outcome)
                            total_income = 0
                            total_outcome = 0
                            entrances_count = []
                            tasks_count = 0
                            total_price_for_resolve = 0
                        week_number = t['updated_at'].isocalendar()[1]
                    if not t['partial_paid_total']:
                        t['partial_paid_total'] = 0
                    entrances_count.append(t['entrance'])
                    if not t['price']:
                        t['price'] = 0
                    if t['task_type_id'] in prihodi_ids:
                        if t['partial_collected']:
                                for pc in t['partial_collected']:
                                    if(pc.created_at.isocalendar()[1] == week_number):
                                        total_income += pc.price
                                        if pc.created_at.isocalendar()[1] == 16:
                                            print '%s;chastichno;%s;%s' %(Entrance.objects.get(pk=t['entrance']), pc.price, t['id'])
                        else:
                            if t['resolved']:
                                total_income += t['price']
                                tasks_count += 1
                                if t['updated_at'].isocalendar()[1] == 16:
                                    print '%s;pulno;%s;%s' %(Entrance.objects.get(pk=t['entrance']), t['price'], t['id'])
                                if t['price_for_resolve']:
                                    total_price_for_resolve += t['price_for_resolve']
                    else:
                        if t['partial_collected']:
                                for pc in t['partial_collected']:
                                        if(pc.created_at.isocalendar()[1] == week_number):
                                            total_outcome += pc.price
                        else:
                            if t['resolved']:
                                total_outcome += t['price']
                                tasks_count += 1
                                if t['price_for_resolve']:
                                    total_price_for_resolve += t['price_for_resolve']

                week_number = t['updated_at'].isocalendar()[1]
                start_row += 1
                sheet.write(start_row, 0, '%s - %s' % (Week(year, week_number).monday(), Week(year, week_number).sunday()))
                sheet.write(start_row, 1, total_income)
                sheet.write(start_row, 2, len(list(set(entrances_count))))
                sheet.write(start_row, 3, tasks_count)
                sheet.write(start_row, 4, total_price_for_resolve)
                sheet.write(start_row, 5, total_outcome)
                sheet.write(start_row, 6, total_income - total_outcome)

                start_row += 1
                sheet.write(start_row, 0, _('Total'))
                sheet.write(start_row, 1, xlwt.Formula("SUM(B2:B%s)" % start_row))
                sheet.write(start_row, 2, xlwt.Formula("SUM(C2:C%s)" % start_row))
                sheet.write(start_row, 3, xlwt.Formula("SUM(D2:D%s)" % start_row))
                sheet.write(start_row, 4, xlwt.Formula("SUM(E2:E%s)" % start_row))
                sheet.write(start_row, 5, xlwt.Formula("SUM(F2:F%s)" % start_row))
                sheet.write(start_row, 6, xlwt.Formula("SUM(G2:G%s)" % start_row))

        filename = '%s/tmp/cachier_income.xls' % (MEDIA_ROOT,)
        wb.save(filename)
        return filename


class EntranceToXls():

    def __init__(self, id):
        self.id = id

    def create_xls(self):
        obj = Entrance.objects.get(id=self.id)
        dynamic_costs = DynamicCost.objects.filter(entrance=obj, active=1, task_type__in=TaskType.objects.filter(can_pay=True))
        apartments = Apartment.objects.filter(entrance=obj)

        wb = xlwt.Workbook()

        font_header = xlwt.Font()  # Create the Font
        font_header.name = 'Times New Roman'
        font_header.height = 14 * 20  # for 16 point

        header_style = xlwt.XFStyle()
        header_style.font = font_header

        horz_style = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;')
        horz_style_green = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_green')
        horz_style_yellow = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_yellow')
        horz_style_left = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;')
        horz_style_left_green = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_green')
        horz_style_left_yellow = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_yellow')
        horz_style_not_paid = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour silver_ega;')
        horz_style_no_border = xlwt.easyxf('font: height 320, name Arial, bold true; align: wrap on, vert centre, horiz center;')

        #############################
        #  ## PRIHODI ######
        #############################

        sheet = wb.add_sheet(_('kasa'))
        sheet.col(0).width = 256 * 50  # 50 characters
        years = Task.objects.filter(resolved_by_admin=True).extra(select={"year": """strftime('%%Y', to_date)"""}).order_by('-year').values_list('year', flat=True).distinct()
        start_row = 2
        years_cells = {}
        for year in years:
            start_row += 1
            sheet.write(start_row, 0, '%s %s' % (_('kasa'), year), horz_style)
            for i in range(1, 13):
                sheet.write(start_row, i, '%s.%s' % (i, year), horz_style)
                sheet.col(i).width = 256 * 9

            sheet.write(start_row, 13, _('Price'), horz_style)

            fake_start_row = 0
            if int(year) > 2015:
                start_row += 1
                fake_start_row = start_row + 1
                sheet.write(start_row, 0, '%s %s' % (_('kasa'), int(year)-1), horz_style_left_green)

            years_cells[year] = {'start_row': start_row}
            month_sums = {}
            task_types = Task.objects.filter(entrance=obj, resolved_by_admin=True, to_date__year=year, task_type__in=TaskType.objects.filter(can_pay=True)).values_list('task_type_id', flat=True)
            task_types = list(set(task_types))
            for t in task_types:
                start_row += 1
                task_type = TaskType.objects.get(id=t)
                sheet.write(start_row, 0, task_type.title, horz_style_left_green)
                for i in range(1, 13):
                    # tt = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=True, to_date__year=year, to_date__month=i, apartment_dynamic_cost_id__isnull=True).aggregate(Sum('price'))
                    tt = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=True, to_date__year=year, to_date__month=i).aggregate(Sum('price'))
                    tt1 = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=False, to_date__year=year, to_date__month=i).aggregate(Sum('partial_paid_total'))
                    price_total = 0
                    if tt['price__sum'] is None:
                        tt['price__sum'] = 0
                    if tt1['partial_paid_total__sum'] is None:
                        tt1['partial_paid_total__sum'] = 0
                    price_total = price_total + tt['price__sum'] + tt1['partial_paid_total__sum']
                    sheet.write(start_row, i, price_total, horz_style_green)
                    if i not in month_sums:
                        month_sums[i] = 0
                    month_sums[i] += price_total
                    sheet.col(i).width = 256 * 12

                sheet.row(start_row).height = 20 * 16
                rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
                sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style_green)

            start_row += 1
            sheet.write(start_row, 0, _('Total income'), horz_style_left_green)
            for i in range(1, 13):
                if fake_start_row != 0 and i == 1:
                    sheet.write(start_row, i, xlwt.Formula("SUM(B%s:B%s)" % (fake_start_row, start_row)), horz_style_green)
                else:
                    sheet.write(start_row, i, month_sums.get(i), horz_style_green)

            rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
            sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style_green)
            total_income_cell = "N%s" % (int(start_row) + 1)

            # ############################ RAZHODI
            month_sums = {}
            task_types = Task.objects.filter(entrance=obj, resolved_by_admin=True, to_date__year=year, task_type__in=TaskType.objects.filter(can_pay=False)).values_list('task_type_id', flat=True)
            task_types = list(set(task_types))
            for t in task_types:
                start_row += 1
                task_type = TaskType.objects.get(id=t)
                sheet.write(start_row, 0, task_type.title, horz_style_left)
                for i in range(1, 13):
                    # tt = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=True, to_date__year=year, to_date__month=i, apartment_dynamic_cost_id__isnull=True).aggregate(Sum('price'))
                    tt = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=True, to_date__year=year, to_date__month=i).aggregate(Sum('price'))
                    tt1 = Task.objects.filter(task_type=task_type, entrance=obj, resolved_by_admin=False, to_date__year=year, to_date__month=i).aggregate(Sum('partial_paid_total'))
                    price_total = 0
                    if tt['price__sum'] is None:
                        tt['price__sum'] = 0
                    if tt1['partial_paid_total__sum'] is None:
                        tt1['partial_paid_total__sum'] = 0
                    price_total = price_total + tt['price__sum'] + tt1['partial_paid_total__sum']
                    sheet.write(start_row, i, price_total, horz_style)
                    if i not in month_sums:
                        month_sums[i] = 0
                    month_sums[i] += price_total
                    sheet.col(i).width = 256 * 12

                sheet.row(start_row).height = 20 * 16
                rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
                sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style)

            start_row += 1
            sheet.write(start_row, 0, _('Total outcome'), horz_style_left_yellow)
            for i in range(1, 13):
                sheet.write(start_row, i, month_sums.get(i), horz_style_yellow)

            rng = (start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1, start_row + 1)
            sheet.write(start_row, 13, xlwt.Formula("SUM(B%s+C%s+D%s+E%s+F%s+G%s+H%s+I%s+J%s+K%s+L%s+M%s)" % rng), horz_style_yellow)
            total_outcome_cell = "N%s" % (int(start_row) + 1)

            start_row += 1
            sheet.write(start_row, 12, _('kasa'), horz_style_left)
            sheet.write(start_row, 13, xlwt.Formula("%s-%s" % (total_income_cell, total_outcome_cell)), horz_style)

            years_cells[year]['value'] = "N%s" % (start_row + 1)
            start_row += 3


        # STARI KASI
        for k in years_cells:
            k = int(k)
            if k > 2015:
                sheet.write(years_cells[str(k)]['start_row'], 1, xlwt.Formula(years_cells[str(k-1)]['value']), horz_style_green)
                sheet.write(years_cells[str(k)]['start_row'], 13, xlwt.Formula(years_cells[str(k-1)]['value']), horz_style_green)
                for i in range(2, 13):
                    sheet.write(years_cells[str(k)]['start_row'], i, 0, horz_style_green)

        #############################
        # ## TABOVE ######
        #############################

        years = Task.objects.filter(task_type=TaskType.objects.get(default_fee=True), entrance=obj).extra(select={"year": """strftime('%%Y', to_date)"""}).order_by('-year').values_list('year').distinct()
        for year in years:
            year = year[0]
            tasks = Task.objects.filter(task_type=TaskType.objects.get(default_fee=True), to_date__year=year, entrance=obj)
            sheet = wb.add_sheet('%s' % year)

            sheet.write(0, 1, '%s: %s (%s)' % (_('Tax at address'), obj.title, year), header_style)  # sheet.write(top_row, left_column, 'Long Cell')
            sheet.merge(0, 0, 1, 17)  # sheet.merge(top_row, bottom_row, left_column, right_column)
            sheet.row(0).height = 24 * 16
            start_row = 2

            sheet.write(start_row, 1, _('Floor'), horz_style)
            sheet.write(start_row, 2, _('Apartment'), horz_style)
            sheet.write(start_row, 3, _('Number of occupants'), horz_style)
            sheet.write(start_row, 4, _('Contact person'), horz_style)
            sheet.write(start_row, 5, _('Monthly payment'), horz_style)
            sheet.write(start_row, 6, _('Due payment'), horz_style)
            sheet.write(start_row, 19, _('Collected'), horz_style)
            sheet.row(start_row).height = 20 * 16

            sheet.col(1).width = 256 * 6  # 7 characters
            sheet.col(2).width = 256 * 12  # 14 characters
            sheet.col(3).width = 256 * 14  # 18 characters
            sheet.col(4).width = 256 * 22  # 24 characters
            sheet.col(5).width = 256 * 10  # 12 characters
            sheet.col(6).width = 256 * 12  # 12 characters
            sheet.col(19).width = 256 * 10  # 12 characters

            for i in range(1, 13):
                sheet.write(start_row, 6 + i, '%s.%s' % (i, year), horz_style)
                sheet.col(5 + i).width = 256 * 9

            cells = {}
            month_payments = {}
            for a in apartments:
                    start_row += 1
                    sheet.row(start_row).height = 20 * 16
                    sheet.write(start_row, 1, a.floor, horz_style)
                    sheet.write(start_row, 2, a.apartment, horz_style)
                    sheet.write(start_row, 3, a.number_of_occupants, horz_style)
                    sheet.write(start_row, 4, a.contact_person, horz_style)
                    sheet.write(start_row, 5, a.monthly_fee, horz_style)

                    fees = tasks.filter(apartment=a)
                    due_payment = 0
                    collected = 0
                    cells[start_row] = {}
                    for f in fees:
                        cells[start_row][f.to_date.month] = f.price
                        try:
                            sheet.write(start_row, 6 + f.to_date.month, f.price or 0, horz_style if f.resolved_by_admin else horz_style_not_paid)
                        except:
                            pass
                        if f.resolved_by_admin:
                            if f.to_date.month not in month_payments:
                                month_payments[f.to_date.month] = 0
                            month_payments[f.to_date.month] += f.price
                            collected += f.price
                        else:
                            if f.price:
                                due_payment += f.price
                    sheet.write(start_row, 6, due_payment or 0, horz_style)
                    sheet.write(start_row, 19, collected or 0, horz_style)

            start_row += 1
            sheet.write(start_row, 6, _('Total'), horz_style)
            for i in range(1, 13):
                sheet.write(start_row, 6 + i, month_payments.get(i, 0), horz_style)

            for c in cells:
                for i in range(1, 13):
                    val = cells[c].get(i)
                    if not val:
                        try:
                            sheet.write(c, 6 + i, val, horz_style)
                        except:
                            pass

        for d in dynamic_costs:
            tasks = Task.objects.filter(apartment_dynamic_cost_id__in=ApartmentDynamicCost.objects.filter(cost=d).values_list('id', flat=True))
            if tasks:
                try:
                    sheet = wb.add_sheet(d.title[:30])
                except:
                    sheet = wb.add_sheet('%s-%s' % (d.title[:27], d.id))

                total_price = 0
                total_partial_price = 0

                sheet.write(0, 1, obj.title.strip(), header_style)  # sheet.write(top_row, left_column, 'Long Cell')
                sheet.merge(0, 0, 1, 7)  # sheet.merge(top_row, bottom_row, left_column, right_column)
                sheet.row(0).height = 24 * 16

                sheet.write(1, 1, d.title.strip(), header_style)  # sheet.write(top_row, left_column, 'Long Cell')
                sheet.merge(1, 1, 1, 7)  # sheet.merge(top_row, bottom_row, left_column, right_column)
                sheet.row(1).height = 24 * 16

                info = strip_tags(d.common_information).strip()
                if info:
                    sheet.write(2, 1, strip_tags(d.common_information).strip(), header_style)  # sheet.write(top_row, left_column, 'Long Cell')
                    sheet.merge(2, 2, 1, 7)  # sheet.merge(top_row, bottom_row, left_column, right_column)
                    sheet.row(2).height = 24 * 16

                start_row = 3
                sheet.write(start_row, 1, _('Floor'), horz_style)
                sheet.write(start_row, 2, _('Apartment'), horz_style)
                sheet.write(start_row, 3, _('Number of occupants'), horz_style)
                sheet.write(start_row, 4, _('Contact person'), horz_style)
                sheet.write(start_row, 5, _('Price'), horz_style)
                sheet.write(start_row, 6, _('Sum paid'), horz_style)

                sheet.col(1).width = 256 * 7  # 7 characters
                sheet.col(2).width = 256 * 16  # 16 characters
                sheet.col(3).width = 256 * 18  # 18 characters
                sheet.col(4).width = 256 * 24  # 24 characters
                sheet.col(5).width = 256 * 12  # 12 characters
                sheet.col(6).width = 256 * 12  # 12 characters

                sheet.row(start_row).height = 20 * 16

                sheet.write(start_row, 7, _('For Payment'), horz_style)
                sheet.col(7).width = 256 * 25  # 25 characters

                for t in tasks:
                    start_row += 1
                    sheet.write(start_row, 1, t.apartment.floor, horz_style)
                    sheet.write(start_row, 2, t.apartment.apartment, horz_style)
                    sheet.write(start_row, 3, t.apartment.number_of_occupants, horz_style)
                    sheet.write(start_row, 4, t.apartment.contact_person, horz_style)
                    sheet.write(start_row, 5, t.price or 0, horz_style)

                    if t.price:
                        total_price += t.price

                    if t.resolved_by_admin:
                        if t.price:
                            total_partial_price += t.price
                        sheet.write(start_row, 6, t.price, horz_style)
                    else:
                        if t.partial_paid_total:
                            total_partial_price += t.partial_paid_total
                        sheet.write(start_row, 6, t.partial_paid_total or 0, horz_style)

                    sheet.write(start_row, 7, xlwt.Formula("SUM(F%s-G%s)" % (start_row+1, start_row+1)), horz_style)
                    sheet.row(start_row).height = 20 * 16

                start_row += 1
                sheet.write(start_row, 5, total_price or 0, horz_style_no_border)
                sheet.write(start_row, 6, total_partial_price or 0, horz_style_no_border)
                sheet.write(start_row, 7, xlwt.Formula("SUM(F%s-G%s)" % (start_row+1, start_row+1)), horz_style_no_border)



        administrative_tasks = Task.objects.filter(task_type__in=TaskType.objects.filter(is_administrative=True), entrance=obj).order_by('-date')
        if administrative_tasks:
            start_row = 2
            sheet = wb.add_sheet('%s' % _('Administrative Tasks'))
            sheet.write(start_row, 1, _('Month'), horz_style)
            sheet.write(start_row, 2, _('User'), horz_style)
            sheet.write(start_row, 3, _('task'), horz_style)
            sheet.write(start_row, 4, _('Common information'), horz_style)

            sheet.col(1).width = 256 * 7  # 7 characters
            sheet.col(2).width = 256 * 24  # 24 characters
            sheet.col(3).width = 256 * 60  # 300 characters
            sheet.col(4).width = 256 * 60  # 300 characters
            sheet.row(start_row).height = 20 * 16
            for a in administrative_tasks:
                start_row+=1
                sheet.write(start_row, 1, a.get_date(), horz_style)
                sheet.write(start_row, 2, a.assignee.get_full_name() if a.assignee_id else '-', horz_style)
                sheet.write(start_row, 3, a.title, horz_style)
                sheet.write(start_row, 4, strip_tags(a.common_information) if a.common_information else '', horz_style)
        filename = '%s/tmp/%s-%s.xls' % (MEDIA_ROOT, slugify(unicode(_unidecode(obj.title))), obj.id)
        wb.save(filename)
        return filename


    def create_static_xls(self):
        wb = xlwt.Workbook()
        horz_style = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;')
        task_type_ids = MonthlyExpence.objects.all().values_list('task_type_id');
        _all = TaskType.objects.filter(id__in=task_type_ids, active=True)
        entrances = Entrance.objects.filter(active=True).order_by('position')

        for a in _all:
            _data = {};
            total = 0;

            tasks = Task.objects.filter(task_type=a, resolved_by_admin=False)
            for t in tasks:
                if t.entrance_id not in _data:
                    _data[t.entrance_id] = {'cnt': 0, 'price': 0}
                _data[t.entrance_id]['cnt'] = _data[t.entrance_id]['cnt'] + 1
                _data[t.entrance_id]['price'] = _data[t.entrance_id]['price'] + t.price
                if t.partial_paid_total:
                    _data[t.entrance_id]['price'] = _data[t.entrance_id]['price'] - t.partial_paid_total
                total = total + _data[t.entrance_id]['price']

            if not total:
                continue

            sheet = wb.add_sheet(a.title)
            sheet.col(0).width = 256 * 35  # 50 characters
            sheet.col(1).width = 256 * 15  # 50 characters
            sheet.col(2).width = 256 * 15  # 50 characters


            sheet.write(1, 0, "%s %s" %(a.title, _('zaduljeniq')), xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz centre;'))
            sheet.merge(1, 1, 0, 2)  # sheet.merge(top_row, bottom_row, left_column, right_column)

            sheet.write(3, 0, _('Entrance'), xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz centre;'))
            sheet.write(3, 1, _('unpaid_months') , xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz centre;'))
            sheet.write(3, 2, _('total_duljima_suma'), xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz centre;'))
            sheet.row(3).height = 20 * 26
            start_column = 0
            start_row = 3


            for e in entrances:
                start_row+=1
                sheet.write(start_row, start_column, e.title, horz_style)
                sheet.write(start_row, start_column+1, _data[e.id]['cnt'] if e.id in _data else 0 , xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz centre;'))
                sheet.write(start_row, start_column+2, _data[e.id]['price'] if e.id in _data else 0, xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz centre;'))

            start_row+=1
            sheet.write(start_row, start_column+2, xlwt.Formula("SUM(C3:C%s)" % (start_row)), xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz centre;'))
        filename = '%s/tmp/statichni-razhodi.xls' % (MEDIA_ROOT)
        wb.save(filename)
        return filename

    def create_contacts_xls(self):
        obj = None
        apartments = Apartment.objects.all().order_by('entrance__position')
        if self.id=='0':
            self.id = None
        if self.id:
            obj = Entrance.objects.get(id=self.id)
            apartments =  apartments.filter(entrance=obj)
        wb = xlwt.Workbook()
        font_header = xlwt.Font()  # Create the Font
        font_header.name = 'Times New Roman'
        font_header.height = 14 * 20  # for 16 point

        header_style = xlwt.XFStyle()
        header_style.font = font_header

        horz_style = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;')
        horz_style_green = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_green')
        horz_style_yellow = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_yellow')
        horz_style_left = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;')
        horz_style_left_green = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_green')
        horz_style_left_yellow = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz left;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour light_yellow')
        horz_style_not_paid = xlwt.easyxf('font: height 320, name Arial; align: wrap on, vert centre, horiz center;borders: top medium, bottom medium, left medium, right medium;pattern: pattern solid, fore_colour silver_ega;')
        horz_style_no_border = xlwt.easyxf('font: height 320, name Arial, bold true; align: wrap on, vert centre, horiz center;')

        sheet = wb.add_sheet(_('Contacts'))
        sheet.col(0).width = 256 * 50  # 50 characters

        start_row = 1
        start_column = 1
        sheet.write(start_row, start_column, _('Entrance'), horz_style)
        sheet.write(start_row, start_column+1, _('Floor'), horz_style)
        sheet.write(start_row, start_column+2, _('Apartment'), horz_style)
        sheet.write(start_row, start_column+3, _('Common area'), horz_style)
        sheet.write(start_row, start_column+4, _('Monthly fee'), horz_style)
        sheet.write(start_row, start_column+5, _('Contact person'), horz_style)
        sheet.write(start_row, start_column+6, _('Contact phone'), horz_style)
        sheet.write(start_row, start_column+7, _('Contact email'), horz_style)
        sheet.write(start_row, start_column+8, _('Number of occupants'), horz_style)
        sheet.write(start_row, start_column+9, _('Has pet'), horz_style)
        sheet.write(start_row, start_column+10, _('Easypay Id'), horz_style)

        sheet.col(0).width = 256 * 7
        sheet.col(start_column).width = 256 * 40
        sheet.col(start_column+1).width = 256 * 7
        sheet.col(start_column+2).width = 256 * 12
        sheet.col(start_column+3).width = 256 * 12
        sheet.col(start_column+4).width = 256 * 15
        sheet.col(start_column+5).width = 256 * 26
        sheet.col(start_column+6).width = 256 * 20
        sheet.col(start_column+7).width = 256 * 26
        sheet.row(start_row).height = 20 * 40

        for a in apartments:
            start_row+=1
            sheet.write(start_row, start_column, a.entrance.title, horz_style)
            sheet.write(start_row, start_column+1, a.floor, horz_style)
            sheet.write(start_row, start_column+2, a.apartment, horz_style)
            sheet.write(start_row, start_column+3, a.common_area if a.common_area else 0, horz_style)
            sheet.write(start_row, start_column+4, a.monthly_fee if a.monthly_fee else 0, horz_style)
            sheet.write(start_row, start_column+5, a.contact_person, horz_style)
            sheet.write(start_row, start_column+6, a.contact_phone, horz_style)
            sheet.write(start_row, start_column+7, a.contact_email, horz_style)
            sheet.write(start_row, start_column+8, int(a.number_of_occupants) if a.number_of_occupants else 0, horz_style)
            sheet.write(start_row, start_column+9, _('Yes') if a.has_pet else _('No'), horz_style)
            sheet.write(start_row, start_column+10, a.easypay_id(), horz_style)
            sheet.row(start_row).height = 20 * 26



        sheet.write(start_row+1, start_column+8, xlwt.Formula("SUM(J3:J%s)" % (start_row+1)), horz_style)

        if self.id:
            filename = '%s/tmp/Apartments-%s.xls' % (MEDIA_ROOT, slugify(unicode(_unidecode(obj.title))))
        else:
            filename = '%s/tmp/Apartments-%s.xls' % (MEDIA_ROOT, 'all')
        wb.save(filename)
        return filename
