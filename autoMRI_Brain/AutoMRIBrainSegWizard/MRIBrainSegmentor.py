import SimpleITK as sitk
import numpy as np
import os 


class MRIBrainSegmentor:
    def __init__(self):
        pass

    # function for skullstripping
    def skullstrip(self, image, atlas, brain_label):
        fixed_image = image
        moving_image = atlas
        initial_transform = sitk.CenteredTransformInitializer(fixed_image, moving_image,sitk.AffineTransform(fixed_image.GetDimension()), sitk.CenteredTransformInitializerFilter.GEOMETRY)
        registration_method = sitk.ImageRegistrationMethod()

        # Similarity metric settings.
        registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
        #registration_method.SetMetricAsDemons(intensityDifferenceThreshold=0.001)
        #registration_method.SetMetricAsJointHistogramMutualInformation	(numberOfHistogramBins = 20,varianceForJointPDFSmoothing = 1.5)
        #registration_method.SetMetricAsANTSNeighborhoodCorrelation(4)
        
        registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
        registration_method.SetMetricSamplingPercentage(0.2, 1) # Percentage of voxels, random number seed (for reproducible results)

        registration_method.SetInterpolator(sitk.sitkLinear)

        # Optimizer settings.
        registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,convergenceMinimumValue=1e-6, convergenceWindowSize=10)
        registration_method.SetOptimizerScalesFromPhysicalShift()

        # Setup for the multi-resolution framework.
        registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [4,2,1])
        registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[4,2,0])
        registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

        registration_method.SetInitialTransform(initial_transform, inPlace=False)

        final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),sitk.Cast(moving_image, sitk.sitkFloat32))

        print('Optimizer\'s stopping condition brain mask, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))
        print('Final metric value brain mask: {0}'.format(registration_method.GetMetricValue()))

        brainmask = sitk.Resample(brain_label, fixed_image, final_transform, sitk.sitkNearestNeighbor,0.0,moving_image.GetPixelID())

        msk = sitk.MaskImageFilter()
        brainimage=msk.Execute(image,brainmask>0 )

        return (brainimage, brainmask)



    # function to find largest most spherical region in a segmentation
    def sphereFinder(self, seg, elong_threshold, seg_number):
        conncomp = sitk.ConnectedComponentImageFilter()
        seg = conncomp.Execute(seg)
        # find label characteristics
        stats = sitk.LabelShapeStatisticsImageFilter()
        stats.Execute(seg)

        labels = stats.GetLabels()
        sizes=[]
        elong = []
        for lab in labels:
            dia=stats.GetEquivalentEllipsoidDiameter(lab)  # in rare cases this will fail and give nans
            ratiodia = np.square(1- dia[1]/(dia[0]+1e-10))
            elong.append(ratiodia)
            sizes.append(stats.GetPhysicalSize(lab))
        sizes=np.asarray(sizes)
        elong = np.asarray(elong)
        labels = np.asarray(labels)

        #  with (1-ratio of ellipsoid diameters)^2 closest to zero, thresholding at elong_threshold
        elong= np.asarray(elong)
        sizes=np.asarray(sizes)
        # find all the regions that have elong < elong_threshold
        sphlabel_inds = np.where(elong<elong_threshold)
        if elong_threshold == -1:
            sphlabel_inds = np.where(elong)
        # among those regions, pick the largest one
        sizes_within_thresh = sizes[sphlabel_inds]   
        sizeinds = np.argmax(sizes_within_thresh)
        
        # Try second largest volume
        ind = 1
        while ind < seg_number:
            sizes_within_thresh[sizeinds] = 0
            sizeinds = np.argmax(sizes_within_thresh)
            ind += 1


        tumor_volume = sizes[sphlabel_inds[0]][sizeinds]

        tlabel = labels[sphlabel_inds[0][sizeinds]]
        tarr = sitk.GetArrayFromImage(seg)
        tarr[tarr!=tlabel]=0
        tarr[tarr>0]=1
        seg = sitk.GetImageFromArray(tarr)
        print("Choosing label corresponding to elong =%f and size = %f" %(elong[sphlabel_inds[0][sizeinds]], tumor_volume))   

        return (seg, tumor_volume)