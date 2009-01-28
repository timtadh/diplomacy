#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

user_manager.logout_session()

ses_dict, user_dict = user_manager.init_user_session()

templater.print_template("templates/logout.html", {'target_page':'main.py'})
