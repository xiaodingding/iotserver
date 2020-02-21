# ~*~ coding: utf-8 ~*~
#
'''
from ops.utils import run_AdHoc


def test_admin_user_connective_manual(asset):
    if not isinstance(asset, list):
        asset = [asset]
    task_tuple = (
        ('ping', ''),
    )
    summary, _ = run_AdHoc(task_tuple, asset, record=False)
    if len(summary['failed']) != 0:
        return False
    else:
        return True

'''

from .models.datapoint import DataPoint
from .models.group import DeviceGroup
from .models.datatemplet import DataTemplet
from .models.device import Device
from .models.data import Data

def device_point_query(device):
    if not isinstance(device, Device):
        if isinstance(device, int):
            device = Device.object.filter(id=device)
            templet = device.datatemplet.all()[:1]
            dtpoint = None

            if (len(templet) < 1):
                return None
            else:
                dtpoint = DataPoint.objects.filter(templet=templet).all()
                return dtpoint
        else:
            print("null: %s" % device)
            return None
    else:
        templet = device.datatemplet.all()[:1]
        dtpoint = None

        if (len(templet) < 1):
            return None
        else:
            dtpoint = DataPoint.objects.filter(templet=templet).all()
            return dtpoint