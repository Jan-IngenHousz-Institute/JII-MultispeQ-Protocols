"""
Simple example on how to take a measurement using a protocol
"""

import matplotlib.pyplot as plt
from jii_multispeq import measurement
from jii_multispeq_protocols import rides as _rides

out = measurement.analyze( _rides._example, _rides._analzye )

measurement.view( out )

# PSI_data_absorbance
# LEFd_trace
# data_raw_PAM

plt.figure(figsize=(10, 6))
plt.plot(out['data_raw_PAM'], color='red', marker='.', linestyle='-', 
                 linewidth=2, markersize=8)
plt.tight_layout()
plt.show()