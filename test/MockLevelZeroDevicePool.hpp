/*
 * Copyright (c) 2015 - 2021, Intel Corporation
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in
 *       the documentation and/or other materials provided with the
 *       distribution.
 *
 *     * Neither the name of Intel Corporation nor the names of its
 *       contributors may be used to endorse or promote products derived
 *       from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY LOG OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef MOCKLEVELZERODEVICEPOOL_HPP_INCLUDE
#define MOCKLEVELZERODEVICEPOOL_HPP_INCLUDE

#include "gmock/gmock.h"

#include "LevelZeroDevicePool.hpp"

class MockLevelZeroDevicePool : public geopm::LevelZeroDevicePool
{
    public:
        MOCK_METHOD(num_accelerator,
                    int(int), (const, override));

        MOCK_METHOD(frequency_status,
                    double(int, unsigned int, int), (const, override));
        MOCK_METHOD(frequency_min,
                    double(int, unsigned int, int), (const, override));
        MOCK_METHOD(frequency_max,
                    double(int, unsigned int, int), (const, override));

        MOCK_METHOD(active_time,
                    uint64_t(int, unsigned int, int), (const, override));
        MOCK_METHOD(active_time_timestamp,
                    uint64_t(int, unsigned int, int), (const, override));

        MOCK_METHOD(power_limit_tdp,
                    int32_t(int, unsigned int, int), (const, override));
        MOCK_METHOD(power_limit_min,
                    int32_t(int, unsigned int, int), (const, override));
        MOCK_METHOD(power_limit_max,
                    int32_t(int, unsigned int, int), (const, override));

        MOCK_METHOD(energy,
                    uint64_t(int, unsigned int, int), (const, override));
        MOCK_METHOD(energy_timestamp,
                    uint64_t(int, unsigned int, int), (const, override));

        MOCK_METHOD(frequency_control,
                    void(int, unsigned int, int, double),
                    (const, override));
};

#endif
