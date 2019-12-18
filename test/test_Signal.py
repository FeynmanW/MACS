#!/usr/bin/env python
# Time-stamp: <2019-12-18 16:48:36 taoliu>

"""Module Description: Test functions for Signal.pyx

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file LICENSE included with
the distribution).
"""

import unittest

from math import log10
import numpy as np
from MACS2.Signal import maxima, savitzky_golay, savitzky_golay_order2_deriv1

# ------------------------------------
# Main function
# ------------------------------------

class Test_maxima(unittest.TestCase):

    def setUp(self):
        data = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,4.0,4.0,4.0,4.0,
                4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,
                5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,
                5.0,5.0,5.0,5.0,5.0,5.0,5.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,
                6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,7.0,7.0,7.0,
                7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,
                7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,6.0,6.0,6.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,
                7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,
                7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,8.0,8.0,8.0,8.0,
                8.0,8.0,8.0,8.0,8.0,8.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,7.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,
                6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,6.0,4.0,4.0,4.0,4.0,4.0,
                4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,
                4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,4.0,
                4.0,4.0,4.0,4.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,
                3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,
                3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,
                3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,
                3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,
                3.0,3.0,3.0,3.0,3.0,3.0]
        # 1-deriv, used to find maximum point with smoothing function
        smoothed  = [ 6.61562562e-02, 6.61510691e-02, 6.61355078e-02, 6.61095723e-02
                    , 6.60732626e-02, 6.60265787e-02, 6.59695206e-02, 6.59020883e-02
                    , 6.58242818e-02, 6.57361012e-02, 6.56375463e-02, 6.56227260e-02
                    , 6.55982725e-02, 6.55641859e-02, 6.55204661e-02, 6.54671131e-02
                    , 6.54041269e-02, 6.53315075e-02, 6.52492549e-02, 6.51573692e-02
                    , 6.50558502e-02, 6.49446981e-02, 6.48239128e-02, 6.46934943e-02
                    , 6.45534427e-02, 6.44037578e-02, 6.42444398e-02, 6.40754886e-02
                    , 6.38969042e-02, 6.37086866e-02, 6.35108358e-02, 6.32099841e-02
                    , 6.29002402e-02, 6.25816042e-02, 6.23474437e-02, 6.21036501e-02
                    , 6.18502233e-02, 6.15871633e-02, 6.13144701e-02, 6.10321437e-02
                    , 6.07401842e-02, 6.04385914e-02, 6.01273655e-02, 5.98065064e-02
                    , 5.94760141e-02, 5.91358886e-02, 5.87861300e-02, 5.84267382e-02
                    , 5.80577131e-02, 5.77731637e-02, 5.74797221e-02, 5.71773884e-02
                    , 5.68661625e-02, 5.65460444e-02, 5.62170341e-02, 5.58791317e-02
                    , 5.55323371e-02, 5.51766503e-02, 5.48120714e-02, 5.44386003e-02
                    , 5.40562370e-02, 5.36649816e-02, 5.32648340e-02, 5.28557942e-02
                    , 5.24378623e-02, 5.20110381e-02, 5.15753219e-02, 5.11307134e-02
                    , 5.06772128e-02, 5.02148200e-02, 4.97435350e-02, 4.92633579e-02
                    , 4.87742886e-02, 4.82763271e-02, 4.77694735e-02, 4.72537277e-02
                    , 4.67290897e-02, 4.61955595e-02, 4.56531372e-02, 4.51018227e-02
                    , 4.45416161e-02, 4.39725173e-02, 4.33945263e-02, 4.28076431e-02
                    , 4.22118678e-02, 4.16072003e-02, 4.10870084e-02, 4.05571833e-02
                    , 4.00177251e-02, 3.95627424e-02, 3.90988676e-02, 3.86261006e-02
                    , 3.81444414e-02, 3.76538901e-02, 3.71544466e-02, 3.66461109e-02
                    , 3.60355153e-02, 3.54167686e-02, 3.47898706e-02, 3.41548216e-02
                    , 3.35116213e-02, 3.28602699e-02, 3.22007674e-02, 3.15331137e-02
                    , 3.07639411e-02, 2.99873583e-02, 2.92033654e-02, 2.84119623e-02
                    , 2.79895843e-02, 2.75627602e-02, 2.71314900e-02, 2.66957737e-02
                    , 2.62556113e-02, 2.58110029e-02, 2.53619483e-02, 2.49084477e-02
                    , 2.44505010e-02, 2.39881082e-02, 2.35212693e-02, 2.30499844e-02
                    , 2.25742533e-02, 2.20940762e-02, 2.16094530e-02, 2.11203837e-02
                    , 2.06268683e-02, 2.01289068e-02, 1.96264993e-02, 1.91196456e-02
                    , 1.86083459e-02, 1.80926001e-02, 1.75724082e-02, 1.70477702e-02
                    , 1.65186862e-02, 1.57984205e-02, 1.50751907e-02, 1.43489969e-02
                    , 1.36198390e-02, 1.28877171e-02, 1.21526311e-02, 1.14145811e-02
                    , 1.06735670e-02, 9.92958884e-03, 9.18264664e-03, 8.43274037e-03
                    , 7.67987006e-03, 6.92403568e-03, 6.16523725e-03, 5.77990992e-03
                    , 5.39458259e-03, 5.00925527e-03, 4.62392794e-03, 4.23860061e-03
                    , 3.85327328e-03, 3.46794595e-03, 3.08261863e-03, 2.69729130e-03
                    , 2.31196397e-03, 1.92663664e-03, 1.54130931e-03, 1.15598198e-03
                    , 7.70654656e-04, 3.85327328e-04, -2.98155597e-18, -3.85327328e-04 # 3.85327328e-04  is the maximum point smoothed[161]
                    , -7.70654656e-04, -1.15598198e-03, -1.44720052e-03, -1.73767805e-03
                    , -2.02741456e-03, -2.31641005e-03, -2.60466454e-03, -2.89217800e-03
                    , -3.17895046e-03, -3.46498190e-03, -3.75027232e-03, -4.03482173e-03
                    , -4.31863013e-03, -4.60169752e-03, -4.88402388e-03, -5.16560924e-03
                    , -5.44645358e-03, -5.72655691e-03, -6.00591922e-03, -6.28454052e-03
                    , -6.56242080e-03, -6.83956007e-03, -7.11595833e-03, -7.39161557e-03
                    , -7.66653180e-03, -7.94070702e-03, -8.30750899e-03, -8.67282894e-03
                    , -9.03666686e-03, -9.39902275e-03, -9.75989661e-03, -1.01192884e-02
                    , -1.04771983e-02, -1.08336260e-02, -1.11885718e-02, -1.15420355e-02
                    , -1.18940172e-02, -1.22445169e-02, -1.25935345e-02, -1.29410701e-02
                    , -1.32871237e-02, -1.36316952e-02, -1.38806760e-02, -1.41274337e-02
                    , -1.43719683e-02, -1.46142799e-02, -1.48543685e-02, -1.50922340e-02
                    , -1.53278765e-02, -1.55612959e-02, -1.57924923e-02, -1.60214657e-02
                    , -1.62482160e-02, -1.64727433e-02, -1.66950475e-02, -1.69151287e-02
                    , -1.71329868e-02, -1.73486219e-02, -1.75620340e-02, -1.77732230e-02
                    , -1.79821890e-02, -1.81889319e-02, -1.83934518e-02, -1.85957487e-02
                    , -1.87958225e-02, -1.89936732e-02, -1.91893009e-02, -1.93827056e-02
                    , -1.95738873e-02, -1.97628458e-02, -1.99495814e-02, -2.01340939e-02
                    , -2.03163834e-02, -2.04964498e-02, -2.06742932e-02, -2.08499135e-02
                    , -2.10233108e-02, -2.11944851e-02, -2.13634363e-02, -2.15301645e-02
                    , -2.16005608e-02, -2.16679931e-02, -2.17324613e-02, -2.17939655e-02
                    , -2.18525056e-02, -2.19080816e-02, -2.19606936e-02, -2.20103416e-02
                    , -2.20570255e-02, -2.21007453e-02, -2.21415011e-02, -2.21792928e-02
                    , -2.22141205e-02, -2.22459841e-02, -2.22748836e-02, -2.23008191e-02
                    , -2.23237906e-02, -2.23437979e-02, -2.23608413e-02, -2.23749205e-02
                    , -2.23860357e-02, -2.23941869e-02, -2.23993740e-02, -2.24015970e-02
                    , -2.24008560e-02, -2.23971509e-02, -2.23904818e-02, -2.23808486e-02
                    , -2.23682514e-02, -2.23526901e-02, -2.23341648e-02, -2.23126753e-02
                    , -2.22882219e-02, -2.22608044e-02, -2.22304228e-02, -2.21970771e-02
                    , -2.21607675e-02, -2.21214937e-02, -2.20792559e-02, -2.20340540e-02
                    , -2.20799969e-02, -2.21237167e-02, -2.21652135e-02, -2.21103785e-02
                    , -2.20525794e-02, -2.19918162e-02, -2.19280890e-02, -2.18613978e-02
                    , -2.17917424e-02, -2.17191231e-02, -2.16435396e-02, -2.15649921e-02
                    , -2.14834806e-02, -2.13990050e-02, -2.13115653e-02, -2.12211616e-02
                    , -2.11277938e-02, -2.10314620e-02, -2.09321661e-02, -2.08299061e-02
                    , -2.07246821e-02, -2.06164941e-02, -2.05053420e-02, -2.03912258e-02
                    , -2.02741456e-02, -2.01541013e-02, -2.00310930e-02, -1.99051206e-02
                    , -1.97761841e-02, -1.96442836e-02, -1.95094190e-02, -1.93715904e-02
                    , -1.92307977e-02, -1.90870410e-02, -1.89403202e-02, -1.87906354e-02
                    , -1.86379865e-02, -1.84823735e-02, -1.83237965e-02, -1.81622554e-02
                    , -1.79977503e-02, -1.78302811e-02, -1.76598479e-02, -1.74864506e-02
                    , -1.73100892e-02, -1.71307638e-02, -1.69484743e-02, -1.67632208e-02
                    , -1.65750032e-02, -1.63838216e-02, -1.61896759e-02, -1.59925661e-02
                    , -1.57924923e-02, -1.55894545e-02, -1.53834526e-02, -1.50803778e-02
                    , -1.47735980e-02, -1.44631131e-02, -1.41489231e-02, -1.38310280e-02
                    , -1.35094279e-02, -1.31841227e-02, -1.28551125e-02, -1.25223972e-02
                    , -1.21859768e-02, -1.19399601e-02, -1.16909793e-02, -1.14390345e-02
                    , -1.11841257e-02, -1.09262528e-02, -1.06654158e-02, -1.04016148e-02
                    , -1.01348497e-02, -9.95922940e-03, -9.78138602e-03, -9.60131960e-03
                    , -9.41903013e-03, -9.23451762e-03, -9.04778207e-03, -8.85882348e-03
                    , -8.66764184e-03, -8.47423716e-03, -8.27860944e-03, -8.08075868e-03
                    , -7.88068487e-03, -7.67838803e-03, -7.47386814e-03, -7.26712521e-03
                    , -7.05815923e-03, -6.84697022e-03, -6.63355816e-03, -6.41792306e-03
                    , -6.20006491e-03, -5.97998373e-03, -5.75767950e-03, -5.53315223e-03
                    , -5.30640192e-03, -5.07742856e-03, -4.84623217e-03, -4.61281273e-03
                    , -4.37717025e-03, -4.13930472e-03, -4.08743373e-03, -4.03482173e-03
                    , -3.98146872e-03, -3.92737469e-03, -3.87253965e-03, -3.81696359e-03
                    , -3.76064652e-03, -3.70358843e-03, -3.64578934e-03, -3.58724922e-03
                    , -3.52796809e-03, -3.46794595e-03, -3.40718280e-03, -3.34567863e-03
                    , -3.28343344e-03, -3.22044725e-03, -3.15672003e-03, -3.09225181e-03
                    , -3.02704257e-03, -2.96109231e-03, -2.89440105e-03, -2.82696876e-03
                    , -2.75879547e-03, -2.68988116e-03, -2.62022583e-03, -2.54982949e-03
                    , -2.47869214e-03, -2.40681377e-03, -2.33419439e-03, -2.26083400e-03
                    , -2.18673259e-03, -2.11189016e-03, -2.03630673e-03, -1.95998227e-03
                    , -1.88291681e-03, -1.80511033e-03, -1.72656284e-03, -1.64727433e-03
                    , -1.56724481e-03, -1.48647427e-03, -1.40496272e-03, -1.32271016e-03
                    , -1.23971658e-03, -1.15598198e-03, -1.07150638e-03, -9.86289757e-04
                    , -9.00332123e-04, -7.20265698e-04, -5.40199274e-04, -3.60132849e-04
                    , -1.80066425e-04, -2.11419424e-18]
        sign = [ 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
                 , 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
                 , 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
                 , 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
                 , 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
                 , 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
                 , 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
                 , 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
                 , 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1. #<- the last 1 is #162 or sign[161]
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.
                 ,-1.,-1.,-1.,-1.,-1.,-1.]
        diff = [ 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,-2. #<- this -2 is #162 or diff[161]
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
                 , 0., 0., 0., 0., 0.]
        self.signal = np.array(data, dtype=np.float32 )
        self.smooth = np.array(smoothed,  dtype=np.float32 )
        self.sign = np.array(sign, dtype=np.float32 )
        self.diff = np.array(diff, dtype=np.float32 )        
        self.windowsize = 253
        self.summit = 161       # this is based on 1-deriv smoothed data

    def test_savitzky_golay(self):
        result = savitzky_golay( self.signal, self.windowsize, 2, deriv = 1 )
        self.assertEqual_nparray1d( result, self.smooth )

    def test_savitzky_golay_order2_deriv1(self):
        result = savitzky_golay_order2_deriv1( self.signal, self.windowsize )
        self.assertEqual_nparray1d( result, self.smooth )

    def test_numpy( self ):
        smoothed = [  6.61562562e-02,  6.61510691e-02,  6.61355078e-02,  6.61095723e-02,
                       7.70654656e-04,  3.85327328e-04, -2.98155597e-18, -3.85327328e-04, # 3.85327328e-04  is the maximum point smoothed[5] or #6
                      -7.70654656e-04, -1.15598198e-03, -1.44720052e-03, -1.73767805e-03 ]
        sign = [ 1., 1., 1., 1.,
                 1., 1.,-1.,-1., # the 6th is the max
                -1.,-1.,-1.,-1. ]
        diff = [ 0., 0., 0., 0.,
                 0.,-2., 0., 0., # trhe 6th has -2
                 0., 0., 0. ]

        np_smoothed= np.array(smoothed, dtype=np.float32 )        
        np_sign = np.array(sign, dtype=np.float32 )
        np_diff = np.array(diff, dtype=np.float32 )       

        sign = np.sign( np_smoothed )
        self.assertEqual_nparray1d( sign, np_sign )
        diff = np.diff( np_sign )
        self.assertEqual_nparray1d( diff, np_diff )
        m = np.where( diff <= -1)[0].astype('int32')
        self.assertEqual( m, 5 )

    # test predefined smoothed data
    def test_numpy_2 ( self ):
        s = savitzky_golay_order2_deriv1( self.signal, self.windowsize )
        self.assertEqual_nparray1d( s, self.smooth )
        print ("expected smoothed:")
        print (self.smooth[160:165])
        print ("calculated smoothed:")
        print (s[160:165])
        
        sign = np.sign( self.smooth )
        self.assertEqual_nparray1d( sign, self.sign )
        sign2= np.sign( s )

        print ("expected smoothed (output again):")
        print (self.smooth[160:165])
        print ("calculated smoothed (output again):")
        print (s[160:165])

        print ("expected sign:")        
        print (self.sign[160:165])
        print ("calculated sign from expected smoothed data:")        
        print (sign[160:165])
        print ("calculated sign from recalculated smoothed data:")        
        print (sign2[160:165])        
        
        self.assertEqual_nparray1d( sign, sign2 )
        self.assertEqual_nparray1d( sign2, self.sign )        

        diff = np.diff( self.sign )
        self.assertEqual_nparray1d( diff, self.diff )

        m = np.where( self.diff <= -1)[0].astype('int32')
        self.assertEqual( m, 161 )

    def test_implement_smooth_here ( self ):
        signal = self.signal
        window_size = self.windowsize
        half_window = (window_size - 1) // 2
        # precompute coefficients
        b = np.array([[1, k, k**2] for k in range(-half_window, half_window+1)], dtype='int64')
        m = np.linalg.pinv(b)[1]
        # pad the signal at the extremes with
        # values taken from the signal itself
        firstvals = signal[0] - np.abs(signal[1:half_window+1][::-1] - signal[0])
        lastvals = signal[-1] + np.abs(signal[-half_window-1:-1][::-1] - signal[-1])
        signal = np.concatenate((firstvals, signal, lastvals))
        ret = np.convolve( m[::-1], signal.astype("float64"), mode='valid') #.astype("float32").round(8) # round to 8 decimals to avoid signing issue
        p = ret[160:165]
        p2 = savitzky_golay_order2_deriv1( self.signal, self.windowsize )[160:165]
        e = self.smooth[160:165]
        print (m[150:170], p, p2, e)
        self.assertEqual_nparray1d( p, e )
        self.assertEqual_nparray1d( p2, e )
        self.assertEqual(1, 2)

        
    def test_maxima(self):
        expect = self.summit
        result = maxima( self.signal, self.windowsize )[0]
        self.assertEqual( result, expect, msg=f"Not equal: result: {result}, expected: {expect}" )

    def assertEqual_nparray1d ( self, a, b, roundn = 4 ):
        self.assertEqual( a.shape[0], b.shape[0] )
        l = a.shape[0]
        for i in range( l ):
            self.assertAlmostEqual( a[i], b[i], places = roundn, msg=f"Not equal at {i} {a[i]} {b[i]}" )
            
