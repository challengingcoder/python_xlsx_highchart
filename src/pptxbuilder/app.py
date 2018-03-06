import os

from flask import Flask, url_for
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

from pptxbuilder.config import config_get_section

this_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__,
            template_folder=os.path.join(this_dir, 'templates'),
            static_folder=os.path.join(this_dir, 'static'))


def __flask_setup():
    # Flask config
    for k, v in config_get_section('APP').items():
        app.config[k] = v

    CSRFProtect(app)

    app.config['SESSION_FILE_DIR'] = os.path.join(this_dir, '..', '..', 'flask_session')
    Session(app)


def __web_setup():
    # Register blueprints
    from pptxbuilder.views import home_bp, builder_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(builder_bp)

    # gettext for future i18n needs
    from gettext import gettext
    app.jinja_env.globals['_'] = gettext

    def s_url_for(path, file):
        # A helper to serve assets with version numbers.

        st_file = os.path.join(this_dir, 'static', path, file)
        if os.path.exists(st_file):
            file_last_mod = os.path.getmtime(st_file)
            path = url_for('static', filename='{}/{}'.format(path, file), v=str(int(file_last_mod)))
        else:
            path = url_for('static', filename='{}/{}'.format(path, file))

        return path

    app.jinja_env.globals['s_url_for'] = s_url_for


def __run_server():
    # Run development server
    email = os.environ.get('BUG_EMAIL')
    password = os.environ.get('BUG_EMAIL_PASSWORD')
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, threaded=True)


__flask_setup()
__web_setup()


def main():
    __run_server()


if __name__ == '__main__':
    main()
