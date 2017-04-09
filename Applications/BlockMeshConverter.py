from optparse import OptionGroup
from PyFoam.Applications.PyFoamApplication import PyFoamApplication
from PyFoam.Basics.RestructuredTextHelper import RestructuredTextHelper
from PyFoam.Basics.FoamOptionParser import Subcommand
from RunDictionary.BlockMesh2D import BlockMesh2D
from PyFoam.Basics.DataStructures import *
from os import path
import sys,re
from PyFoam.ThirdParty.six import print_


class BlockMeshConverter(PyFoamApplication):
    def __init__(self,
                args=None,
                 **kwargs):
        description="""\
This utility extrudes  2D blockMeshDict to 3DblockMeshDict appropriate for OpenFOAM blockMesh utility. Application requires a blockMesh2D file representing
        the two dimensional domain and converts it to 3D domain by extruding or rotating the domain.
                """
        PyFoamApplication.__init__(self,
                                   args=args,
                                   description=description,
                                   usage="%prog <blockMeshDict2D>",
                                   changeVersion=False,
                                   nr=1,
                                   interspersed=True,
                                   subcommands=False,
                                   **kwargs)
    def addOptions(self):
        how=OptionGroup(self.parser,
                         "How",
                         "Extrusion type of 2D blockMesh")
        self.parser.add_option_group(how)
        how.add_option("--extrude",
                        action="store_true",
                        dest="extrude",
                        default=False,
                        help="Extrude 2D blockMesh in z direction")


        how.add_option("--x-rotate",
                        action="store_true",
                        dest="rotatex",
                        default=False,
                        help="Rotates 2D blockMesh around x axis")

        how.add_option("--y-rotate",
                        action="store_true",
                        dest="rotatey",
                        default=False,
                        help="Rotates 2D blockMesh around y axis")

        value=OptionGroup(self.parser,
                          "Value",
                          "Values of extrusion")
        self.parser.add_option_group(value)
        value.add_option("--distance-front",
                         action="store",
                         type="float",
                         default=0,
                         dest="frontvalue",
                         help="The value of extrusion in positive z-direction")
        value.add_option("--distance-back",
                         action="store",
                         type="float",
                         default=0,
                         dest="backvalue",
                         help="The value of extrusion in negative z-direction")
        value.add_option("--angle-front",
                         action="store",
                         type="float",
                         default=2.5,
                         dest="frontangle",
                         help="Rotation angle in positive z-direction")
        value.add_option("--angle-back",
                         action="store",
                         type="float",
                         default=2.5,
                         dest="backangle",
                         help="Rotation angle in negative z-direction")
        value.add_option("--division",
                         action="store",
                         type="int",
                         default=1,
                         dest="division",
                         help="Number of divisions")

        output=OptionGroup(self.parser,
                          "Output",
                          "Specifying where the result goes")
        self.parser.add_option_group(output)
        output.add_option("--destination",
                         action="store",
                         default="blockMeshDict",
                         dest="destination",
                         help="Enter the name of converted blockMeshDict. Default value: %default")
        output.add_option("--print-to-stdout",
                        action="store_true",
                        dest="printToStdout",
                        default=False,
                        help="Instead of writing to file print to the console")

    def run(self):
        # print_(path.dirname(self.parser.getArgs()[0]))
        bmFile=self.parser.getArgs()[0]
        if not path.exists(bmFile):
            self.error(bmFile,"not found")
        outbmFile=self.opts.destination
        if self.opts.extrude:
            mesh=BlockMesh2D(bmFile,
                             "EXTRUDE",
                             -abs(self.opts.backvalue),
                             abs(self.opts.frontvalue),
                             abs(self.opts.division)
            )
        elif self.opts.rotatex:
            mesh=BlockMesh2D(bmFile,
                             "ROTATEX",
                             -abs(self.opts.backangle),
                             abs(self.opts.frontangle),
                             abs(self.opts.division)
            )
        elif self.opts.rotatey:
            mesh=BlockMesh2D(bmFile,
                             "ROTATEY",
                             -abs(self.opts.backangle),
                             abs(self.opts.frontangle),
                             abs(self.opts.division)
            )
        else:
            self.error("No transformation specified: --extrude, --rotate-x or --rotate-y")

        if self.opts.printToStdout:
            print_(mesh.convert2DBlockMesh())
        else:
            open(outbmFile,"w").write(mesh.convert2DBlockMesh())
