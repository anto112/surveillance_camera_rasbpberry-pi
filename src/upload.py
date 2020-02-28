import dropbox

TOKEN = 'FvWjZpwuN3AAAAAAAAAQm8R3Boawpu2da8jaVeggE97mYgWkcvLHrQuo6g7LSdp6'


def upload_images(image_name):
    name_file = image_name + ".jpeg"
    dbx = dropbox.Dropbox(TOKEN)
    uploadPath = "C:/Users/Haryanto/Documents/smart-security-camera/" + name_file
    # Read in file and upload
    with open(uploadPath, 'rb') as f:
        print("Uploading " + name_file + " to Dropbox ...")

        dbx.files_upload(f.read(), "/" + name_file, mute=True)
    f.close()
