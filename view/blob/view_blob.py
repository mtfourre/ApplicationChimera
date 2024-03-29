from Chimera.models import Blob, Album, User, ProfilePhoto
from Chimera.utils import blob_to_dict
from django.http import HttpResponse
from Chimera.results import Result
from json import dumps, loads


def blob(request):  # /blob/view
    if request.method == 'POST':
        body = loads(request.body)

        blob_id = body.get('blob_id')
        user_id = body.get('user_id')
        album_id = body.get('album_id')
        count = body.get('count')

        if not (blob_id or album_id or user_id):
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        if blob_id:
            try:
                current_blob = Blob.objects.get(pk=blob_id)
            except Blob.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            except Blob.MultipleObjectsReturned:
                response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
                return HttpResponse(response, content_type='application/json')
            response = {'blob': blob_to_dict(current_blob)}
            Result.append_result(response, Result.SUCCESS)
        elif user_id:
            try:
                user = User.objects.get(pk=user_id)
                profile_photo = ProfilePhoto.objects.get(user=user)
            except User.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            except ProfilePhoto.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            blobs = Blob.objects.filter(album=profile_photo.album)
            if blobs.count() < 1:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            response = {'blob': blob_to_dict(blobs[0])}
            Result.append_result(response, Result.SUCCESS)
        elif album_id:
            try:
                album = Album.objects.get(pk=album_id)
            except Album.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            blobs = Blob.objects.filter(album=album)
            if blobs.count() < 1:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')

            blob_list = []
            response = {}

            if count:
                count = int(count)
                if count > blobs.count():
                    for blob_entry in blobs:
                        blob_list.append(blob_to_dict(blob_entry))
                    Result.append_result(response, Result.BLOB_COUNT_INVALID)
                elif count <= 0:
                    for blob_entry in blobs:
                        blob_list.append(blob_to_dict(blob_entry))
                    Result.append_result(response, Result.SUCCESS)
                else:
                    i = 0
                    for blob_entry in blobs:
                        if i < count:
                            blob_list.append(blob_to_dict(blob_entry))
                            i += 1
                        else:
                            break
                    Result.append_result(response, Result.SUCCESS)
            else:
                for blob_entry in blobs:
                    blob_list.append(blob_to_dict(blob_entry))
                Result.append_result(response, Result.SUCCESS)

            response['blobs'] = blob_list
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
