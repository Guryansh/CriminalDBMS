from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ProfileForm
from .models import Profile, User
import base64, cv2, os
import numpy as np
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
    context = {'page': page}
    return render(request, 'login.html', context)

def create_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        gender = request.POST.get('gender')
        dob = request.POST.get('date')
        pob = request.POST.get('pob')
        nation = request.POST.get('nation')
        gname = request.POST.get('gname')
        wby = request.POST.get('wby')
        ctype = request.POST.get('ctype')
        body_marks = request.POST.get('body_marks')
        folder_name = str(Profile.objects.all().count()+1)

        folder_path = os.path.join('static', 'profiles', folder_name)
        folder_path2 = os.path.join('static', 'pics', folder_name)
        os.makedirs(folder_path)
        os.makedirs(folder_path2)

        photo_data = request.POST['photo_data']
        img_data = base64.b64decode(photo_data.split(',')[1])

        nparr = np.frombuffer(img_data, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite('%s/%s.jpg' % (folder_path2, name), img_np)

        algo = os.path.join('static', 'haarcascade/haarcascade_frontalface_default.xml')
        haar_cascade = cv2.CascadeClassifier(algo)
        grayImg = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        face = haar_cascade.detectMultiScale(grayImg, 1.3, 4)
        if len(face) < 1:
            return redirect('create_profile')
        for (x, y, width, height) in face:
            faceOnly = grayImg[y:y + height, x:x + width]

        FACEONLY = np.ascontiguousarray(faceOnly)
        # Generate a unique filename for the image (you can use UUID or timestamp)
        filename = '0'
        filename2 = '1'
        cv2.imwrite('%s/%s.jpg' % (folder_path, filename), FACEONLY)
        cv2.imwrite('%s/%s.jpg' % (folder_path, filename2), FACEONLY)
        profile = Profile(folder_name=folder_name, name=name, alias=alias, gender=gender, dob=dob, POB=pob,
                          Nationality=nation, body_marks=body_marks, gang=gname, wantedby=wby, ctype=ctype).save()
        return render(request, 'success.html')  # Redirect to a success page

    return render(request, 'create_profile.html')


def upload_photo(request):
    if request.method == 'POST' and 'photo_data' in request.POST:
        photo_data = request.POST['photo_data']
        img_data = base64.b64decode(photo_data.split(',')[1])

        # Define the directory where images will be stored
        upload_dir = os.path.join('static', 'scanned_images')

        # Create the directory if it doesn't exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Generate a unique filename for the image (you can use UUID or timestamp)
        filename = 'image.jpg'

        # Save the image to the upload directory
        with open(os.path.join(upload_dir, filename), 'wb') as f:
            f.write(img_data)

        # Construct the URL of the saved image
        image_url = os.path.join(upload_dir, filename).replace('\\', '/')

        haar_cascade = os.path.join('static', 'haarcascade/haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(haar_cascade)
        (images, labels, names, ids) = ([], [], {}, 0)
        (width, height) = (130, 100)
        count = 0
        dataset = os.path.join('static', 'profiles')
        # print('Training...')
        for (subdirs, dirs, files) in os.walk(dataset):
            for subdir in dirs:
                names[ids] = subdir
                subject_path = os.path.join(dataset, subdir)
                for filename in os.listdir(subject_path):
                    path = os.path.join(subject_path, filename)
                    label = ids
                    img = cv2.imread(path, 0)
                    img = cv2.resize(img, (width, height))
                    images.append(img)
                    labels.append(int(label))
                ids += 1

        # list the images and the labels
        (images, labels) = [np.array(img_list) for img_list in [images, labels]]

        # create a model of classifiers
        model = cv2.face.LBPHFaceRecognizer_create()
        # model = cv2.face.FisherFaceRecognizer_create()

        # train the model
        model.train(images, labels)
        nparr = np.frombuffer(img_data, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        grayImg = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        # obtain face coordinates
        faces = face_cascade.detectMultiScale(grayImg, 1.3, 5)
        predicted_names = []
        name = 'Unknown'
        for (x, y, w, h) in faces:
            face = grayImg[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)
            # print(prediction)
            if prediction[1] < 800:
                name = names[prediction[0]]
            else:
                name = 'Unknown'
            predicted_names.append(name)
        queryset = Profile.objects.filter(folder_name__in=predicted_names)
        all_profiles = Profile.objects.all()
        remaining_profiles = all_profiles.difference(queryset)
        context = {
            'result': queryset,
            'others': remaining_profiles
        }
        return render(request, "result.html", context)

    else:
        return JsonResponse({'error': 'Failed to upload photo'}, status=400)


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        gender = request.POST.get('gender')
        dob = request.POST.get('date')
        pob = request.POST.get('pob')
        nation = request.POST.get('nation')
        gname = request.POST.get('gname')
        wby = request.POST.get('wby')
        ctype = request.POST.get('ctype')
        body_marks = request.POST.get('body_marks')
        folder_name = str(name) + str(dob)
        filters = Q()

        if name:
            filters &= Q(name__icontains=name)
        if alias:
            filters &= Q(alias__icontains=alias)
        if gender is not None:
            filters &= Q(gender=gender)
        if dob:
            filters &= Q(dob=dob)
        if pob:
            filters &= Q(POB__icontains=pob)
        if nation:
            filters &= Q(Nationality__icontains=nation)
        if gname:
            filters &= Q(gang__icontains=gname)
        if wby:
            filters &= Q(wantedby__icontains=wby)
        if ctype:
            filters &= Q(ctype__icontains=ctype)
        if body_marks:
            filters &= Q(body_marks__icontains=body_marks)

        # Filter profiles based on the constructed filter conditions
        queryset = Profile.objects.filter(filters)
        all_profiles = Profile.objects.all()
        remaining_profiles = all_profiles.difference(queryset)
        context = {
            'result': queryset,
            'others': remaining_profiles
        }
        return render(request, "result.html", context)
    return render(request, "home.html")

def profile(request,pk):
    if request.method == 'POST' and 'delete_profile' in request.POST:
        Profile.objects.get(id=pk).delete()
        return render(request, 'success.html')  # Redirect to a success page
    try:
        result=Profile.objects.get(id=pk)
    except Exception as e:
        return render(request, 'error.html')
    else:
        context={
        'result':result,
        }
        return render(request, "profile.html", context)

def update(request,pk):
    if request.method == 'POST':
        profile=Profile.objects.get(id=pk)
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        gender = request.POST.get('gender')
        dob = request.POST.get('date')
        pob = request.POST.get('pob')
        nation = request.POST.get('nation')
        gname = request.POST.get('gname')
        wby = request.POST.get('wby')
        ctype = request.POST.get('ctype')
        body_marks = request.POST.get('body_marks')


        profile.name = name
        profile.alias = alias
        profile.gender = gender
        profile.dob = dob
        profile.POB = pob
        profile.Nationality = nation
        profile.body_marks = body_marks
        profile.gang = gname
        profile.wantedby = wby
        profile.ctype = ctype

        # Save the updated profile
        profile.save()
        return redirect('profile',pk)
    try:
        result = Profile.objects.get(id=pk)
    except Exception as e:
        return render(request, 'error.html')
    else:
        context = {
            'result': result,
        }
        return render(request, "update.html", context)