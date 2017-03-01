from common import SeleniumLib
from selenium.webdriver.common.keys import Keys
import time

class Slack(object):

    def __init__(self, driver, wait_time=20):
        self.driver = driver
        self.wait_time = wait_time
        self.selenium_lib = SeleniumLib(self.driver, self.wait_time)

    def auth (self, slack_site, user, password, slack_username):
        driver = self.driver
        try:
            driver.get('http://'+slack_site+'.slack.com')
            elem = driver.find_element_by_id('email')
            elem.send_keys(user)

            elem = driver.find_element_by_id('password')
            elem.send_keys(password)
            self.selenium_lib.wait_for_id_to_be_clickable('signin_btn')
        except:
            return False

        if self.verify_current_user(slack_username) == False:
            return False

        return True



    def change_location(self, destination, type='channel'):
        if type == 'channel':
            #do something for channels to match?
            location_string = 'channel_name'
            destination_string = destination.replace(',','')
            clickme_css_selector = '.channel_name[clickme=true]'
        else:
            location_string = 'member_username'
            destination_string = "@"+destination
            clickme_css_selector = '.member_username[clickme=true]'

        #first try to open the cmd-k dialog
        cmdk_open = False
        tries = 1
        while cmdk_open == False and tries <= 3:
            try:
                self.selenium_lib.wait_for_xpath(".//*[@id='msgs_div']")
                self.selenium_lib.wait_for_css_path_to_be_visible("#msgs_div") ##hella waits..

                elem = self.driver.find_element_by_xpath("//body")
                elem.send_keys(Keys.COMMAND, 'k')
                print 'tried to send cmd-k... try: '+str(tries)

                box = self.driver.find_element_by_xpath("html/body/ts-jumper[@class='active']")
                cmdk_open = True
                print 'found box to be open!'
                time.sleep(1)
            except Exception as e:
                time.sleep(2)
                print "didn't get to open the box"

        if cmdk_open == False: #didn't open the switcher
            return False

        #try to locate the desired place
        try:
            print 'typing location'
            box.send_keys(destination)
            time.sleep(1) #wait for autocomplete
            path = "//span[@class='"+location_string+"'][text()='"+destination+"']"
            print 'selecting location: '+path
            self.selenium_lib.wait_for_xpath_to_be_clickable(path)
            print 'can click... but selenium is limited here'
            elem = self.driver.find_element_by_xpath(path)

            print 'got elem... setting temp attribute and clicking'

            self.driver.execute_script("arguments[0].setAttribute('clickme','true')", elem)
            self.driver.execute_script("arguments[0].setAttribute('style','border:3px solid black')", elem)
            print 'set attribute... now clicking'

            self.driver.execute_script("el = document.querySelector('"+clickme_css_selector+"'); el.click();")

            time.sleep(1) #wait for the channel to change
            current_location = self.driver.find_element_by_id('channel_name').text.strip('#')
            if current_location == destination_string:
                return True
            else:
                print 'current_location: '+current_location
                #print 'should have changed to '+destination
                print 'destination_string '+destination_string
                return False

        except Exception as e:
            print e
            print "couldn't change channel to "+destination
            return False

    def type_message(self, message):
        try: #type the right thing
            self.selenium_lib.wait_for_xpath_to_be_clickable(".//*[@id='msg_input']")

            elem = self.driver.find_element_by_id('msg_input')
            elem.send_keys(message)
            elem.send_keys(Keys.RETURN)

        except:
            print "couldn't type message to butter"
            return False

    def verify_current_user(self, slack_username):
        try: #testing to see if we're logged in right
            self.selenium_lib.wait_for_text_in_xpath(".//*[@id='team_menu_user_name']", slack_username)
            print "found username: " + slack_username
        except:
            print "couldn't find username: "+ slack_username
            return False

    def verify_last_responder(self, butter_username):
        try: #make sure we get a response
            self.selenium_lib.wait_for_text_in_css_path("div.day_container:last-child ts-message:last-child a.message_sender", butter_username)
            print 'responded!'
        except:
            print "didn't get a response back from "+butter_username
            return False

    def verify_last_response(self,response):
        try:
            self.selenium_lib.wait_for_text_in_css_path("div.day_container:last-child ts-message:last-child span.message_body",response)
            print 'expected response "'+response+'" and got it'
            return True
        except:
            print "didn't get expected response: "+response
            return False

    def verify_attachment_named(self, filename, position='1'):
        try:
            self.selenium_lib.wait_for_text_in_css_path('div.day_container:last-child ts-message:last-child span.message_body div.inline_attachment[data-attachment-id="'+position+'"] div.msg_inline_attachment_row:first-child b:first-child',filename)
            print 'responded properly with '+filename
        except:
            print "didn't get dm response from butter when requesting a channel search for: "+filename
            return False

    def verify_team_attachment_named(self, filename):
        try:
            self.selenium_lib.wait_for_text_in_css_path('div.day_container:last-child ts-message:nth-last-child(3) span.message_body div.inline_attachment[data-attachment-id="1"] div.msg_inline_attachment_row:first-child b:first-child a',filename)
            print 'responded properly with '+filename
        except Exception as e:
            print "\n\n"+str(e)+"\n\n"
            print "didn't get file from butter when requesting : "+filename
            return False


    def click_attachment_button(self):
        try:
            self.selenium_lib.wait_for_css_path_to_be_clickable('div.day_container:last-child ts-message:last-child span.message_body div.inline_attachment[data-attachment-id="1"] div.attachment_actions button.btn_attachment')
            print "clicked a dm button to share a result to a channel"
        except:
            print "didn't get response"
            return False

    def click_share_button(self):
        try:
            self.selenium_lib.wait_for_css_path_to_be_clickable('div.day_container:last-child ts-message:last-child span.message_body div.inline_attachment:last-child button.btn_attachment:first-child')
            print "clicked a dm button to share a result to a channel"
        except:
            print "didn't click button"
            return False

    def click_feedback_button(self):
        try:
            self.selenium_lib.wait_for_css_path_to_be_clickable('div.day_container:last-child ts-message:last-child span.message_body div.inline_attachment:last-child button.btn_attachment:first-child')
            print "clicked a feedback button"
        except:
            print "didn't click button"
            return False

        try:
            # make sure it worked
            time.sleep(3)
            attrib = self.selenium_lib.get_attribute_in_css_path("div.day_container:last-child ts-message:last-child span.message_body div.inline_attachment:last-child div.column_border",'style')
            if attrib == 'background-color: rgb(76, 175, 80);':
                print "feedback button success: "+attrib
                return True
            else:
                print "feedback button failure: "+attrib
                return False
        except:
            print "feedback button failed"
            return False


    def logout(self):
        driver = self.driver
        self.selenium_lib.wait_for_id_to_be_clickable('team_menu')
        self.selenium_lib.wait_for_xpath_to_be_clickable(".//*[@id='logout']/a")
