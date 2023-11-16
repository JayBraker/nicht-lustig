# SPDX-FileCopyrightText: 2023-present Josha Bartsch <>
#
# SPDX-License-Identifier: MIT
from flask import Flask


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_envvar("NICHT_LUSTIG_CONFIG")


    from nicht_lustig.views import nicht_lustig_archive

    app.register_blueprint(nicht_lustig_archive)

    return app
