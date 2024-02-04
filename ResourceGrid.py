import numpy as np
class ResourceGrid:
    def __init__(self,guard_carriers,ofdm_symbols,FFT_size,pilot_symbol,Bandwidth):
        self._guard_carriers = guard_carriers
        self._ofdm_symbols = ofdm_symbols
        self._fft_size = FFT_size
        
        self._pilot_symbol = pilot_symbol
        self._Bandwidth = Bandwidth
        self._effective_carriers = FFT_size - 2*guard_carriers
        self._pilot_carriers = self._effective_carriers // 4
        self._data_carriers = self._effective_carriers - self._pilot_carriers
        self._pilot_interval = int(np.rint(self._data_carriers//self._pilot_carriers))
        self._data_symbols = ofdm_symbols * self._data_carriers
        self._subcarrier_spacing = self.subcarrier_spacing()
        self._samplingFrequency = self.SamplingFrequeny()
        self._samplingTime = 1/self._samplingFrequency
        self._OFDM_SymbolDuration = self.OFDM_SymbolDuration()
        self._OFDM_GuardDuration = self.OFDM_GuardDuration()
        self._TotalDuration = self._OFDM_GuardDuration + self._OFDM_SymbolDuration
        
    def subcarrier_spacing(self):
        return self._Bandwidth/(self._effective_carriers)
   
    def SamplingFrequeny(self):
        return (2*self._Bandwidth)
   
    def OFDM_SymbolDuration(self):
        return self._samplingTime * (self._effective_carriers)
    
    def OFDM_GuardDuration(self):
        return (2*self._guard_carriers * self._samplingTime)

   