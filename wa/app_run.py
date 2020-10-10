import os
import time
import json
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from os import listdir
from os.path import join, isfile
from data.DataAccesObjects import DataAccesObjects as DAO
from flask_socketio import SocketIO
 
 
UPLOAD_FOLDER = '/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/categories'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
 
 
app = Flask(__name__)
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api', methods=['POST', 'GET'])
def index():
    return " api wa version 1.0 " 
 
@app.route('/images', methods=['POST', 'PUT'], endpoint='upload_file')
def upload_file():
    
    if request.method == 'POST':
        for file in request.files.getlist('images'):
            filename_image = file.filename
            filename_path = (filename_image.rsplit('avatar.jpg'))[0]
            #filename_categorie =  (filename_image.rsplit('_'))[1]
            f = open('verificacao.txt', 'w')
            f.write(filename_image+'\n')
            #f.write(filename_path+'\n')
            f.close()
            if os.path.exists('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/'+ filename_categorie + filename_path):
                destination = os.path.join(app.config['UPLOAD_FOLDER'],filename_path)
            else:
                os.makedirs('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/'+ filename_categorie + filename_path)
                destination = os.path.join('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories',filename_categorie, filename_path, filename_image)
            file.save(destination)     
       
        return 'ok', 200





@app.route('/service', methods=['POST', 'PUT'], endpoint='upload_service')
def upload_service():
    if request.method == 'POST':
        for file in request.files.getlist('service'):
            filename_image = file.filename
            filename_path = filename_image.rsplit('_')[0]
            exist_path = '/home/coolbagsafe/apps_wsgi/api_wa/wa/static/images/%s'%filename_path
            f = open('verificacao.txt', 'w')
            f.write(filename_image+'\n')
            f.write(filename_path+'\n')
            f.close()
            if os.path.exists(exist_path):
                destination = os.path.join('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/images',filename_path, filename_image)
            else:
                path_create = os.path.join(app.config['UPLOAD_FOLDER'], filename_path)
                os.makedirs('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/images/%s'%filename_path)
                destination = os.path.join('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/images',filename_path, filename_image)
            file.save(destination)
            
       
        return 'ok', 200

@app.route('/profile', methods=['POST', 'PUT'], endpoint='upload_profile')
def upload_profile():
    path_create = ''
    data_dao = DAO()
    if request.method == 'POST':
        for file in request.files.getlist('profile'):
            filename_image = file.filename
            print('filename_image %s'%filename_image)
            filename_path = filename_image.rsplit('_')[0] + '_' + filename_image.rsplit('_')[1]
            filename_directory =  (filename_image.rsplit('_'))[2]
            print('filename_directory %s' %filename_directory)
            print(filename_image.split('_'))
            key_number = (filename_image.split('_')[-1]).replace('.jpg', '')
            print("key number %s"%key_number)
            exist_path = '/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/%s/%s'%(filename_directory, filename_path)
            #f = open('verificacao.txt', 'w')
            #f.write(filename_image+'\n')
            #f.write(filename_directory+'\n')
            #f.write(filename_path+'\n')
            #f.close()
            if os.path.exists(exist_path):
                destination = os.path.join('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories',filename_directory, filename_path, filename_image)
            else:
                path_create = os.path.join(app.config['UPLOAD_FOLDER'], filename_path)
                os.makedirs('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/%s/%s'%(filename_directory, filename_path))
                destination = os.path.join("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories",filename_directory, filename_path, filename_image)
            file.save(destination)
            photos_str = ''
            photos_dir = os.listdir(os.path.join("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories",filename_directory, filename_path))
            str_photos = ''
            for p in photos_dir:
                str_photos = str_photos + '###' + str(p)
            print("photos_dir %s"%photos_dir)
            data_dao.cadastro_photos_user(filename_path, str(str_photos))
            
            
       
        return 'ok', 200
    
@socketio.on('/chat')
def chat_socket(data):
    prin('recebido json socket: ' + str(data))
    
    
@app.route('/chat', methods=['POST'], endpoint='chat')
def chat():
    data = request.get_json()
    print("data chat %s"%data)
    data_dao = DAO()
    
    file_chat = "%s_%s.txt"%(data['from'],data['to'])
    file_chat2 = "%s_%s.txt"%(data['to'], data['from'])
    if data['from'] in os.listdir("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat"):
        print("VAI GRAVAR......")
        #if file_chat in os.listdir(os.path.join("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat",data['from'])):
        f = open("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat/%s/%s_%s.txt"%(data['from'], data['from'],data['to']), '+a')
        #else if file_chat2 in os.listdir(os.path.join("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat",data['from'])):
        f.write("to: " + data['to']+ " " + "message: " + data['message'] + "\n")
        f.close()
        
    else:
        print("JÁ GRAVOU....")
        os.makedirs("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat/%s"%data['from'])
        f = open("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat/%s/%s_%s.txt"%(data['from'], data['from'],data['to']), '+a')
        f.write("to: " + data['to']+ " " + "message: " + data['message'] + "\n")
        f.close()
        
    if data['to'] in os.listdir("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat"):
        print("GRAVANDO DENOVO....")
        f = open("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat/%s/%s_%s.txt"%(data['to'], data['from'],data['to']), '+a')
        f.write("from: " + data['from'] + " " + "message: " + data['message'] + "\n")
        f.close()
        
    else:
        print("JA GRAVOU DENOVO....")
        os.makedirs("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat/%s"%data['to'])
        f = open("/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/chat/%s/%s_%s.txt"%(data['to'], data['from'],data['to']), '+a')
        f.write("from: " + data['from'] + " " + "message: " + data['message'] + "\n")
        f.close()
    return 'ok',200
            

@app.route('/offerservice', methods=['POST', 'PUT'], endpoint='offer_service')
def offer_service():
    data = request.get_json()
    data_dao = DAO()
    print(data)
    data_json = dict(idUser=data['idUser'], name=data['name'], description=data['description'], dateRegister=data['dateRegister'], categories = data['categories'], subcategories=data['subCategories'], email=data['email'])
    destination = '/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/%s/%s/%s.json'%(data['categories'], data['idUser'], data['idUser'])
    destination_dir = '/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/%s/%s'%(data['categories'], data['idUser'])
    if os.path.exists(destination_dir):
        #print(data_json)
        #print(data['name'])
        #print(data['idUser'])
        #f = open(destination, 'w')
        #json.dump(data, f)
        #f.close()
        ...
    else:
        os.makedirs(destination_dir)
        #print(data_json)
        #print(data['name'])
        #print(data['idUser'])
        #f = open(destination, 'w')
        #json.dump(data, f)
        #f.close()
    data_dao.cadastro_user(data)
       
    return 'ok', 200

@app.route('/deleteimageprofile', methods=['DELETE'], endpoint='deleteimageprofile')
def deleteimageprofile():
    data_dao = DAO()
    data = request.get_json()
    print(data['photos'])
    data_json = dict(photos=data['photos'])
    key_number = (data['photos'].split('_')[-1]).replace('.jpg', '')
    idUser = data['idUser']
    destination =  '/home/coolbagsafe/apps_wsgi/api_wa/wa/' + data['photos']
    os.remove(destination)
    data_dao.delete_photos_user(idUser, key_number)
    return 'ok', 200

@app.route('/searchprof', methods=['POST', 'GET'], endpoint='search_professional')
def search_professional():
    data = request.get_json()
    data_json = dict(categories=data['categories'])
    #destination = '/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/searchprofessional/%s.json'%(data['idUser'])
    destination = '/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/%s'%(data['categories'])
    directories = [ d for d in listdir(destination) ]
    dict_directory = {}
    dir_files = {}
    
    for i in  range(len(directories)):
        
        files = [f for f in listdir(destination +'/'+ directories[i]) if isfile(join((destination+ '/' + directories[i]), f))]
        dict_directory[i] = files
    
    #files_dir =  '/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/%s'%(data['categories'])
    #files = [f for f in listdir(directories) if isfile(join(directories, f))]
    #print("directories ----> %s"%directories)
    print("files ------->>>> %s"%files)
    #print("dir_files =====> %s"%dir_files)
    print("dict_directory ===> %s" %dict_directory)
    arqujson = json.dumps(dict_directory)
    print(arqujson)
    return jsonify({"statuscode":'ok', "data": arqujson})
    



@app.route('/getcategory', methods=['POST', 'GET'], endpoint='get_categories')
def get_categories():
    data = request.get_json()
    print(data['category'])
    data_json = dict(categorie=data['category'])
    data_dao = DAO()
    retorno = data_dao.get_category(data['category'])
    data = {json.dumps(retorno)}
    print(retorno)
    response = app.response_class(response=json.dumps(retorno), status=200, mimetype='application/json')
    return response

@app.route('/avatar', methods=['POST'], endpoint='avatar')
def avatar():
    if request.method == 'POST':
        data_dao = DAO()
        for file in request.files.getlist('avatar'):
            filename_image = file.filename
            image_name = 'avatar.jpg'
            print("filename_image %s"%filename_image)
            full_name = filename_image.rsplit('avatar.jpg')
            full_name = full_name[0].rsplit('_')
            filename_path = full_name[0] + '_' + full_name[1]#(filename_image.rsplit('avatar.jpg'))[0]
            print("filename_path %s"%filename_path)
            filename_categorie =  full_name[2]#(filename_image.rsplit('_'))[1]
            print("filename_categorie %s"%filename_categorie)
            f = open('verificacao.txt', 'w')
            f.write(filename_image+'\n')
            #f.write(filename_path+'\n')
            f.close()
            if os.path.exists('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/'+ filename_categorie +'/avatares/'+ filename_path):
                destination = os.path.join('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories',filename_categorie,'avatares', filename_path, image_name)
            else:
                os.makedirs('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories/'+ filename_categorie + '/avatares/' + filename_path)
                destination = os.path.join('/home/coolbagsafe/apps_wsgi/api_wa/wa/static/profiles/offerservice/categories',filename_categorie,'avatares', filename_path, image_name)
            file.save(destination)
            image_database =  os.path.join('/static/profiles/offerservice/categories',filename_categorie,'avatares', filename_path, image_name)
            data_dao.avatar(filename_path, image_database)
       
        return 'ok', 200
    

@app.route('/getuserdepoimentos', methods=['POST'], endpoint='get_user_depoimentos')
def get_user_depoimentos():
    data_dao = DAO()
    data = request.get_json()
    print("DATA IN GETUSERDEPOIMENTOS %s"%data)
    retorno =  data_dao.get_user_depoimentos(data['idUser'])
    data = {json.dumps(retorno)}
    print(retorno)
    response = app.response_class(response=json.dumps(retorno), status=200, mimetype='application/json')
    return response
    


if __name__ == '__main__':
    socketio.run(app, host='10.15.1.45', port=5000, debug=True)
