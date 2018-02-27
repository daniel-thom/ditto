# -*- coding: utf-8 -*-

"""
test_writer
----------------------------------

Tests for `ditto` module writers
"""
import logging
import os

import pytest

from tests import outdir
from tests.test_session import manage_outdir

logger = logging.getLogger(__name__)

writer_dir = os.path.join(outdir,'test_writer')


@pytest.fixture(scope='module',autouse=True)
def create_writer_dir(manage_outdir):
    assert os.path.exists(outdir)
    assert not os.path.exists(writer_dir)
    os.mkdir(writer_dir)

@pytest.fixture(scope="function")
def change_to_writer_dir():
    curdir = os.getcwd()
    os.chdir(writer_dir)
    yield
    os.chdir(curdir)

def test_opendss_writer(change_to_writer_dir):
    from ditto.writers.opendss.write import Writer
    from ditto.models.node import Node
    from ditto.models.line import Line
    from ditto.models.load import Load
    from ditto.models.regulator import Regulator
    from ditto.models.wire import Wire
    from ditto.models.capacitor import Capacitor
    from ditto.models.powertransformer import PowerTransformer
    from ditto.models.winding import Winding
    #from ditto.model import Model
    from ditto.store import Store
    from ditto.models.storage import Storage 
    from ditto.models.phase_storage import PhaseStorage
    from ditto.models.base import Unicode
    from ditto.models.power_source import PowerSource

    m = Store()
    node1 = Node(m, name='n1')
    node2 = Node(m, name='n2')
    node3 = Node(m, name='n3')
    wirea = Wire(m, gmr=1.3, X=2, Y = 20)
    wiren = Wire(m, gmr=1.2, X=2, Y = 20)
    line1 = Line(m, name='l1', wires=[wirea, wiren])
    load1 = Load(m, name='load1', p=5400, q=2615.3394)

    winding1 = Winding(m, connecting_element='n2', connection_type='W', num_phases=3, nominal_voltage=12.47, rated_power=25, tap_percentage=1)
    winding2 = Winding(m, connecting_element='l1', connection_type='W', num_phases=3, nominal_voltage=6.16, rated_power=25, tap_percentage=1.2)
    transformer1 = PowerTransformer(m, name='t1', resistance=0.5, reactance=6, num_phases=3, windings=[winding1, winding2]) 
    reg1 = Regulator(m, name='t1_reg', connected_transformer='t1', connected_winding=2, pt_ratio=60, delay=2)
    cap1 = Capacitor(m, name='cap1', connecting_element='n2', num_phases=3, nominal_voltage=7.2, var=300, connection_type='Y')
    print(line1.impedance_matrix)

    #Storage testing
    phase_storage_A = PhaseStorage(m, phase='A', p=15.0, q=5.0)
    phase_storage_B = PhaseStorage(m, phase='B', p=16.0, q=6.0)
    storage = Storage(m, name='store1', connecting_element='n3', nominal_voltage=12470.0, rated_power=10000.0, rated_kWh=100.0, stored_kWh=75.5, 
                         reserve=20.0, discharge_rate=25.0, charge_rate=18.7, charging_efficiency=15.3, discharging_efficiency=22.0, resistance=20, 
                         reactance=10, model_=1, phase_storages=[phase_storage_A, phase_storage_B] )

    #PV systems testing
    PV_system = PowerSource(m, name='PV1', is_sourcebus=0, nominal_voltage=12470, phases=[Unicode('A'),Unicode('C')], rated_power=20000.0, connection_type='D',
                               cutout_percent=30.0, cutin_percent=15.3, resistance=14.0, reactance=5.2, v_max_pu=100, v_min_pu=60, power_factor=.9)

    writer = Writer()
    writer.write_wiredata(m)
    writer.write_linegeometry(m)
    writer.write_linecodes(m)
    writer.write_storages(m)
    writer.write_PVs(m)
    writer.write_lines(m,linecodes=False)
    writer.write_loads(m)
    writer.write_transformers(m)
    writer.write_regulators(m)
    writer.write_capacitors(m)
    