from app import rc_app, fm
from flask import render_template, url_for, jsonify, request
import os
from app.models.video_manager import parse_video

@rc_app.route('/')
def index_page():
	# image_path = 'app/datacenter/images/dog.jpg'
	# image_path = os.path.join(rc_app.root_path, 'datacenter', 'images', 'dog.jpg')
	# image_path = url_for('static', filename='datacenter/images/dog.jpg')
	image_path = url_for('static', filename='image/rapidlabeling.png')
	
	return render_template('lending.html', image_path=image_path)

@rc_app.route('/make_dir', methods=['POST'])
def make_dir():
	if request.method == 'POST':
		to_client = {}
		new_hashid = fm.make_new_hashid()
		to_client['new_hashid'] = new_hashid
		new_folder_path = fm.make_datacenter_path(new_hashid, request.form['username'], request.form['frame_step'])

		f = request.files['file']
		print("f : ", f)
		print("f.filename : ", f.filename)
		ext = f.filename.split('.')[-1]
		if ext == "mp4" or ext == "avi":
			video_path = os.path.join(new_folder_path, "video_{}.{}".format(new_hashid, ext))
			f.save(video_path)
			to_client['file_save_status'] = True
			dc = fm.get_data_controllor(new_hashid)
			parse_video(video_path, "video_{}".format(new_hashid), dc.infomation_json['images_folder_path'], int(request.form['frame_step']))
		else:
			to_client['file_save_status'] = False
		to_client['new_folder_path'] = new_folder_path

	return jsonify(to_client)


