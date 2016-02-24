#!/usr/bin/python

import httplib
import httplib2
import os
from time import sleep

from apiclient import *
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


class Youtube:
    def __init__(self, clientid, clientsecret):
        print "Starting Youtube...",
        self.clientid = clientid
        self.clientsecret = clientsecret

        httplib2.RETRIES = 1  # We handle the retries
        self.MAX_RETRIES = 10

        self.EXCEPTION_LIST = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                               httplib.IncompleteRead, httplib.ImproperConnectionState,
                               httplib.CannotSendRequest, httplib.CannotSendHeader,
                               httplib.ResponseNotReady, httplib.BadStatusLine)  # Retry on Exceptions

        self.STATUS_LIST = [500, 502, 503, 504]  # Retry on codes

        self.CLIENT_SECRETS_FILE = "client_secrets.json"

        self.YOUTUBE_SCOPES = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube "\
                              "https://www.googleapis.com/auth/youtube.force-ssl https://www.googleapis.com/auth/" \
                              "youtubepartner"
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

        self.MISSING_CLIENT_SECRETS_MESSAGE = "ERROR: clients_secrets.json not filled out %s" \
                                              % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                             str(self.CLIENT_SECRETS_FILE)))
        self.VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

        print "Done"

    def get_authenticated_service(self, argss, type="upload"):
        print "Authenticating... ",

        flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
                                       scope=self.YOUTUBE_SCOPES,
                                       message=self.MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage("youtube-oauth2.json")
        credentials = storage.get()

        print "Done\ngetting new values...",

        flow.client_secret = str(self.clientsecret)
        flow.client_id = str(self.clientid)

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage, argss)

        print "Done"
        return discovery.build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                               http=credentials.authorize(httplib2.Http()))

    def initialize_upload(self, youtubes, options):
        tags = None
        if options.keywords:
            tags = options.keywords.split(",")
        print "Starting upload...",
        body = dict(
            snippet=dict(
                title=options.title,
                description=options.description,
                tags=tags,
                categoryId=options.category
            ),
            status=dict(
                privacyStatus=options.privacyStatus
            )
        )
        insert_request = youtubes.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=http.MediaFileUpload(options.file,
                                            chunksize=-1,
                                            resumable=True))

        print "Uploading now...",

        idman = str(self.resumable_upload(insert_request))

        print "Done\nDone\nDone"

        return idman

    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print "Uploading video..."
                status, response = insert_request.next_chunk()
                if 'id' in response:
                    print "Video id '%s' was successfully uploaded." % response['id']
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
            except HttpError, tries:
                if tries.resp.status in self.STATUS_LIST:
                    error = "A un-reliable HTTP error %d occurred:\n%s" % (tries.resp.status, tries.content)
                else:
                    raise
            except self.EXCEPTION_LIST, err:
                error = "A retrying error occurred: %s" % str(err)

            if error is not None:
                print error
                retry += 1
                if retry > self.MAX_RETRIES:
                    exit("To many attempts to upload to youtube...\nquiting...")
                sleep_seconds = 23 * (2 ** retry)
                print "Sleeping %f seconds and then retrying..." % sleep_seconds
                sleep(sleep_seconds)
        return response['id']

    def pre_delete_video(self, youtubes, id):
        #videos_list_response = youtubes.videos().list(id=id, part='snippet').execute()

        #if not videos_list_response["items"]:
        #    exit("Video '%s' was not found. On Scope: %s") % (id, self.YOUTUBE_DELETE_SCOPE)

        # Since the request specified a video ID, the response only contains one
        # video resource. This code extracts the snippet from that resource.
        #videos_list_snippet = videos_list_response["items"][0]["snippet"]

        # Update the video resource by calling the videos.update() method.
        videos_update_response = youtubes.videos().delete(id=id)
        print videos_update_response.execute()

    def upload_video(self, files, title="video", description="description", category="22", keywords="",
                     privacy="public"):
        argparser.add_argument("--file")
        argparser.add_argument("--title")
        argparser.add_argument("--description")
        argparser.add_argument("--category")
        argparser.add_argument("--keywords")
        argparser.add_argument("--privacyStatus", choices=self.VALID_PRIVACY_STATUSES)
        arguments = ["--file=" + files, "--title=" + title, "--description=" + description, "--category=" + category,
                     "--keywords=" + keywords, "--privacyStatus=" + privacy]
        args = argparser.parse_args(arguments)

        if not os.path.exists(args.file):
            exit("Error finding video file exiting...")

        tempyou = self.get_authenticated_service(args)

        videoid = None

        try:
            videoid = self.initialize_upload(tempyou, args)
            print "Done uploading... Success!"
        except HttpError, error:
            print "A connection error (%d) occured: %s " % (error.resp.status, error.content)
            exit("Error uploading.....")

        return videoid

    def delete_video(self, videoid):

        argparser.add_argument("--video-id")

        arguments = ["--video-id=" + videoid]

        args = argparser.parse_args(arguments)

        tempyou = self.get_authenticated_service(args)

        #try:
        self.pre_delete_video(tempyou, videoid)
        print "Done deleting... Success!"
        #except HttpError, error:
            #print "A connection error (%d) occured: %s " % (error.resp.status, error.content)
            #exit("Error deleting.....")
