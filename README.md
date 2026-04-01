<h1 align="center">
  <span style="color:#00FFFF;"> ٠ ࣪⭑Experimental CubeSat Star Tracker๋࣭ ⭑</span>
</h1>


## ✦ Summary ✦

This project is a MATLAB-based exploratory prototype aimed at understanding the basic pipeline of star trackers used for spacecraft attitude determination. It operates on BMP images captured from an MT9P031 CMOS sensor and focuses on experimenting with key steps such as star detection, centroiding, and pattern matching, rather than implementing a complete or optimized system. 

Pixel coordinates are converted into 3D unit vectors using an inverse pinhole camera model with assumed parameters (focal length and pixel pitch). This serves as a simplified approximation and does not fully capture real optical or sensor behavior.

Lens distortion effects were explored using the Brown–Conrady distortion model, with parameters obtained from Astrometry.net (plate solving). This was used to observe how distortion influences centroid accuracy, rather than perform precise calibration.

Star-like regions are identified using intensity thresholding followed by 4-connected region growing. Sub-pixel centroids are estimated using a weighted center-of-gravity approach. This method works reasonably well for clear star blobs but is sensitive to noise and threshold selection.

A small reference catalog (~60 Hipparcos-2 stars in the Gemini region) was used for initial experiments instead of a full-sky catalog. Triangle-based geometric features (angular distances) are generated and matched using a hash-based lookup approach. This simplifies matching but limits robustness and scalability.

Candidate matches are checked using Wahba’s problem (solved via SVD/Kabsch) to estimate rotation and observe consistency between detected and catalog stars. The resulting attitude is expressed as a rotation matrix and Euler angles.

Overall, this is a learning-oriented prototype intended to explore the core concepts behind star tracker pipelines, rather than a flight-ready or optimized implementation.

<img width="480" height="246" alt="Screenshot (994)" src="https://github.com/user-attachments/assets/5d02052a-dd08-4c9f-824c-c89a425cab40" /><img width="320" height="246" alt="Screenshot (430)" src="https://github.com/user-attachments/assets/2f5aec61-dffe-4798-b17d-8d1ca99f53d7" />


### Random Notes
- I'll be dumping everything I came across or tried to use in the extra folder — research papers, reduced catalogs, files from Nova, etc.<br>
- Many parts still need improvement, especially where accuracy is low or latency is high (and there are definitely better modern methods I wasn’t able to implement). 
- Use the Tycho-2 catalog for fainter stars' magnitudes if needed.<br>
- Also, .fits files can’t be directly opened, so I generated quick-fix Python scripts for opening them. They worked, but I didn't bother maintaining/sorting the scripts       after their work was over. So, use them carefully or consider writing your own.<br>
- Tried a few plate-solving tools… turns out that’s a whole topic on its own. <br>
- Currently takes ~50 sec to solve one image after partially parallelizing the triangle DB (earlier ~1:10 min)-still slow. <br>
- Finding good input images (with minimal distortion) is a challenge in itself. Try to find someone experienced with real star trackers for better insight into                parameters and constraints. <br>
- Initially planned to implement a geometric voting algorithm (GVA), but ran into multiple issues during implementation. format it so there is no text below bullet points when i put it in readme.
  




