from datetime import datetime
import numpy as np


def check_date_format(date_str):
    try:
        # Attempt to parse the date string using the first format "%Y-%m-%dT%H:%M:%S"
        return np.datetime64(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S"))

    except ValueError:
        try:
            # Attempt to parse the date string using the second format "%Y-%m-%d"
            return np.datetime64(datetime.strptime(date_str, "%Y-%m-%d"))

        except ValueError:
            # If neither format matches, raise an exception or return an appropriate message
            raise ValueError("Invalid date format")


def create_narration(text):
    try:
        x = text.split(sep=' ')
        # Captures the first instance where text starts with '|'
        start_point = x.index([i for i in x if i.startswith('|')][0])
        # Captures the first instance where text ends starts with '|'
        end_point = x.index([j for j in x if j.endswith('|')][0]) + 1
        return ' '.join(x[start_point:end_point]).title().replace('|', '')
    except (IndexError, AttributeError):
        # to handle situation where narration text does not start with / ends with '|' or
        # does not have '|' at all
        return None


company_info = [
    {'cid': '1',
     'data': {
         'database': 'nadunjayathunga$elite_security',
         'long_name': 'Elite Security Services',
         'abbr': 'ESS',
         'rev_cat': ['Manpower', 'Projects', 'Services'],
         'nav_links': ['Finance', 'HR', 'Operations', 'Sales'],
         'constants': {'RP': 1_220, 'HC': 100, 'TRAINING': 500, 'ACCOMODATION': 3_420, 'TRPT': 3_000},
         'voucher_types': {'Sales Invoice': -1, 'Credit Note': -1, 'Journal Entry': 0, 'Project Invoice': 0,
                           'Contract Invoice': -1, 'Debit Note': -1, 'Receipt': 0, 'SERVICE INVOICE': -1},
     }
     },
    {'cid': '2',
     'data': {
         'database': 'nadunjayathunga$premium',
         'long_name': 'Premium Hospitality',
         'abbr': 'PH',
         'rev_cat': ['Manpower'],
         'nav_links': ['Finance', 'Operations', 'Sales'],
         'constants': {'RP': 1_220, 'HC': 100, 'TRAINING': 500, 'ACCOMODATION': 3_320, 'TRPT': 3_000},
         'voucher_types': {'Sales Invoice': -1, 'Credit Note': -1, 'Journal Entry': -2, 'Project Invoice': -2,
                           'Receipt': -1, 'Contract Invoice': -1, 'Debit Note': -1, 'SERVICE INVOICE': -1}}
     },
    {'cid': '3',
     'data': {
         'database': 'nadunjayathunga$nbn_logistics',
         'long_name': 'NBN Logistics',
         'abbr': 'NBL',
         'rev_cat': ['Clearance', 'Transport', 'Freight', 'Other'],
         'nav_links': ['Finance', 'HR', 'Sales'],
         'constants': {'RP': 0, 'HC': 0, 'TRAINING': 0, 'ACCOMODATION': 0, 'TRPT': 0},
         'voucher_types': {'Sales Invoice': -1, 'Credit Note': -1, 'Journal Entry': -1, 'Project Invoice': -2,
                           'Receipt': -1, 'Contract Invoice': -1, 'Debit Note': -1, 'SERVICE INVOICE': -1}}
     },
    {'cid': '4',
     'data': {
         'database': 'nadunjayathunga$nbn_realestate',
         'long_name': 'NBN Real Estate',
         'abbr': 'NBR',
         'rev_cat': ['Clearance', 'Transport', 'Freight', 'Other'],
         'nav_links': ['Finance', 'HR', 'Sales'],
         'constants': {'RP': 0, 'HC': 0, 'TRAINING': 0, 'ACCOMODATION': 0, 'TRPT': 0},
         'voucher_types': {'Sales Invoice': -1, 'Credit Note': -1, 'Journal Entry': -1, 'Project Invoice': -2,
                           'Receipt': -1, 'Contract Invoice': -1, 'Debit Note': -1, 'SERVICE INVOICE': -1}}
     }
]

table_info = [
    {
        'sheetname': 'fData',
        'usecols': ['voucher_number', 'voucher_date', 'type', 'ledger_code', 'business_unit',
                    'job_number', 'service_element_code', 'debit', 'credit'],
        'index': 'voucher_number'
    },
    {
        'sheetname': 'fLogInv',
        'usecols': ['job_number', 'invoice_number', 'invoice_date', 'customer_code', 'sales_person_code', 'net_amount'],
        'index': 'invoice_number'
    },
    {
        'sheetname': 'fOutSourceInv',
        'usecols': ['invoice_number', 'invoice_date', 'customer_code', 'net_amount'],
        'index': 'invoice_number'
    },
    {
        'sheetname': 'fAMCInv',
        'usecols': ['invoice_number', 'invoice_date', 'customer_code', 'net_amount'],
        'index': 'invoice_number'
    },
    {
        'sheetname': 'fProInv',
        'usecols': ['invoice_number', 'invoice_date', 'customer_code', 'net_amount', 'order_id'],
        'index': 'invoice_number'
    },
    {
        'sheetname': 'fCreditNote',
        'usecols': ['invoice_number', 'invoice_date', 'ledger_code', 'net_amount', 'type'],
        'index': 'invoice_number'
    },
    {
        'sheetname': 'fBudget',
        'usecols': ['fy', 'ledger_code', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov',
                    'dec'],
        'index': 'ledger_code'
    },
    {
        'sheetname': 'dEmployee',
        'usecols': ['emp_id', 'emp_type', 'emp_name', 'dept', 'designation', 'grade', 'dob', 'doj', 'leave_policy',
                    'nationality', 'confirmation_date', 'sex', 'maritial_state', 'travel_cost', 'current_status',
                    'last_increment', 'last_rejoin', 'termination_date', 'ba', 'hra', 'tra', 'ma', 'oa', 'pda'],
        'index': 'emp_id'
    },
    {
        'sheetname': 'dJobs',
        'usecols': ['job_number', 'customer_code', 'job_date', 'emp_id'],
        'index': 'job_number'
    },
    {
        'sheetname': 'fGL',
        'usecols': ['bussiness_unit_name', 'cost_center', 'voucher_date', 'voucher_number', 'credit', 'debit',
                    'transaction_type', 'job_number', 'ledger_code', 'narration'],
        'index': 'ledger_code'
    },
    {
        'sheetname': 'fGlJob',
        'usecols': ['voucher_date', 'voucher_number', 'credit', 'debit', 'transaction_type', 'job_number',
                    'ledger_code'],
        'index': 'ledger_code'
    },
    {
        'sheetname': 'dCoAAdler',
        'usecols': ['ledger_code', 'ledger_name', 'first_level', 'forth_level', 'third_level', 'second_level'],
        'index': 'ledger_code'
    },
    {
        'sheetname': 'dCustomers',
        'usecols': ['customer_code', 'cus_name', 'ledger_code'],
        'index': 'customer_code'
    },
    {
        'sheetname': 'fOT',
        'usecols': ['cost_center', 'date', 'job_id', 'attendance', 'ot_hr', 'net', 'day_type'],
        'index': 'cost_center'
    },
    {
        'sheetname': 'fBudget',
        'usecols': ['fy', 'ledger_code', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov',
                    'dec'],
        'index': 'ledger_code'
    }
]

fin_tiles_values = [
    {'value': 'Revenue', 'filt': [
        'Logistics Revenue', 'Manpower Revenue', 'Projects Revenue', 'Services Revenue']},

    {'value': 'GP', 'filt': ['Logistics Revenue', 'Manpower Revenue', 'Projects Revenue', 'Services Revenue',
                             'Staff Cost - Logistics', 'Service Cost - Logistics', 'Accommodation - Manpower',
                             'Staff Cost - Manpower',
                             'Transportation - Manpower', 'Others - Manpower',
                             'Material Parts & Consumables - Projects', 'Staff Cost - Projects',
                             'Maintenance - Projects', 'Depreciation - Projects', 'Others - Projects',
                             'Material Parts & Consumables - Services']},

    {'value': 'Overhead', 'filt': ['Staff Cost', 'Rental Expenses', 'Office Expenses.', 'Sales & Promotion',
                                   'Management Fees', 'Professional & Legal', 'Depreciation', 'Others - G & A',
                                   'Provision for Doubtful debts']},

    {'value': 'NP', 'filt': ['Logistics Revenue', 'Manpower Revenue', 'Projects Revenue', 'Services Revenue',
                             'Staff Cost - Logistics', 'Service Cost - Logistics', 'Accommodation - Manpower',
                             'Staff Cost - Manpower',
                             'Transportation - Manpower', 'Others - Manpower',
                             'Material Parts & Consumables - Projects', 'Staff Cost - Projects',
                             'Maintenance - Projects', 'Depreciation - Projects', 'Others - Projects',
                             'Interest Expenses', 'Other Income', 'Other Revenue', 'Staff Cost', 'Rental Expenses',
                             'Office Expenses.', 'Sales & Promotion',
                             'Management Fees', 'Professional & Legal', 'Depreciation', 'Others - G & A',
                             'Provision for Doubtful debts', 'Material Parts & Consumables - Services']},

    {'value': 'EBITDA', 'filt': ['Logistics Revenue', 'Manpower Revenue', 'Projects Revenue', 'Services Revenue',
                                 'Staff Cost - Logistics', 'Service Cost - Logistics', 'Accommodation - Manpower',
                                 'Staff Cost - Manpower',
                                 'Transportation - Manpower', 'Others - Manpower',
                                 'Material Parts & Consumables - Projects', 'Staff Cost - Projects',
                                 'Maintenance - Projects', 'Others - Projects',
                                 'Other Income', 'Other Revenue', 'Staff Cost', 'Rental Expenses', 'Office Expenses.',
                                 'Sales & Promotion',
                                 'Management Fees', 'Professional & Legal', 'Others - G & A',
                                 'Material Parts & Consumables - Services']}
]

fin_tiles_pct = ['GP %', 'NP %', 'EBITDA %']

time_series_data = {
    'Current Month': 'current_month',
    'Previous Year Same Month': 'previous_year_same_month',
    'YTD Current Year': 'ytd_current_year'
}

graph_legends = {'Logistics Revenue - Clearance': 'Clearance',
                 'Logistics Revenue - Transport': 'Transport',
                 'Logistics Revenue - Freight': 'Freight',
                 'Logistics Revenue - Other': 'Other',
                 'Manpower Revenue': 'Manpower',
                 'Projects Revenue': 'Projects',
                 'Services Revenue': 'Services'}

months = {'01': 'Jan',
          '02': 'Feb',
          '03': 'Mar',
          '04': 'Apr',
          '05': 'May',
          '06': 'Jun',
          '07': 'Jul',
          '08': 'Aug',
          '09': 'Sep',
          '10': 'Oct',
          '11': 'Nov',
          '12': 'Dec',
          'Total': 'Total',
          'first_level': 'Header'}

pl_sort_order = {'Manpower Revenue': 1,
                 'Projects Revenue': 2,
                 'Services Revenue': 3,
                 'Direct Income': 4,
                 'Staff Cost - Manpower': 5,
                 'Transportation - Manpower': 6,
                 'Accommodation - Manpower': 7,
                 'Others - Manpower': 8,
                 'Staff Cost - Projects': 9,
                 'Maintenance - Projects': 10,
                 'Depreciation - Projects': 11,
                 'Material Parts & Consumables - Projects': 12,
                 'Others - Projects': 13,
                 'Cost of Sales': 14,
                 'Gross Proft / Loss': 15,
                 'Gross Proft / Loss %': 16,
                 'Other Revenue': 17,
                 'Indirect Income': 18,
                 'Staff Cost': 19,
                 'Rental Expenses': 20,
                 'Office Expenses.': 21,
                 'Sales & Promotion': 22,
                 'Management Fees': 23,
                 'Professional & Legal': 24,
                 'Depreciation': 25,
                 'Others - G & A': 26,
                 'Provision for Doubtful debts': 27,
                 'Overhead': 28,
                 'Interest Expenses': 29,
                 'Finance Cost': 30,
                 'Net Profit / Loss': 31,
                 'Net Profit / Loss %': 32
                 }

bs_sort_order = {'Property, Plant  & Equipment': 1,
                 'Intangible Assets': 2,
                 'Right of use Asset': 3,
                 'Non Current Assets': 4,
                 'Cash & Cash Equivalents': 5,
                 'Trade Receivables': 6,
                 'Inventory': 7,
                 'Due from Related Parties': 8,
                 'Other Receivable': 9,
                 'Current Assets': 10,
                 'Assets': 11,
                 'Share Capital': 12,
                 'Statutory Reserves': 13,
                 'Retained Earnings': 14,
                 'Equity': 15,
                 'Provisions': 16,
                 'Lease Liabilities': 17,
                 'Non Current Liabilities': 18,
                 'Accounts Payables': 19,
                 'Accruals & Other Payables': 20,
                 'Due to Related Parties': 21,
                 'Current Liabilities': 22,
                 'Liability & Equity': 23}

job_type_exclusions = {'Manpower - Employee Benefits': ['not_joined', 'discharged'],
                       'exclude_list_ot': ['AC-ACCOMODATION', 'Annual Leave', 'Bereavement leave- Local',
                                           'Bereavement leave-Overseas', 'CI-CLIENT INTERVIEW', 'discharged',
                                           'FP-FINGER PRINT', 'Hajj Leave'
                                                              'HO-HEAD OFFICE', 'ME-MOI Exam', 'MM-MOI MEDICAL',
                                           'MT-MOI Training', 'not_joined', 'OF-Off', 'QM-QID MEDICAL', 'SB-STANDBY',
                                           'Sick Leave - FP', 'Sick Leave - HP',
                                           'Sick Leave - UP', 'SL-SICK LEAVE', 'TN-TRAINING', 'Unpaid Leave'],
                       'Manpower - Salaries': ['Annual Leave', 'Bereavement leave- Local', 'Bereavement leave-Overseas',
                                               'discharged', 'not_joined', 'Sick Leave - UP', 'Unpaid Leave'],
                       'exclude_list_fix_bil': ['AC-ACCOMODATION', 'Annual Leave', 'Bereavement leave- Local',
                                                'Bereavement leave-Overseas', 'discharged', 'Hajj Leave', 'not_joined',
                                                'OF-Off', 'PS-PATROLING SUPERVISOR',
                                                'SB-STANDBY', 'Sick Leave - FP', 'Sick Leave - HP', 'Sick Leave - UP',
                                                'SL-SICK LEAVE', 'Unpaid Leave'],
                       'exclude_list_fix_gen': ['not_joined', 'discharged'],
                       'exclude_list_off': ['AC-ACCOMODATION', 'Annual Leave', 'Bereavement leave- Local',
                                            'Bereavement leave-Overseas', 'CI-CLIENT INTERVIEW ', 'discharged',
                                            'FP-FINGER PRINT', 'Hajj Leave'
                                                               'HO-HEAD OFFICE', 'ME-MOI Exam', 'MM-MOI MEDICAL',
                                            'MT-MOI Training', 'not_joined', 'OF-Off', 'QM-QID MEDICAL', 'SB-STANDBY',
                                            'Sick Leave - FP', 'Sick Leave - HP',
                                            'Sick Leave - UP', 'SL-SICK LEAVE', 'TN-TRAINING', 'Unpaid Leave',
                                            'OJ-ON JOB TRAINING', 'PS-PATROLING SUPERVISOR']}

ctc_amount = {'insurance':
                  {'a1': {'adult': 9_146, 'minor': 5_663},
                   'a2': {'adult': 6_243, 'minor': 0},
                   'b': {'adult': 5_898, 'minor': 3_693},
                   'c': {'adult': 2_788, 'minor': 2_182},
                   'd': {'adult': 1_977, 'minor': 0},
                   },
              'rp':
                  {
                      'a1': {'adult': 1_220, 'minor': 500},
                      'a2': {'adult': 1_220, 'minor': 500},
                      'b': {'adult': 1_220, 'minor': 500},
                      'c': {'adult': 1_220, 'minor': 500},
                      'd': {'adult': 1_220, 'minor': 500},
                  }}

related_parties = {'Auto Class Automobiles W.L.L': ['Auto Class Automobiles', 'Auto Class Automobiles W.L.L'],
                   'Elite Facility Management W.L.L': ['Elite Facility Management W.L.L.'],
                   'GAT Middle East W.L.L': ['GAT Middle East'],
                   'Heirs of Nasser Bin Khaled Holding W.L.L': ['Heirs of Nasser Bin Khaled Holding W.L.L',
                                                                'Heirs of Nasser Bin Khalid Holding W.L.L'],
                   'Nasser Bin Khaled & Sons Automobiles W.L.L': ['Nasser Bin Khaled & Sons Automobiles W.L.L',
                                                                  'Nasser Bin Khalid Automobiles W.L.L'],
                   'Nasser Bin Khaled Al-Thani & Sons Holding Company W.L.L': [
                       'Nasser Bin Khaled Al-Thani & Sons Holding Co.',
                       'Nasser Bin Khalid Al-Thani and Sons Holding Company W.L.L - R/P'],
                   'Nasser Bin Khaled and Sons Real Estate Co. W.L.L': [
                       'Nasser Bin Khaled and Sons Real Estate Co. W.L.L',
                       'Nasser Bin Khalid and Sons Real Estate Company WLL'],
                   'Nasser Bin Khaled Tyre Services W.L.L': ['Nasser Bin Khaled Tyre Services W.L.L',
                                                             'Nasser Bin Khaled Tires Services W.L.L.'],
                   'Nasser Bin Khaled Travel & Tourism W.L.L': ['Nasser Bin Khaled Travel & Tourism',
                                                                'Nasser Bin Khalid Travel & Tourism'],
                   'Nasser Bin Nawaf & Partners Holding W.L.L': ['Nasser Bin Nawaf & Partners Holding W.L.L',
                                                                 'NBN Holdings',
                                                                 'Nasser Bin Nawaf and Partners Holding Company W.L.L'],
                   'Nasser Bin Nawaf Logistics W.L.L': ['Nasser Bin Nawaf Logistics W.L.L',
                                                        'Nasser Bin Nawaf Logistics W.L.L.'],
                   'Nasser Bin Nawaf Real Estate W.L.L': ['Nasser Bin Nawaf Real Estate W.L.L',
                                                          'Nasser Bin Nawaf Real Estate WLL'],
                   'Nasser Bin Nawaf Technologies W.L.L': ['Nasser Bin Nawaf Technologies W.L.L.',
                                                           'Nasser Bin Nawaf Techologies W.L.L'],
                   'Q Auto W.L.L': ['Q Auto', 'Q-AUTO W.L.L'],
                   'Qatar Automobiles Company W.L.L': ['Qatar Automobiles Company W.L.L', 'Qatar Automobiles Company'],
                   'AFG College W.L.L': ['AFG College W.L.L'],
                   'Al Waab City W.L.L': ['Al Waab City W.L.L'],
                   'Doha Academy W.L.L': ['Doha  Academy'],
                   'H-Deco Qatar W.L.L': ['H-Deco Qatar W.L.L'],
                   'Nasser Bin Khaled & Sons Projects Promotion Co. W.L.L': [
                       'Nasser Bin Khaled & Sons Projects Promotion Co. W.L.L'],
                   'Nasser Bin Khaled & Sons Trading Company W.L.L': ['Nasser Bin Khaled & Sons Trading Company'],
                   'Nasser Bin Khaled Heavy Equiment W.L.L': ['Nasser Bin Khaled Heavy Equiment WLL'],
                   'Nasser Bin Khaled Medical Equipments W.L.L': ['Nasser Bin Khaled Medical Equipments W.L.L'],
                   'Nasser Bin Khaled Service centers W.L.L': ['Nasser Bin Khaled Service centers W.L.L'],
                   'NBK Powered Sports W.L.L': ['NBK Powered Sports W.L.L'],
                   'NBK Ready Mix W.L.L': ['NBK Ready Mix'],
                   'Hassan Matar S Al-Sowaidi': ['Partners Account - Hassan Matar S Al-Sowaidi'],
                   'Nawaf Nasser Al-Thani': ['Private Office'],
                   'SNC Lavalin ProFac Gulf Management W.L.L': ['SNC Lavalin ProFac Gulf Management'],
                   'Ziebart W.L.L': ['Ziebart'], }

elimination_ledgers = ['Refundable Deposits', 'Advance to Suppliers - PDC', 'PDC Payables',
                       'Other Payable - Security Cheques', 'Refundable Deposits - Security Cheques', 'PDC Receivable']
