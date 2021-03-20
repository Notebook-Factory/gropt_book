# Abstract
***
*Michael Loecher* <sup>1,2</sup> | *Matthew J. Middione* <sup>1,2</sup> | *Daniel B. Ennis* <sup>1,2</sup>



<sup>1</sup> Department of Radiology, Stanford University, Stanford, CA, USA
<br>
<sup>2</sup> Department of Radiology, Veterans Affairs Palo Alto Health Care System, Palo Alto, CA, USA


**Purpose**: To introduce and demonstrate a software library for time‐optimal gradient waveform optimization with a wide range of applications. The software enables direct on‐the‐fly gradient waveform design on the scanner hardware for multiple vendors.
<br />

**Methods**: The open‐source gradient optimization (GrOpt) toolbox was implemented in C with both Matlab and Python wrappers. The toolbox enables gradient waveforms to be generated based on a set of constraints that define the features and encodings for a given acquisition. The GrOpt optimization routine is based on the alternating direction method of multipliers (ADMM). Additional constraints enable error corrections to be added, or patient comfort and safety to be adressed. A range of applications and compute speed metrics are analyzed. Finally, the method is implemented and tested on scanners from different vendors. <br />
**Results**: Time‐optimal gradient waveforms for different pulse sequences and the constraints that define them are shown. Additionally, the ability to add, arbitrary motion (gradient moment) compensation or limit peripheral nerve stimulation is demonstrated. There exists a trade‐off between computation time and gradient raster time, but it was observed that acceptable gradient waveforms could be generated in 1‐40 ms. Gradient waveforms generated and run on the different scanners were functionally equivalent, and the images were comparable. <br />
**Conclusions**: GrOpt is an open source toolbox that enables on‐the‐fly optimization of gradient waveform design, subject to a set of defined constraints. GrOpt was presented for a range of imaging applications, analyzed in terms of computational complexity, and implemented to run on the scanner for a multi‐vendor demonstration.
<br />
<br />
*KEYWORDS* 
<br />
*Gradient waveform design, MRI, Open source software, Optimization*



**Corespondence**: Michael Loecher, Radiological Sciences Lab, Stanford University, 1201 Welch Road, Stanford, CA 94305, USA.
Email: mloecher@stanford.edu