# Copyright 2023 Sébastien Demanou. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import argparse
import asyncio
import logging

from oremi.core.logger import Logger

from discovery.package import APP_DESCRIPTION
from discovery.package import APP_NAME
from discovery.package import SERVER_HEADER
from discovery.service import register_discovery_service


def parse_arguments():
  parser = argparse.ArgumentParser(prog = APP_NAME, description = APP_DESCRIPTION)

  parser.add_argument(
    '--service-host',
    type = str,
    help = 'Host address of the Oremi TTS server.',
  )

  parser.add_argument(
    '--service-port',
    type = int,
    help = 'Port number of the Oremi TTS server.',
  )

  parser.add_argument(
    '--supported-languages',
    nargs = '+',
    type = str,
    help = 'List of supported language codes for text-to-speech.',
  )

  parser.add_argument(
    '--discovery-uri',
    type = str,
    help = 'Oremi Discovery URI to connect to.',
  )

  parser.add_argument(
    '--discovery-cert-file',
    type = str,
    help = 'Path to the certificate file to use for the connection.',
  )

  parser.add_argument(
    '--log-file',
    type = str,
    default = None,
    help = 'Name of the log file.',
  )

  parser.add_argument(
    '--verbose',
    action = 'store_true',
    help = 'Enable verbose logging.',
  )

  return parser.parse_args()


async def start() -> None:
  args = parse_arguments()
  verbose: bool = args.verbose
  log_level = logging.DEBUG if verbose else logging.INFO
  logger = Logger.create(APP_NAME, filename = args.log_file, level = log_level)

  logger.info(f'Starting discovery client for {SERVER_HEADER}')
  logger.info(f'Log level {"DEBUG" if logger.level == logging.DEBUG else "INFO"}')

  await register_discovery_service(
    service_host = args.service_host,
    service_port = args.service_port,
    discovery_uri = args.discovery_uri,
    discovery_cert_file = args.discovery_cert_file,
    supported_languages = args.supported_languages,
    logger = logger,
  )


try:
  asyncio.run(start())
except KeyboardInterrupt:
  pass
