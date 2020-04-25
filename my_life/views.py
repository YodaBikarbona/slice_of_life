# Google drive api
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import json
import django
import datetime
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .models import (
    User,
    Image,
    Post,
    ImageComment,
    PostComment
)
from .validators import (
    Validation
)
from .helper import (
    error_handler,
    new_psw,
    check_valid_limit_and_offset,
    tag_grouping
)
from .serializers import (
    UserSerializer,
    ImageSerializer,
    PostSerializer,
    ImageCommentSerializer,
    PostCommentSerializer
)


@api_view(['POST'])
def login(request):
    body = request.data
    if not Validation.login_validation(data=body):
        return error_handler(error_status=400, message=f'Wrong data!')
    user = User.get_user_by_username(username=body['username'])
    if not user:
        return error_handler(error_status=404, message='User not found!')
    if user.blocked:
        return error_handler(error_status=403, message='User has blocked!')
    if user.password != new_psw(salt=user.salt, password=body['password']):
        return error_handler(error_status=403, message='User or password is wrong!')
    token = user.security_token()
    user = UserSerializer(many=False, instance=user).data
    user['token'] = token
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'User is successfully logged!',
                'result': user
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_gallery(request):
    images = Image.get_all_photo_gallery()
    images = ImageSerializer(many=True, instance=images).data
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Images',
                'results': images
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_image(request, id):
    try:
        int(id)
    except ValueError as ex:
        print(ex)
        return error_handler(error_status=400, message='Bad data!')
    image = Image.get_image_by_unique_id(id=id)
    if not image:
        return error_handler(error_status=404, message=f'Not found!')
    image.increase_views()
    comments = ImageComment.get_comments_by_image_id(image_id=image.id)
    image = ImageSerializer(many=False, instance=image).data
    comments = ImageCommentSerializer(many=True, instance=comments).data
    image['comments'] = comments
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Image',
                'result': image
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_next_image(request, id):
    try:
        int(id)
    except ValueError as ex:
        print(ex)
        return error_handler(error_status=400, message='Bad data!')
    image = Image.get_image_by_unique_id(id=id)
    if not image:
        return error_handler(error_status=404, message=f'Not found!')
    next_image = Image.get_next_image(image_id=image.id)
    if not next_image:
        return error_handler(error_status=404, message=f'Not found!')
    next_image.increase_views()
    comments = ImageComment.get_comments_by_image_id(image_id=next_image.id)
    next_image = ImageSerializer(many=False, instance=next_image).data
    comments = ImageCommentSerializer(many=True, instance=comments).data
    next_image['comments'] = comments
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Image',
                'result': next_image
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_previous_image(request, id):
    try:
        int(id)
    except ValueError as ex:
        print(ex)
        return error_handler(error_status=400, message='Bad data!')
    image = Image.get_image_by_unique_id(id=id)
    if not image:
        return error_handler(error_status=404, message=f'Not found!')
    next_image = Image.get_previous_image(image_id=image.id)
    if not next_image:
        return error_handler(error_status=404, message=f'Not found!')
    next_image.increase_views()
    comments = ImageComment.get_comments_by_image_id(image_id=next_image.id)
    next_image = ImageSerializer(many=False, instance=next_image).data
    comments = ImageCommentSerializer(many=True, instance=comments).data
    next_image['comments'] = comments
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Image',
                'result': next_image
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_home_posts(request):
    posts = Post.get_home_posts()
    posts = PostSerializer(many=True, instance=posts).data
    for post in posts:
        post['content'] = post['content'].replace('\r', '')
        post['content'] = post['content'][:1555] + '...'
        res = tag_grouping(post['content'], True)
        post['content'] = res
        date = post['created'].split('T')[0].split('-')
        date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
        post['created'] = date.strftime("%b %d %Y")
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Posts',
                'results': posts
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_posts(request):
    query_string = request.GET
    limit = query_string['limit'] if 'limit' in query_string else None
    offset = query_string['offset'] if 'offset' in query_string else None
    limit, offset = check_valid_limit_and_offset(limit=limit, offset=offset)
    posts = Post.get_posts(offset=offset, limit=limit)
    posts_number = Post.count_posts()
    posts = PostSerializer(many=True, instance=posts).data
    for post in posts:
        post['content'] = post['content'].replace('\r', '')
        post['content'] = post['content'][:1555] + '...'
        res = tag_grouping(post['content'], True)
        post['content'] = res
        date = post['created'].split('T')[0].split('-')
        date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
        post['created'] = date.strftime("%b %d %Y")
        post['posts_number'] = posts_number
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Posts',
                'results': posts
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_post(request, id):
    try:
        int(id)
    except ValueError as ex:
        print(ex)
        return error_handler(error_status=400, message='Bad data!')
    post = Post.get_post_by_unique_id(id=id)
    if not post:
        return error_handler(error_status=404, message=f'Not found')
    post.increase_views()
    comments = PostComment.get_comments_by_post_id(post_id=post.id)
    post = PostSerializer(many=False, instance=post).data
    date = post['created'].split('T')[0].split('-')
    date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    post['created'] = date.strftime("%b %d %Y")
    res = tag_grouping(post['content'], True)
    post['content'] = res
    comments = PostCommentSerializer(many=True, instance=comments).data
    post['comments'] = comments
    for i in post['content']:
        print(i)
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Image',
                'result': post
            }
        ),
        content_type='application/json',
        status=200
    )


# Google drive api

# # If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
#
#
# def main():
#     """Shows basic usage of the Drive v3 API.
#     Prints the names and ids of the first 10 files the user has access to.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'client_secret_266918615164-0v4sfqieu6rbcd9a0d7e3j5ltrgqtic0.apps.googleusercontent.com.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('drive', 'v3', credentials=creds)
#
#     # Call the Drive v3 API
#     results = service.files().list(
#         pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#
#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(u'{0} ({1})'.format(item['name'], item['id']))


# import httplib2
# import os, io
#
# from apiclient import discovery
# from oauth2client import client
# from oauth2client import tools
# from oauth2client.file import Storage
# from apiclient.http import MediaFileUpload, MediaIoBaseDownload
# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None
# import auth
# # If modifying these scopes, delete your previously saved credentials
# # at ~/.credentials/drive-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/drive'
# CLIENT_SECRET_FILE = 'client_secret.json'
# APPLICATION_NAME = 'Drive API Python Quickstart'
# authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
# credentials = authInst.getCredentials()
#
# http = credentials.authorize(httplib2.Http())
# drive_service = discovery.build('drive', 'v3', http=http)
#
# def listFiles(size):
#     results = drive_service.files().list(
#         pageSize=size,fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print('{0} ({1})'.format(item['name'], item['id']))
#
# def uploadFile(filename,filepath,mimetype):
#     file_metadata = {'name': filename}
#     media = MediaFileUpload(filepath,
#                             mimetype=mimetype)
#     file = drive_service.files().create(body=file_metadata,
#                                         media_body=media,
#                                         fields='id').execute()
#     print('File ID: %s' % file.get('id'))
#
# def downloadFile(file_id,filepath):
#     request = drive_service.files().get_media(fileId=file_id)
#     fh = io.BytesIO()
#     downloader = MediaIoBaseDownload(fh, request)
#     done = False
#     while done is False:
#         status, done = downloader.next_chunk()
#         print("Download %d%%." % int(status.progress() * 100))
#     with io.open(filepath,'wb') as f:
#         fh.seek(0)
#         f.write(fh.read())
#
# def createFolder(name):
#     file_metadata = {
#     'name': name,
#     'mimeType': 'application/vnd.google-apps.folder'
#     }
#     file = drive_service.files().create(body=file_metadata,
#                                         fields='id').execute()
#     print ('Folder ID: %s' % file.get('id'))
#
# def searchFile(size,query):
#     results = drive_service.files().list(
#     pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
#     items = results.get('files', [])
#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(item)
#             print('{0} ({1})'.format(item['name'], item['id']))
# #uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
# #downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')
# #createFolder('Google')
# searchFile(10,"name contains 'Getting'")


