"""
@brief Example code to run the nightly ISR's 'Flat Field Correction Stage'.

@author Nicole M. Silvestri
        University of Washington
        nms@astro.washington.edu

 file created Tue Nov 25, 2008 

@file

"""

if __name__ == "__main__":
    import eups
    import os
    import lsst.afw.image as afwImage
    import lsst.daf.base as dafBase
    import lsst.pex.logging as pexLog
    import lsst.pex.policy as pexPolicy
    import lsst.ip.isr.FlatFieldCorrection as ipIsrFlat 

    pexLog.Trace.setVerbosity("lsst.ip.isr", 4)
    
    dataDir = eups.productDir("afwdata")
    if not dataDir:
        raise RuntimeError("Must set up afwdata to run this program.")
    isrDir = eups.productDir("ip_isr")
    if not isrDir:
        raise RuntimeError("Must set up ip_isr to run this program.")
    
    chunkExposureInPath = os.path.join(dataDir, "linearStageTestExposure_1")
    masterChunkExposureInPath = os.path.join(dataDir, "CFHT", "D4", "05Am05.flat.0.36.00_1_img.fits")
    isrPolicyPath = os.path.join(isrDir, "pipeline", "isrPolicy.paf")
    chunkExposureOutPath = os.path.join(dataDir, "FlatStageTestExposure_1")
    
    memId0 = dafBase.Citizen_getNextMemId()

    chunkExposure = afwImage.ExposureD()
    chunkExposure.readFits(chunkExposureInPath)
    masterChunkExposure = afwImage.ExposureD()
    masterChunkExposure.readFits(masterChunkExposureInPath)

    isrPolicy = pexPolicy.Policy.createPolicy(isrPolicyPath)
    
    ipIsrFlat.flatFieldCorrection(chunkExposure, masterChunkExposure, isrPolicy)

    pexLog.Trace("lsst.ip.isr.flatFieldCorrection", 4, "Writing chunkExposure to %s [_img|var|msk.fits]" % (chunkExposureOutPath,))
    chunkExposure.writeFits(chunkExposureOutPath)
    
    # check for memory leaks
    if dafBase.Citizen_census(0, memId0) != 0:
        print dafBase.Citizen_census(0, memId0), "Objects leaked:"
        print dafBase.Citizen_census(dafBase.cout, memId0)
