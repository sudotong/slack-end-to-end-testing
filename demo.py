"""
Run periodically to share a file
Don't forget to add geckodriver to your path
"""
import sys
import os

from selenium_lib.driverfactory import DriverFactory
from selenium_lib.slack import Slack

class Scripter():
    def __init__(self):
        self.driverfactory = DriverFactory()
        self.driver = self.driverfactory.get_driver()


    def do_something_scripted(self):
        slack = Slack(self.driver)

        authed_slack_site = 'ppcrew'
        authed_user_email = 'russhanneman@ojacko.com'
        authed_user_pass = '2PaK{7yUmZDGqGbB'
        authed_user_name = 'russ_hanneman'
        slack.auth(authed_slack_site, authed_user_email, authed_user_pass, authed_user_name)

        if slack.verify_current_user(authed_user_name) == False:
            return False

        if slack.change_location('butter-stage', 'user') == False:
            return False

        if slack.type_message("abc123") == False:
            return False

        if slack.verify_last_response('def456') == False:
            return False

        if slack.verify_last_responder('butter-stage') == False:
            return False
        """
        if self.verify_attachment_named('King James Bible Full Text.txt') == False:
            return False

        if slack.click_share_button() == False:
            return False

        if slack.click_attachment_button() == False:
            return False

        if slack.click_feedback_button() == False:
            return False
        """
        slack.logout()
        return True

    def terminate_drivers(self):
        self.driverfactory.terminate_drivers()


if __name__ == "__main__":
    scripter = Scripter()

    if scripter.do_something_scripted():
        print "success"
    else:
        print "failure"

    scripter.terminate_drivers()
