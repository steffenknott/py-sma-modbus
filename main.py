import argparse, sys

from modbus import Modbus
from sma import add_tripower_register, add_sbstorage_register, add_sbxx_1av_41_register
from logger import TableLogger

parser = argparse.ArgumentParser(description='Gather data of your sma inverter')
parser.add_argument('registers',
                    type=int,
                    nargs='+',
                    help='list of register numbers')
parser.add_argument('-d', '--daemon',
                    action='store_true',
                    help='keep polling')
parser.add_argument('-i', '--interval',
                    type=int,
                    default=1,
                    help='time between polls')
parser.add_argument('-l', '--list',
                    action='store_true',
                    help='list all registers')
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='log results')
parser.add_argument('-g', '--enablegui',
                    action='store_true',
                    help='enable ncurses gui')
parser.add_argument('-a', '--address',
                    type=str,
                    required=True,
                    help='modbus ip')
parser.add_argument('-p', '--port',
                    type=int,
                    required=True,
                    help='modbus port')
parser.add_argument('-u', '--unit',
                    type=int,
                    required=True,
                    help='modbus unit')
parser.add_argument('-t', '--type',
                    type=str,
                    required=True,
                    help='inverter type')

args = parser.parse_args()

wr = Modbus(args, logger=TableLogger())

if args.type == "tripower":
    add_tripower_register(wr)
elif args.type == "sbstorage":
    add_sbstorage_register(wr)
elif args.type == "sbxx-1av-41":
    add_sbxx_1av_41_register(wr)
else:
    sys.exit("Unknown inverter type.")

if args.list:
    wr.list_available_registers()
else:
    for register in args.registers:
        wr.poll_register(register)
    wr.start()
