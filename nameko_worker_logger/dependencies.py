# Written by Vladimir Provalov <vladimir.provalov@emlid.com>
#
# Copyright (c) 2018, Emlid Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms,
# with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging

from nameko.extensions import DependencyProvider


def _worker_ctx_to_dict(worker_ctx):
    return {
        'call_id': worker_ctx.call_id,
        'method_name': worker_ctx.entrypoint.method_name,
        'service_name': worker_ctx.service_name
    }


def _exception_info_to_dict(exc_info):
    exc_type, msg, traceback = exc_info
    return {'type': exc_type, 'message': msg, 'traceback': traceback}


class WorkerLogger(DependencyProvider):
    """Logs exceptions and provides logger with worker's contextual info."""

    def __init__(self, logger_name):
        """:param logger_name: name of logger instance."""
        self.logger = logging.getLogger(logger_name)

    def get_dependency(self, worker_ctx):
        """Create logger adapter with worker's contextual data."""
        worker_info = {'worker': _worker_ctx_to_dict(worker_ctx)}
        adapter = logging.LoggerAdapter(self.logger, extra=worker_info)
        return adapter

    def worker_result(self, worker_ctx, result=None, exc_info=None):
        """Log exception info, if it is present."""
        if exc_info is None:
            return
        exception_info = {'exception_info': _exception_info_to_dict(exc_info)}
        worker_info = {'worker': _worker_ctx_to_dict(worker_ctx)}
        self.logger.error(exception_info, extra=worker_info)
