from gmail import Gmail
from time import sleep


class YoutubeCheck:
    def __init__(self, users, passes):
        print "Started youtube checker....",
        self.gmail = Gmail()
        self.user = users
        self.password = passes
        self.emails = []
        self.lastNum = None
        self.arguments = None
        print "Done"

        self.set_args(sender="accounts-noreply@youtube.com", unread=True)

    @staticmethod
    def delete_email(emaillist):
        for email in emaillist:
            email.delete()

    def set_args(self, **kwargs):
        print "Attempting to start gmail (args)...",
        self.arguments = kwargs
        print "Done"

    def get_emails(self):
        return self.gmail.inbox().mail(self.arguments)

    def check_videos(self):
        self.login()
        sleep(1)
        print "Trying to check if new emails have been sent...",
        self.emails = []
        emailss = (self.get_emails())
        if len(emailss) == 0:
            return [0]
        print "Done"
        for email in emailss:
            subject = email.subject
            if '"' in subject:
                if '"' in subject[subject.index("\"")+1:]:
                    print "Found copyrighted video...",
                    videoname = str(subject[subject.index("\"")+1:][:subject.index("\"")]).replace("\"", "")
                    self.emails.append(videoname)
                    print "Done"
        self.delete_email(emailss)
        return self.emails

    def login(self):
        self.gmail.login(self.user, self.password)

    def logout(self):
        self.gmail.logout()


if __name__ == "__main__":
    checker = YoutubeCheck("pseudonymous.coders@gmail.com", "criwasfirst")
    print checker.check_videos()