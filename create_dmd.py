# Add Visum Python environment to system path
import sys
sys.path.append(r"C:\Program Files\PTV Vision\PTV Visum 2021\Exe\Python37Modules\Lib\site-packages")

import os
import wx
import logging
import VisumPy.helpers as VPH
import dialogs as dlg


def start_logging():
    logger = logging.getLogger()
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def create_demandmodel(demandmodels):
    #! demandmodels needs to be a list of tuples: [(name, code),...] demand model codes
    for name, code in demandmodels:
        d = Visum.Net.AddDemandModel(code, 0)
        d.SetAttValue('NAME', name)

def create_actpairs(actpairs):
    #! actpairs needs to be a list of tuples: [(name, code, demand_model_code),...]
    for name, code, dm_code in actpairs:
        a = Visum.Net.AddActPair(code, dm_code) #! Check that other parameters (O_Activity & D_Activity) aren't needed
        a.SetAttValue('NAME', name)

def create_persongroups(persongroups):
    #! persongroups needs to be a list of tuples: [(name, code, demand_model_code),...]
    for name, code, dm_code in persongroups:
        p = Visum.Net.AddPersonGroup(code, dm_code)
        p.SetAttValue('NAME', name)

def create_dstrata(dstrata):
    #! dstrata needs to be a list of tuples: [(name, code, demand_model_code, actpair, [persongroups]),...]
    for name, code, dm_code, actpair, persongroups in dstrata:
        pgroups = ','.join(persongroups)
        p = Visum.Net.AddPersonGroup(code, dm_code, pgroups, actpair)
        p.SetAttValue('NAME', name)

def create_modes(modes):


def create_tsys():

def create_dsegs():


def input_actpairs():
    NTEM_actpairs = [("HB Work","HBW"),
                     ("HB Employers Business (EB)","HBEB"),
                     ("HB Education","HBEd"),
                     ("HB Shopping","HBShop"),
                     ("HB Personal Business (PB)","HBPB"),
                     ("HB Recreation / Social","HBRec"),
                     ("HB Visiting friends & relatives","HBVFR"),
                     ("HB Holiday / Day trip","HBHol"),
                     ("NHB Work","NHBW"),
                     ("NHB Employers Business (EB)","NHBEB"),
                     ("NHB Education","NHBEd"),
                     ("NHB Shopping","NHBShop"),
                     ("NHB Personal Business (PB)","NHBPB"),
                     ("NHB Recreation / Social","NHBRec"),
                     ("NHB Holiday / Day trip","NHBHol")]

    # First get number of activity pairs required by the user
    try:
        num_actpairs = int(dlg.text_entry_dlg("Please enter the number of activity pairs:", 'Activity Pairs'))
    except ValueError:
        wx.MessageBox("Please enter an integer.",'Error', wx.ERROR)
        num_actpairs = int(dlg.text_entry_dlg("Please enter the number of activity pairs:", 'Activity Pairs'))
    finally:
        wx.MessageBox("Invalid input - model generation terminated.",'Error', wx.ERROR)
        exit(0)
    
    # Next, user adds names and codes of activity pairs
    ap_dlg = dlg.user_data_input(None, 'Enter Activity Pair Data', ['Name', 'Code'])
    if ap_dlg.ShowModal() == wx.ID_OK:
        # OK: return the activity pairs data
        act_pairs = ap_dlg.get_value()
        ap_dlg.Destroy()
    else:
        # Cancel: Close dialog and exit
        ap_dlg.Destroy()
        exit(0)
    
    # TODO Add mapping to NTEM purposes for data import

    return act_pairs

    def input_persongroups(act_pairs):

        # First get number of person group sets required by the user
        try:
            num_persongroupsets = int(dlg.text_entry_dlg("Please enter the number of person group sets.\n(The number of different segmentations required; if the same structure is to be used for all activity pairs enter 1):", 'Person Group Sets'))
        except ValueError:
            wx.MessageBox("Please enter an integer.",'Error', wx.ERROR)
            num_persongroupsets = int(dlg.text_entry_dlg("Please enter the number of person group sets.\n(The number of different segmentations required; if the same structure is to be used for all activity pairs enter 1):", 'Person Group Sets'))
        finally:
            wx.MessageBox("Invalid input - model generation terminated.",'Error', wx.ERROR)
            exit(0)

        # For each set, define the number of person groups 
        # Next, user adds names and codes of activity pairs
        pgs_dlg = dlg.user_data_input(None, 'Enter Person Group Numbers', ['Person Group Set', 'Number of Person Groups'], table=zip(range(1,num_persongroupsets+1), ['']*num_persongroupsets))
        if pgs_dlg.ShowModal() == wx.ID_OK:
            # OK: return the person group set data
            persongroupsets = pgs_dlg.get_value()
            pgs_dlg.Destroy()
        else:
            # Cancel: Close dialog and exit
            pgs_dlg.Destroy()
            exit(0)

        # For each set define the person groups
        persongroups = []
        for i in range(num_persongroupsets):
            pg_dlg = dlg.user_data_input(None, f'Enter Person Group Set {i+1} data', ['No', 'Name', 'Code'], table=zip(range(1,persongroupsets[i][1]+1), ['']*persongroupsets[i][1], ['']*persongroupsets[i][1]))
            if pg_dlg.ShowModal() == wx.ID_OK:
                # OK: return the person gorup data
                persongroups.append(pg_dlg.get_value())
                pg_dlg.Destroy()
            else:
                # Cancel: Close dialog and exit
                pg_dlg.Destroy()
                exit(0)

        if num_persongroupsets > 1:
            # For each activity pair, define the person group set
            ap_pg_dlg = dlg.user_data_input(None, f'Enter Activity Pair/Person Group Set Correspondence', ['No', 'Activity Pair', 'PersonGroup Set'], table=zip(range(1, len(act_pairs)+1), [y for x, y in act_pairs], ['']*len(act_pairs)))
            if ap_pg_dlg.ShowModal() == wx.ID_OK:
                # OK: return the activity pairs / person group set mapping
                ap_pgs = ap_pg_dlg.get_value()
                ap_pg_dlg.Destroy()
            else:
                # Cancel: Close dialog and exit
                pg_dlg.Destroy()
                exit(0)
        else:
            ap_pgs = [(x[0],1) for x in act_pairs]

        all_persongroups = []
        for p in persongroups:
            for x, y, z in p:
                all_persongroups.append((y, z))

        return ap_pgs, all_persongroups


# TODO Add ability to have >1 demand model (for different structures)
# TODO Add opening / saving selections

def input_time_periods():
    try:
        num_timeperiods = int(dlg.text_entry_dlg("Please enter the number of Time Periods:", 'Time Periods'))
    except ValueError:
        wx.MessageBox("Please enter an integer.",'Error', wx.ERROR)
        num_timeperiods = int(dlg.text_entry_dlg("Please enter the number of Time Periods:", 'Time Periods'))
    finally:
        wx.MessageBox("Invalid input - model generation terminated.",'Error', wx.ERROR)
        exit(0)

    tp_dlg = dlg.user_data_input(None, f'Enter Time Period data', ['No', 'Code'], table=zip(range(1,num_timeperiods+1), ['']*num_timeperiods))
    if tp_dlg.ShowModal() == wx.ID_OK:
        # OK: return the person gorup data
        timeperiods = [x[1] for x in tp_dlg.get_value()]
        tp_dlg.Destroy()
    else:
        # Cancel: Close dialog and exit
        tp_dlg.Destroy()
        exit(0)
    return timeperiods

def input_tsys(modes):
    if modes == 'full':
        tsys = [('CB', 'Car Business', 'PrT', 1),
                ('CC', 'Car Commute', 'PrT', 1),
                ('CO', 'Car Other', 'PrT', 1),
                ('BB', 'Bus Business', 'PuT', 0),
                ('BC', 'Bus Commute', 'PuT', 0),
                ('BO', 'Bus Other', 'PuT', 0),
                ('RB', 'Rail Business', 'PuT', 0),
                ('RC', 'Rail Commute', 'PuT', 0),
                ('RO', 'Rail Other', 'PuT', 0),
                ('HGV', 'Heavy Good Vehicles', 'PrT', 2.5),
                ('LGV', 'Light Goods Vehicles', 'PrT', 1),
                ('W', 'PuT_Walk', 'PuTWalk', 0),
                ('Cycle', 'Cycle', 'PuT', 0),
                ('Walk', 'Walk', 'PuT', 0)]
    elif modes == 'agg_pt' or modes == 'agg':
        tsys = [('CB', 'Car Business', 'PrT', 1),
                ('CC', 'Car Commute', 'PrT', 1),
                ('CO', 'Car Other', 'PrT', 1),
                ('PTB', 'Public Transport Business', 'PuT', 0),
                ('PTC', 'Public Transport Commute', 'PuT', 0),
                ('PTO', 'Public Transport Other', 'PuT', 0),
                ('HGV', 'Heavy Good Vehicles', 'PrT', 2.5),
                ('LGV', 'Light Goods Vehicles', 'PrT', 1),
                ('W', 'PuT_Walk', 'PuTWalk', 0),
                ('Cycle', 'Cycle', 'PuT', 0),
                ('Walk', 'Walk', 'PuT', 0)]
    return tsys



def input_modes(timeperiods):
    # Options for a few different mode setups - could expand with more options for the user
    full = [('CarD', 'Car driver'),
            ('CarP', 'Car Passenger'), 
            ('Bus', 'Bus'), 
            ('Rail', 'Rail'), 
            ('Cycle', 'Cycle'), 
            ('Walk', 'Walk')]
    agg_pt = [('CarD', 'Car driver'), 
              ('CarP', 'Car Passenger'),
              ('PT', 'Public Transport'),
              ('Cycle', 'Cycle'), 
              ('Walk', 'Walk')]
    agg = [('Car', 'Car'), ('PT', 'Public Transport'), ('Active', 'Active')]