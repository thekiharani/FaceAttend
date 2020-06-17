import cv2
import face_recognition
import numpy as np
import os
from django.conf import settings
from accounts.models import CustomUser
from .models import Attendance


class VideoCamera(object):

    def get_frame(self, lesson):
        video_capture = cv2.VideoCapture(0)
        students = CustomUser.objects.filter(is_instructor=False)
        known_face_encodings = []
        known_face_names = []
        # Load a sample picture and learn how to recognize it.
        for student in students:
            current_image = face_recognition.load_image_file(os.path.join(settings.BASE_DIR, 'media/'+student.face_pic.url.split('/')[2]))
            current_face_encoding = face_recognition.face_encodings(current_image)[0]
            known_face_encodings.append(current_face_encoding,)
            known_face_names.append(student.email)

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        total = 0

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    msg = "Processing..."

                    # If a match was found in known_face_encodings, use the known face with the smallest distance to
                    # the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        student = CustomUser.objects.get(email=name)
                        try:
                            registered = Attendance.objects.get(student_id=student.pk, lesson_id=lesson)
                            msg = 'Success...'
                            path = os.path.join(settings.BASE_DIR, "{}.jpg".format(name))
                            registered.proof = "{}.jpg".format(name)
                            registered.save()
                        except Attendance.DoesNotExist:
                            Attendance.objects.create(student=student, lesson_id=lesson)

                    face_names.append(msg+" : "+name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                crop_img = frame
                cv2.imwrite(os.path.join(settings.BASE_DIR, "media/{}.jpg".format(name.split(':')[1])), crop_img)

                try:
                    student = CustomUser.objects.get(email=name)
                    registered = Attendance.objects.get(student_id=student.pk, lesson_id=lesson)
                    registered.proof = "{}.jpg".format(name)
                    registered.save()
                except Attendance.DoesNotExist:
                    pass
                except CustomUser.DoesNotExist:
                    pass


            # Display the resulting image
            # cv2.imshow('Video', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        video_capture.release()
        cv2.destroyAllWindows()
