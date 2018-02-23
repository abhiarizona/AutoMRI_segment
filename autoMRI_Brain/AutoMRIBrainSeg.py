from __main__ import vtk, qt, ctk, slicer
import SimpleITK as sitk
import sitkUtils as su
import numpy as np
import AutoMRIBrainSegWizard 
from EditorLib import EditUtil
#from FastMarching_threshold_slicer import FastMarching_threshold_slicer

class AutoMRIBrainSeg:
    def __init__(self, parent):
        parent.title = """ Brain MRI Auto-Segmentation """
        parent.categories = ["""Examples"""]
        parent.contributors = ["Matthew Scarpelli","Stephen Yip","Lingdao Sha"]
        parent.helpText = """ To be filled """
        parent.acknowledgementText = """ To be filled """
        self.parent = parent

class AutoMRIBrainSegWidget:
    def __init__(self, parent=None):
        if not parent:
            self.parent = slicer.qMRMLWidget()
            self.parent.setLayout(qt.QVBoxLayout())
            self.parent.setMRMLScene(slicer.mrmlScene)
        else:
            self.parent = parent
        self.layout = self.parent.layout()
        if not parent:
			self.setup()
			self.parent.show()

    def setup(self):
        #Collapsible button
        autoMRIBrainCollapsibleButton = ctk.ctkCollapsibleButton()
        autoMRIBrainCollapsibleButton.text = "Collapsible button for Brain MRI auto-segmentation"
        self.layout.addWidget(autoMRIBrainCollapsibleButton)

        #Layout within the collapsible button
        autoMRIBrainFormLayout = qt.QFormLayout(autoMRIBrainCollapsibleButton)

        #Load Brain MRI image button
        # loadMRIBrainButton = qt.QPushButton("Load Brain MRI image and add ROI annotation")
        # loadMRIBrainButton.toolTip = "Click to load Brain MRI image and annotate tumor center location"
        # autoMRIBrainFormLayout.addWidget(loadMRIBrainButton)
        # loadMRIBrainButton.connect('clicked(bool)', self.onloadMRIBrainButtonClicked)

        #Load Brain MRI T1 image button
        loadMRIT1Button = qt.QPushButton("Load Brain MRI T1 image")
        loadMRIT1Button.toolTip = "Click to load Brain MRI T1 image and annotate tumor center location"
        # autoMRIBrainFormLayout.addWidget(loadMRIT1Button)
        loadMRIT1Button.connect('clicked(bool)', self.onloadMRIT1ButtonClicked)

        #Load Brain MRI T2 FLAIR
        loadMRIFLAIRButton = qt.QPushButton("Load Brain MRI T2 FLAIR image")
        loadMRIFLAIRButton.toolTip = "Click to load Brain MRI image and annotate tumor center location"
        # autoMRIBrainFormLayout.addWidget(loadMRIFLAIRButton)
        loadMRIFLAIRButton.connect('clicked(bool)', self.onloadMRIFLAIRButtonClicked)

        loadMRIBrainButtons = qt.QGridLayout()
        loadMRIBrainButtons.addWidget(loadMRIT1Button, 0,0)
        loadMRIBrainButtons.addWidget(loadMRIFLAIRButton, 0,1)
        autoMRIBrainFormLayout.addRow(loadMRIBrainButtons)

        #load ATLAS
        loadATLASButton = qt.QPushButton("Load ALTAS Images")
        loadATLASlabelButton = qt.QPushButton("Load ALTAS Labels")
        loadATLASButton.connect('clicked(bool)', self.onloadATLASButtonClicked)
        loadATLASlabelButton.connect('clicked(bool)', self.onloadATLASlabelButtonClicked)
        autoMRIBrainFormLayout.addWidget(loadATLASButton)
        autoMRIBrainFormLayout.addWidget(loadATLASlabelButton)

        # Segment T1 
        SegT1Button = qt.QPushButton("Segment T1")
        SegT1Button.toolTip = "Click this button to segment tumor if loaded image is T1."
        SegT1Button.connect('clicked(bool)', self.onloadSegT1ButtonClicked)
        # autoMRIBrainFormLayout.addWidget(loadSegT1Button)
        #Segment FLAIR
        SegFLAIRButton = qt.QPushButton("Segment FLAIR")
        SegFLAIRButton.toolTip = "Click this button to segment tumor if loaded image is FLAIR"
        SegFLAIRButton.connect('clicked(bool)', self.onloadSegFLAIRButtonClicked)
        #Buttons to form
        segMRIBrainButtons = qt.QGridLayout()
        segMRIBrainButtons.addWidget(SegT1Button, 0,0)
        segMRIBrainButtons.addWidget(SegFLAIRButton, 0,1)
        autoMRIBrainFormLayout.addRow(segMRIBrainButtons)


        ##### Ajust value for volume to keep ##########
        ##########################################
#        sigmalabel = qt.QLabel()
#        sigmalabel.setText("Ajust ROI size value for better segmentation (1-10)")
#        autoMRIBrainFormLayout.addWidget(sigmalabel)
#        sigmaSlider = qt.QSlider(qt.Qt.Horizontal)
#        sigmaSlider.toolTip = "Slide to change threshold value"
#        sigmaSlider.setMinimum(1)
#        sigmaSlider.setMaximum(10)
#        sigmaSlider.setValue(1)
#        sigmaSlider.setTickPosition(qt.QSlider.TicksBelow)
#        sigmaSlider.setTickInterval(1)
#        self.sigmaSlider = sigmaSlider
#        #label for ticks
#        sigmavalues = qt.QGridLayout()
#        r1 = qt.QLabel("1")
#        # r2 = qt.QLabel("3")
#        # r3 = qt.QLabel("5")
#        # r4 = qt.QLabel("7")
#        # r5 = qt.QLabel("9")
#        sigmavalues.addWidget(sigmaSlider, 0,0,1,5)
#        sigmavalues.addWidget(r1,1,0,1,1)
#        # sigmavalues.addWidget(r2,1,1,1,1)
#        # sigmavalues.addWidget(r3,1,2,1,1)
#        # sigmavalues.addWidget(r4,1,3,1,1)
#        # sigmavalues.addWidget(r5,1,4,1,1)
#        #Apply the changes
#        sigmaApplyButton = qt.QPushButton("Apply")
#        sigmaApplyButton.toolTip = "Click to apply new sigma value"
#        sigmavalues.addWidget(sigmaApplyButton, 0,5,2,1)
#        sigmaApplyButton.connect('clicked(bool)', self.changesApplyButtonClicked)
#        autoMRIBrainFormLayout.addRow(sigmavalues)
#        # Add vertical spacer
#        self.layout.addStretch(1)


        #ATLAS directories
        # self.atlas_T1_dir = '/Users/lingdao.sha/Documents/Images/Radiology/Brain_MRI_auto/Brain/mni_icbm152_nlin_sym_09a/mni_icbm152_t1_tal_nlin_sym_09a.nii'
        # self.atlas_label_T1_dir = '/Users/lingdao.sha/Documents/Images/Radiology/Brain_MRI_auto/Brain/mni_icbm152_nlin_sym_09a/mni_icbm152_t1_tal_nlin_sym_09a_mask.nii'

        ### Parameters for tweaking ###
        # Elongation threshold (0 = perfect sphere)
        self.elong_thresh = -1 #  default = 0.25; switch to -1 to remove threshold altogether (may be needed in cases where algorithm gives nans or segmented tumor region is not correct)
        # Segmentation to select when refining segmentation
        self.seg_number = 1 # 1 (default) corresponds to largest volume, 2 corresponds to second largest volume, etc. This may need to be changed if eyes are getting segmented instead of tumor
        # change which thresholded segment to keep during t1p segmentation
        self.lowIntEnhance = 0 # 0 (default) takes highest intensity region; 1 takes second highest intensity region
        ### End tweak parameters ###

        # register and resample FLAIR to T1p and perform skull stripping
        self.registerSkullStripImages = 1 # 1 yes; 0 load registered/resampled and sull stripped images from file

        # Output file names
        self.name_T1p_label = 'T1p_label.nrrd'
        self.name_T1p_image = 'T1p_image.nrrd'

        # Output file names
        self.name_FLAIR_label = 'FLAIR_label.nrrd'
        self.name_FLAIR_image = 'FLAIR_image.nrrd'

        # volume thresholds for FLAIR segmented tumors (derived through empiracal results)
        self.volume_FLAIR_lower_threshold = 3000  # Regions with volumes less than this was never the tumor
        self.volume_FLAIR_upper_threshold = 185000  # Regions with volumes greater than this always included many (non-tumor) regions of the brain

    def onloadATLASButtonClicked(self):
        w = qt.QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Select ATLAS Images")
        self.atlas_T1_dir = str(qt.QFileDialog.getOpenFileName(w, 'Open File', '/Documents/'))
        print('ATLAS Images Loaded!')
        

    def onloadATLASlabelButtonClicked(self):
        w = qt.QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Select ATLAS Labels")
        self.atlas_label_T1_dir = str(qt.QFileDialog.getOpenFileName(w, 'Open File', '/Documents/'))
        print('ALTAS Labels Loaded!')

    def onloadMRIT1ButtonClicked(self):
        # widge to load file
        w = qt.QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Select MRI T1 Image")
        self.T1_image_path = qt.QFileDialog.getOpenFileName(w, 'Open File', '/')
        self.T1_path = str('/'.join(self.T1_image_path.split('/')[0:-1]))+'/'

        lm = slicer.app.layoutManager()
        lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
        view = lm.threeDWidget(0).threeDView()
        viewNode = view.mrmlViewNode()

        viewNode.SetBackgroundColor((0,0,0))
        viewNode.SetBackgroundColor2((0,0,0))
        viewNode.SetAxisLabelsVisible(0)
        viewNode.SetBoxVisible(0)
        self.view = view

        # if image_path is not None:
        #   self.image_loaded = True
        load, image = slicer.util.loadVolume(self.T1_image_path, returnNode=True)        

    def onloadSegT1ButtonClicked(self):
        img_T1 = sitk.ReadImage(str(self.T1_image_path), sitk.sitkFloat32)

        # Read in ATLAS
#        atlas_T1 = sitk.ReadImage(self.atlas_T1_dir, sitk.sitkFloat32)
        labelatlas_T1 = sitk.ReadImage(self.atlas_label_T1_dir, sitk.sitkUInt8)
        
       
        msk = sitk.MaskImageFilter()
        img_T1brain=msk.Execute(img_T1,labelatlas_T1>0 )
        
        # Filter T1 image
        blurFilter = sitk.CurvatureFlowImageFilter()
        blurFilter.SetNumberOfIterations(5)
        blurFilter.SetTimeStep(0.1)
        blurredT1=blurFilter.Execute(img_T1brain)


        # Perform thresholding
        otsu_filter = sitk.OtsuMultipleThresholdsImageFilter()
        otsu_filter.SetNumberOfThresholds(2)
        otsu_filter.Execute(blurredT1)
        thresholdsT1 = otsu_filter.GetThresholds()
        print('Thresholds for T1 segmentation = ', thresholdsT1)

        if self.lowIntEnhance == 1:
            segT1_upper = blurredT1 > thresholdsT1[0] 
            segT1_lower = blurredT1 < thresholdsT1[1]
            segT1p_raw = segT1_lower * segT1_upper
        else:
            segT1p_raw = blurredT1 > thresholdsT1[1]
            
        vectorRadius = (10, 10, 5)
        kernel = sitk.sitkBall
        segT1p_raw = sitk.BinaryMorphologicalClosing(segT1p_raw,
                                                     vectorRadius,
                                                     kernel)

        # Refine T1p segmentation
        # Find largest most spherical region in tumor segmentation
#        segT1p, tumor_volume = AutoMRIBrainSegWizard.MRIBrainSegmentor().sphereFinder(segT1p_raw, self.elong_thresh, self.seg_number)
#        segT1p.CopyInformation(img_T1brain)
        # start expt
#        seed = (159,141,9)
#        seg = sitk.Image(blurredT1.GetSize(), sitk.sitkUInt8)
#        seg.CopyInformation(blurredT1)
#        seg[seed] = 1

        # confidence connected it's working
#        segT1p = sitk.ConfidenceConnected(blurredT1, seedList=[seed],
#                                          numberOfIterations=10,
#                                          multiplier=1.65,
#                                          initialNeighborhoodRadius=1,
#                                          replaceValue=1)
#        vectorRadius = (10, 10, 5)
#        kernel = sitk.sitkBall
#        segT1p = sitk.BinaryMorphologicalClosing(segT1p,
#                                                 vectorRadius,
#                                                 kernel)
        segT1p = segT1p_raw
        #print('mean value', mean1)
        nda = sitk.GetArrayFromImage(segT1p)
        white_pix = np.count_nonzero(nda)
        
        print('Number of white pixels:', white_pix)
#        segT1p = sitk.VectorConfidenceConnected(int(blurredT1), seedList=[seed],
#                                             numberOfIterations=1,
#                                             multiplier=2.5,
#                                             initialNeighborhoodRadius=1)
        
        # fill holes
        holefill=sitk.VotingBinaryIterativeHoleFillingImageFilter() 
        holefill.SetMaximumNumberOfIterations(5)
        segTumorbulk=holefill.Execute(sitk.Cast(segT1p>0,sitk.sitkUInt8))

        sitk.WriteImage(segTumorbulk, self.T1_path + self.name_T1p_label)
        T1p_label = slicer.util.loadVolume(self.T1_path + self.name_T1p_label, properties={'labelmap':True}, returnNode=True)

        labelname = 'T1p_label';
        labelNode = slicer.util.getNode(pattern=labelname)
        self.labelNode = labelNode
        self.auto3DGen()


    def auto3DGen(self):
        labelNodeDisplay = self.labelNode.GetDisplayNode()
        labelNodeDisplay.SetAndObserveColorNodeID('vtkMRMLColorTableNodeFileGenericColors.txt')
        self.labelNode.SetAndObserveDisplayNodeID(labelNodeDisplay.GetID())

        tm = slicer.modules.models.mrmlScene().GetNodesByName('Model_1_1')
        for i in tm:
            slicer.modules.models.mrmlScene().RemoveNode(i)

        modelHNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelHierarchyNode')
        modelHNode.SetName('TumorModel')
        modelHNode = slicer.mrmlScene.AddNode(modelHNode)
        parameters = {}
        parameters["InputVolume"] = self.labelNode
        parameters['ModelSceneFile'] = modelHNode.GetID()
        parameters['Smooth'] = 60
        modelmaker = slicer.modules.modelmaker
        slicer.cli.run(modelmaker, None, parameters, wait_for_completion = True)
        self.view.resetFocalPoint()



    def onloadMRIFLAIRButtonClicked(self):
        # widge to load file
        w = qt.QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Select MRI FLAIR Image")
        self.FLAIR_image_path = qt.QFileDialog.getOpenFileName(w, 'Open File', '/')
        self.FLAIR_path = str('/'.join(self.FLAIR_image_path.split('/')[0:-1]))+'/'

        lm = slicer.app.layoutManager()
        lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
        view = lm.threeDWidget(0).threeDView()
        viewNode = view.mrmlViewNode()

        viewNode.SetBackgroundColor((0,0,0))
        viewNode.SetBackgroundColor2((0,0,0))
        viewNode.SetAxisLabelsVisible(0)
        viewNode.SetBoxVisible(0)
        self.view = view

        load, image = slicer.util.loadVolume(self.FLAIR_image_path, returnNode=True)
        
        # adding a automated seed point
        volumesLogic = slicer.modules.volumes.logic()
        label_name = image.GetName()+"-rough-label"
        label = volumesLogic.CreateLabelVolume(slicer.mrmlScene, image, label_name)
#        label_path  = str(path+label_name+filetype)
#        print(label_path)
#
#        self.view = view
#        self.path = path
#        self.image_path = image_path
#        self.label_path = label_path
#        self.image_name = image.GetName()
        self.label_name = label_name
#        self.labelpostfix1 = '_tumor_confidenceconnected'
#        self.labelpostfix2 = '_lung_confidenceconnected'
        
        selectionNode = slicer.app.applicationLogic().GetSelectionNode()
        selectionNode.SetReferenceActiveLabelVolumeID(label.GetID())
        EditUtil.EditUtil().propagateVolumeSelection()

        # switch to Edit module
        slicer.util.selectModule('Editor')
        slicer.modules.EditorWidget.toolsBox.selectEffect('PaintEffect')
        

    def onloadSegFLAIRButtonClicked(self):
        
        label_sitk = su.PullFromSlicer(self.label_name)
        roi=sitk.GetArrayFromImage(label_sitk)
        roi=roi>0
        seedpointobj= AutoMRIBrainSegWizard.FastMarching_threshold_slicer()
        seedpoint=seedpointobj.computeCentroid_swap(roi)
        img_FLAIR = sitk.ReadImage(str(self.FLAIR_image_path), sitk.sitkFloat32)

        # Read in ATLAS
        atlas_T1 = sitk.ReadImage(self.atlas_T1_dir, sitk.sitkFloat32)
        labelatlas_T1 = sitk.ReadImage(self.atlas_label_T1_dir, sitk.sitkUInt8)

        # Apply ATLAS to FLAIR image
        img_FLAIRbrain, brainmask = AutoMRIBrainSegWizard.MRIBrainSegmentor().skullstrip(img_FLAIR, atlas_T1, labelatlas_T1)

        # write out skull stripped images
        sitk.WriteImage(img_FLAIRbrain, self.FLAIR_path  + self.name_FLAIR_image)

        # Load registered and resampled FLAIR image
        img_FLAIRbrain = sitk.ReadImage(self.FLAIR_path  + self.name_FLAIR_image, sitk.sitkFloat32)

        # smoothing with filter
        blurFilter = sitk.CurvatureFlowImageFilter()
        blurFilter.SetNumberOfIterations(5)
        blurFilter.SetTimeStep(0.1)
        blurredFLAIR=blurFilter.Execute(img_FLAIRbrain)

        # perform segmentation with thresholding
        #chan_filter = sitk.ScalarChanAndVeseSparseLevelSetImageFilter()
#        water_filter = sitk.MorphologicalWatershedImageFilter()
#        water_filter.SetLevel(600)
#        segFLAIR_raw = water_filter.Execute(blurredFLAIR)
        #water_filter.SetMarkWatershedLine(1)
        #water_filter.SetFullyConnected(1)

#        seed = (219,220,13)
#        seg = sitk.Image(blurredFLAIR.GetSize(), sitk.sitkUInt8)
#        seg.CopyInformation(blurredFLAIR)
#        seg[seed] = 1
        #seg = sitk.BinaryDilate(blurredFLAIR, 3)
        #segFLAIR = sitk.ConnectedThreshold(blurredFLAIR, seedList=[seed], lower=200, upper=1200)
        
        segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                            numberOfIterations=10,
                                            multiplier=3,
                                            initialNeighborhoodRadius=1,
                                            replaceValue=1)
        print('done')
        # Filling holes if any in ROI
        vectorRadius = (10, 10, 5)
        kernel = sitk.sitkBall
        segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                   vectorRadius,
                                                   kernel)
#        b = np.array(semiauto)
#        white_pix = b.reshape(-1)
        nda = sitk.GetArrayFromImage(segFLAIR)
        white_pix = np.count_nonzero(nda)
#        n_white_pix = np.sum(semiauto == 1)
        print('Number of white pixels:', white_pix) # To check if the tumors  are segmented out well
        if white_pix > 45000:
            
                    segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                        numberOfIterations=10,
                                                        multiplier=2.75,
                                                        initialNeighborhoodRadius=1,
                                                        replaceValue=1)
                    print('done')

                    vectorRadius = (10, 10, 5)
                    kernel = sitk.sitkBall
                    segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                               vectorRadius,
                                                               kernel)

                    nda = sitk.GetArrayFromImage(segFLAIR)
                    white_pix = np.count_nonzero(nda)

                    print('Number of white pixels:', white_pix)
                    
                    if white_pix > 45000:
                        
                        segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                            numberOfIterations=10,
                                                            multiplier=2.5,
                                                            initialNeighborhoodRadius=1,
                                                            replaceValue=1)
                        print('done')

                        vectorRadius = (10, 10, 5)
                        kernel = sitk.sitkBall
                        segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                   vectorRadius,
                                                                   kernel)

                        nda = sitk.GetArrayFromImage(segFLAIR)
                        white_pix = np.count_nonzero(nda)

                        print('Number of white pixels:', white_pix)
                        if white_pix > 45000:
                            
                                                                                                        
                        
                            segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                                numberOfIterations=10,
                                                                multiplier=2.35,
                                                                initialNeighborhoodRadius=1,
                                                                replaceValue=1)
                            print('done')

                            vectorRadius = (10, 10, 5)
                            kernel = sitk.sitkBall
                            segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                   vectorRadius,
                                                                   kernel)

                            nda = sitk.GetArrayFromImage(segFLAIR)
                            white_pix = np.count_nonzero(nda)

                            print('Number of white pixels:', white_pix)
                            # This will work for very small nodules
                            if white_pix > 45000:
                                                                                                                                                                    
                        
                                segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                                    numberOfIterations=10,
                                                                    multiplier=2.15,
                                                                    initialNeighborhoodRadius=1,
                                                                    replaceValue=1)
                                print('done')

                                vectorRadius = (10, 10, 5)
                                kernel = sitk.sitkBall
                                segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                   vectorRadius,
                                                                   kernel)

                                nda = sitk.GetArrayFromImage(segFLAIR)
                                white_pix = np.count_nonzero(nda)

                                print('Number of white pixels:', white_pix)
                                # This will work for very small nodules hopefully (last resort)
                                if white_pix > 45000:
                                    
                                
                                                                                                        
                                    segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                                        numberOfIterations=10,
                                                                        multiplier=1.95,
                                                                        initialNeighborhoodRadius=1,
                                                                        replaceValue=1)
                                    print('done')

                                    vectorRadius = (10, 10, 5)
                                    kernel = sitk.sitkBall
                                    segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                               vectorRadius,
                                                                               kernel)

                                    nda = sitk.GetArrayFromImage(segFLAIR)
                                    white_pix = np.count_nonzero(nda)

                                    print('Number of white pixels:', white_pix)
                                                                    
                                    if white_pix > 45000:
                                                                                                            
                                                                                                        
                                        segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                                            numberOfIterations=10,
                                                                            multiplier=1.85,
                                                                            initialNeighborhoodRadius=1,
                                                                            replaceValue=1)
                                        print('done')

                                        vectorRadius = (10, 10, 5)
                                        kernel = sitk.sitkBall
                                        segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                               vectorRadius,
                                                                               kernel)

                                        nda = sitk.GetArrayFromImage(segFLAIR)
                                        white_pix = np.count_nonzero(nda)

                                        print('Number of white pixels:', white_pix)
                                        
                                        if white_pix > 45000:
                                            
                                                                                                            
                                                                                                        
                                            segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                                                numberOfIterations=10,
                                                                                multiplier=1.75,
                                                                                initialNeighborhoodRadius=1,
                                                                                replaceValue=1)
                                            print('done')

                                            vectorRadius = (10, 10, 5)
                                            kernel = sitk.sitkBall
                                            segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                               vectorRadius,
                                                                               kernel)

                                            nda = sitk.GetArrayFromImage(segFLAIR)
                                            white_pix = np.count_nonzero(nda)

                                            print('Number of white pixels:', white_pix)
                                            
                                            if white_pix > 45000:
                                                                                            
                                                                                                            
                                                                                                        
                                                segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                                                    numberOfIterations=10,
                                                                                    multiplier=1.65,
                                                                                    initialNeighborhoodRadius=1,
                                                                                    replaceValue=1)
                                                print('done')

                                                vectorRadius = (10, 10, 5)
                                                kernel = sitk.sitkBall
                                                segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                                           vectorRadius,
                                                                                           kernel)

                                                nda = sitk.GetArrayFromImage(segFLAIR)
                                                white_pix = np.count_nonzero(nda)

                                                print('Number of white pixels:', white_pix)
                                                
                                                if white_pix > 45000:
                                                                                            
                                                                                                            
                                                                                                        
                                                    segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                                                        numberOfIterations=10,
                                                                                        multiplier=1.55,
                                                                                        initialNeighborhoodRadius=1,
                                                                                        replaceValue=1)
                                                    print('done')

                                                    vectorRadius = (10, 10, 5)
                                                    kernel = sitk.sitkBall
                                                    segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                                           vectorRadius,
                                                                                           kernel)

                                                    nda = sitk.GetArrayFromImage(segFLAIR)
                                                    white_pix = np.count_nonzero(nda)

                                                    print('Number of white pixels:', white_pix)
                                                    
                                                    if white_pix > 45000:
                                                                                            
                                                                                                            
                                                                                                        
                                                        segFLAIR = sitk.ConfidenceConnected(blurredFLAIR, seedList=[seedpoint],
                                                                                            numberOfIterations=10,
                                                                                            multiplier=1.4,
                                                                                            initialNeighborhoodRadius=1,
                                                                                            replaceValue=1)
                                                        print('done')

                                                        vectorRadius = (10, 10, 5)
                                                        kernel = sitk.sitkBall
                                                        segFLAIR = sitk.BinaryMorphologicalClosing(segFLAIR,
                                                                                                   vectorRadius,
                                                                                                   kernel)

                                                        nda = sitk.GetArrayFromImage(segFLAIR)
                                                        white_pix = np.count_nonzero(nda)

                                                        print('Number of white pixels:', white_pix)
                                    
        holefill=sitk.VotingBinaryIterativeHoleFillingImageFilter() 
        holefill.SetMaximumNumberOfIterations(5)
        segFLAIR=holefill.Execute(segFLAIR) 

        ### save resulting segmentation ###
        sitk.WriteImage(segFLAIR, self.FLAIR_path + self.name_FLAIR_label)


        FLAIR_label = slicer.util.loadVolume(self.FLAIR_path + self.name_FLAIR_label, properties={'labelmap':True}, returnNode=True)

        labelname = 'FLAIR_label';
        labelNode = slicer.util.getNode(pattern=labelname)
        self.labelNode = labelNode
        self.auto3DGen()



#    def changesApplyButtonClicked(self):
#        seg_number = self.sigmaSlider.value
#        print("ROI volume selected is: ", seg_number)
#
#        img_FLAIR = sitk.ReadImage(str(self.FLAIR_image_path), sitk.sitkFloat32)
#
#        # Read in ATLAS
#        atlas_T1 = sitk.ReadImage(self.atlas_T1_dir, sitk.sitkFloat32)
#        labelatlas_T1 = sitk.ReadImage(self.atlas_label_T1_dir, sitk.sitkUInt8)
#
#        # Apply ATLAS to FLAIR image
#        img_FLAIRbrain, brainmask = AutoMRIBrainSegWizard.MRIBrainSegmentor().skullstrip(img_FLAIR, atlas_T1, labelatlas_T1)
#
#        # write out skull stripped images
#        sitk.WriteImage(img_FLAIRbrain, self.FLAIR_path  + self.name_FLAIR_image)
#
#        # Load registered and resampled FLAIR image
#        img_FLAIRbrain = sitk.ReadImage(self.FLAIR_path  + self.name_FLAIR_image, sitk.sitkFloat32)
#
#        # smoothing with filter
#        blurFilter = sitk.CurvatureFlowImageFilter()
#        blurFilter.SetNumberOfIterations(5)
#        blurFilter.SetTimeStep(0.1)
#        blurredFLAIR=blurFilter.Execute(img_FLAIRbrain)
#
#        # perform segmentation with thresholding
#        otsu_filter = sitk.OtsuMultipleThresholdsImageFilter()
#        otsu_filter.SetNumberOfThresholds(3)
#        otsu_filter.Execute(blurredFLAIR)
#        thresholds = otsu_filter.GetThresholds()
#        print('Thresholds for FLAIR segmentation =',thresholds)
#
#        segFLAIR_raw = blurredFLAIR>thresholds[2]
#        # Refine FLAIR segmentation
#        # Find largest most spherical region in FLAIR segmentation
#        segFLAIR, tumor_volume = AutoMRIBrainSegWizard.MRIBrainSegmentor().sphereFinder(segFLAIR_raw, self.elong_thresh, seg_number)
#        segFLAIR.CopyInformation(img_FLAIRbrain)
#
#        # If tumor volume too big then run thresholding again on segmented volume
#        if tumor_volume > self.volume_FLAIR_upper_threshold: 
#            msk = sitk.MaskImageFilter()
#            blurredFLAIR_masked=msk.Execute(blurredFLAIR,segFLAIR>0)
#            # perform segmentation with thresholding
#            otsu_filter = sitk.OtsuMultipleThresholdsImageFilter()
#            otsu_filter.SetNumberOfThresholds(3)
#            otsu_filter.Execute(blurredFLAIR_masked)
#            thresholds_masked = otsu_filter.GetThresholds()
#            print('Thresholds for masked FLAIR segmentation =',thresholds_masked)
#            segFLAIR = blurredFLAIR_masked > thresholds_masked[2]
#            # Find largest most spherical region in FLAIR segmentation
#            segFLAIR, tumor_volume = AutoMRIBrainSegWizard.MRIBrainSegmentor().sphereFinder(segFLAIR, self.elong_thresh, seg_number)
#            segFLAIR.CopyInformation(img_FLAIRbrain)
#            # Try different threhold if tumor volume becomes too small
#            if tumor_volume < self.volume_FLAIR_lower_threshold: 
#                segFLAIR_upper = blurredFLAIR_masked > thresholds_masked[1] 
#                segFLAIR_lower = blurredFLAIR_masked < thresholds_masked[2]
#                segFLAIR = segFLAIR_lower * segFLAIR_upper
#                segFLAIR, tumor_volume = AutoMRIBrainSegWizard.MRIBrainSegmentor().sphereFinder(segFLAIR, self.elong_thresh, seg_number)
#                segFLAIR.CopyInformation(img_FLAIRbrain)
#                if tumor_volume < self.volume_FLAIR_lower_threshold: 
#                    segFLAIR_upper = blurredFLAIR_masked > thresholds_masked[0] 
#                    segFLAIR_lower = blurredFLAIR_masked < thresholds_masked[1]
#                    segFLAIR = segFLAIR_lower * segFLAIR_upper
#                    segFLAIR, tumor_volume = AutoMRIBrainSegWizard.MRIBrainSegmentor().sphereFinder(segFLAIR, self.elong_thresh, seg_number)
#                    segFLAIR.CopyInformation(img_FLAIRbrain)
#        ## End of if statement
#
#        # Fill holes
#        holefill=sitk.VotingBinaryIterativeHoleFillingImageFilter() 
#        holefill.SetMaximumNumberOfIterations(5)
#        segFLAIR=holefill.Execute(segFLAIR) 
#
#        ### save resulting segmentation ###
#        sitk.WriteImage(segFLAIR, self.FLAIR_path + self.name_FLAIR_label)
#
#
#        FLAIR_label = slicer.util.loadVolume(self.FLAIR_path + self.name_FLAIR_label, properties={'labelmap':True}, returnNode=True)
#
#        labelname = 'FLAIR_label';
#        labelNode = slicer.util.getNode(pattern=labelname)
#        self.labelNode = labelNode
#        self.auto3DGen()
