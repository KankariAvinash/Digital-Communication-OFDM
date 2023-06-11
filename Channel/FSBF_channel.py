#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Johannes Demel.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np


def db2lin(v):
    return 10. ** (v / 10.)


def get_complex_noise_vector(vec_len, sigma=1., dtype=np.complex64):
    """ Get complex random vector with variance sigma**2

    We use standard deviation.
    It translates to noise power (variance) with sigma ** 2
    :param vec_len: number of complex noise samples
    :param sigma: standard deviation of noise.
    :return: complex random vector
    """
    # we expect a complex value, needs to be split for I and Q
    dev = np.sqrt(.5) * sigma
    noise = np.random.normal(0.0, dev, [2, vec_len])
    return (noise[0] + 1.j * noise[1]).astype(dtype)


class channel(object):
    def __init__(self, channel_type='FSBF', oversampling_factor=20):
        channel_type = channel_type.upper()
        assert channel_type in ('AWGN', 'FSBF')
        self._channel_type = channel_type
        self._oversampling_factor = oversampling_factor

        self._pdp = np.array([1, 0.472366552741015, 0.223130160148430, 0.105399224561864, 0.0497870683678639,
                              0.0235177458560091, 0.0111089965382423, 0.00524751839918138, 0.00247875217666636, 0.00117087962079117])
        self._pdp /= np.sqrt(np.sum(self._pdp.real ** 2 + self._pdp.imag ** 2))
        # haha we don't have a random channel. Pff
        self._channel_state = get_complex_noise_vector(self._pdp.size)
        self._taps = self._channel_state * self._pdp
        self.update_oversampled_taps()

    def update_oversampled_taps(self):
        self._oversampled_taps = np.zeros(
            self._taps.size * self._oversampling_factor, dtype=self._taps.dtype)
        self._oversampled_taps[::self._oversampling_factor] = self._taps

    def update_channel_state(self):
        self._channel_state = get_complex_noise_vector(self._pdp.size)

    def update_channel_taps(self):
        self._taps = self._channel_state * self._pdp

    def step(self):
        self.update_channel_state()
        self.update_channel_taps()
        self.update_oversampled_taps()

    def _transmit(self, tx_symbols, snr_db):
        self.step()
        rx = np.convolve(tx_symbols, self._oversampled_taps,
                         'full')  # [0:tx_symbols.size]
        noise = get_complex_noise_vector(rx.size, 1. / db2lin(snr_db))
        return rx + noise

    def transmit(self, tx_symbols, snr_db):
        if tx_symbols.ndim == 1:
            return self._transmit(tx_symbols, snr_db)
        else:
            return np.array([self._transmit(s, snr_db) for s in tx_symbols])


def FSBF_simulate_channel(tx_symbols, snr_db, oversampling_factor,channel_type='FSBF'):
    return channel(channel_type, oversampling_factor).transmit(tx_symbols, snr_db)
