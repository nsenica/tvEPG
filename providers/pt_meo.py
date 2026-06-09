# -*- coding: utf-8 -*-

import providers.pt_meo_go

def getEPG(list, nr_days):
    return providers.pt_meo_go.getEPG(list, nr_days)
