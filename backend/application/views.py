from flask import render_template, request, redirect, url_for, flash, jsonify, Blueprint, send_file
from flask_security import auth_required, roles_required, login_required, roles_accepted, current_user, hash_password, verify_password, SQLAlchemyUserDatastore
from .extensions import db, cache
from .models import User, Role, Influencer, Sponsor
from .datastore import user_datastore
from .resources import *
from celery.result import AsyncResult
from .tasks import create_csv
import os

def create_views(app, user_datastore : SQLAlchemyUserDatastore):

    # Home Page Of The Application
    @cache.cached(timeout = 30)
    @app.route('/', methods = ['GET', 'POST'])
    def home():
        return render_template('index.html')
    
    # Registration Page
    @app.route('/user/registration', methods = ['POST'])
    def user_registration():

        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not username or not password or not role in ['Influencer', 'Sponsor']:
            return jsonify({"message": "Invalid Registration Inputs"}), 400
        if user_datastore.find_user(username = username):
            return jsonify({"message": "User Already Exists"}), 400
        
        password_hashed = hash_password(password)
        user = user_datastore.create_user(username = username, password = password_hashed)
        role = user_datastore.find_or_create_role(name = role)
        user_datastore.add_role_to_user(user, role)
        db.session.commit()

        if role == "Influencer":

            name = data.get('name')
            email = data.get('email')
            category = data.get('category')
            reach = data.get('reach')
            description = data.get('description')

            influencer = Influencer(user_id = user.id, name = name, email = email, category = category, reach = reach, description = description)
            user.active = True
            db.session.add(influencer)

        elif role == "Sponsor":

            name = data.get('name')
            email = data.get('email')
            industry = data.get('industry')
            valuation = data.get('valuation')
            description = data.get('description')

            sponsor = Sponsor(user_id = user.id, name = name, email = email, industry = industry, valuation = valuation, description = description)
            user.active = False
            db.session.add(sponsor)

        db.session.commit()
        return jsonify({"message": "User Registered Successfully"}), 200
    
    # Login Page
    @app.route('/user/login', methods = ['POST'])
    def user_login():

        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Invalid Login Inputs"}), 400

        user = user_datastore.find_user(username = username)

        if not user:
            return jsonify({"message": "Invalid Login! User doesn't exist!"}), 400
        
        if 'Sponsor' in [role.name for role in user.roles]:
            if not user.active:
                return jsonify({"message": "Your Account is not yet approved by Admin."}), 403

        if verify_password(password, user.password):
            return jsonify({'token': user.get_auth_token(), 'role': user.roles[0].name, 'username': user.username, 'id': user.id}), 200
        else:
            return jsonify({"message": "Wrong Password"}), 400
        
# Admin Routes------------------------------------------------------------------------------------------------------------------------------
        
    # Admin Dashboard
    @app.route('/admin/dashboard', methods = ['GET'])
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def admin_dashboard():
        return jsonify({"message": "Welcome to Admin Dashboard"})
    
    # Admin Approve New Sponsors [Page]
    @app.route('/admin/new_sponsors', methods = ['GET'])
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def admin_approve_sponsors():

        new_users = User.query.filter_by(active = False).all()

        new_sponsors = []
        for user in new_users:
            if user.roles[0].name == "Sponsor":
                sponsor = Sponsor.query.filter_by(user_id = user.id).first()
                if sponsor:
                    new_sponsors.append(sponsor.to_dict())

        return jsonify({"new_sponsors": new_sponsors}), 200
    
    # Admin All Influencers [Page]
    @app.route("/admin/all_influencers", methods = ['GET'])
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def all_influencers():

        all_influencers = Influencer.query.all()

        return jsonify({"all_influencers": [influencer.to_dict() for influencer in all_influencers]}), 200
    
    # Admin All Sponsors [Page]
    @app.route("/admin/all_sponsors", methods = ['GET'])
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def all_sponsors():

        all_sponsors = Sponsor.query.join(User, Sponsor.user_id == User.id).filter(User.active == True).all()

        return jsonify({"all_sponsors": [sponsor.to_dict() for sponsor in all_sponsors]}), 200
    
    # Admin All Campaigns [Page]
    @app.route("/admin/all_campaigns", methods = ['GET'])
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def all_campaigns():
        
        all_campaigns = Campaign.query.all()

        return jsonify({"all_campaigns": [campaign.to_dict_with_relations() for campaign in all_campaigns]}), 200
    
    # Admin All Ad Requests [Page]
    @app.route("/admin/all_adrequests", methods = ['GET'])
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def all_adrequests():

        all_adrequests = AdRequest.query.all()

        return jsonify({"all_adrequests": [adrequest.to_dict_with_relations() for adrequest in all_adrequests]}), 200
    
    # Admin Flagged Campaigns [Page]
    @app.route("/admin/flagged_campaigns")
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def flagged_campaigns():

        flagged_campaigns = Campaign.query.filter_by(flag_status = "Flagged").all()
        
        return jsonify({"flagged_campaigns": [campaign.to_dict_with_relations() for campaign in flagged_campaigns]}), 200
    
    # Admin Flagged Influencers [Page]
    @app.route("/admin/flagged_influencers")
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def flagged_influencers():

        flagged_influencers = Influencer.query.filter_by(flag_status = "Flagged").all()
        
        return jsonify({"flagged_influencers": [influencer.to_dict() for influencer in flagged_influencers]}), 200
    
    # Admin Flagged Sponsors [Page]
    @app.route("/admin/flagged_sponsors")
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def flagged_sponsors():

        flagged_sponsors = Sponsor.query.filter_by(flag_status = "Flagged").all()
        
        return jsonify({"flagged_sponsors": [sponsor.to_dict() for sponsor in flagged_sponsors]}), 200
    
    # Admin Platform Statistics [Page]
    @app.route("/admin/platform_statistics")
    @roles_required('Admin')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def admin_dashboard_statistics():

        total_sponsors = Sponsor.query.join(User).filter(User.active == True).count()
        total_influencers = Influencer.query.count()
        active_campaigns = Campaign.query.filter_by(status = "Active").count()
        active_public_campaigns = Campaign.query.filter_by(status = "Active", visibility = "Public").count()
        active_private_campaigns = Campaign.query.filter_by(status = "Active", visibility = "Private").count()
        total_adrequests = AdRequest.query.count()
        total_pending_adrequests = AdRequest.query.filter_by(status = "Pending").count()
        total_accepted_adrequests = AdRequest.query.filter_by(status = "Accepted").count()
        total_rejected_adrequests = AdRequest.query.filter_by(status = "Rejected").count()
        total_flagged_sponsors = Sponsor.query.filter_by(flag_status = "Flagged").count()
        total_flagged_influencers = Influencer.query.filter_by(flag_status = "Flagged").count()
        total_flagged_campaigns = Campaign.query.filter_by(flag_status = "Flagged").count()
        adrequest_sent_by_sponsor = AdRequest.query.filter_by(owner = "Sponsor").count()
        adrequest_sent_by_influencer = AdRequest.query.filter_by(owner = "Influencer").count()
        completed_campaigns = Campaign.query.filter_by(status = "Over").count()

        platform_statistics = {
            "total_sponsors": total_sponsors,
            "total_influencers": total_influencers,
            "active_campaigns": active_campaigns,
            "active_public_campaigns": active_public_campaigns,
            "active_private_campaigns": active_private_campaigns,
            "total_adrequests": total_adrequests,
            "total_pending_adrequests": total_pending_adrequests,
            "total_accepted_adrequests": total_accepted_adrequests,
            "total_rejected_adrequests": total_rejected_adrequests,
            "total_flagged_sponsors": total_flagged_sponsors,
            "total_flagged_influencers": total_flagged_influencers,
            "total_flagged_campaigns": total_flagged_campaigns,
            "adrequest_sent_by_sponsor": adrequest_sent_by_sponsor,
            "adrequest_sent_by_influencer": adrequest_sent_by_influencer,
            "completed_campaigns": completed_campaigns
        }

        return jsonify({"platform_statistics": platform_statistics}), 200
    
# Influencer Routes------------------------------------------------------------------------------------------------------------------------------
    
    # Influencer Dashboard
    @app.route('/influencer/dashboard', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def influencer_dashboard():

        influencer = Influencer.query.filter_by(user_id = current_user.id).first()

        return jsonify({"message": f"Welcome {influencer.name}"}), 200
    
    # Influencer Profile [Page]
    @app.route('/influencer/profile', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def influencer_profile():

        influencer = Influencer.query.filter_by(user_id = current_user.id).first()

        return jsonify({"influencer": influencer.to_dict()}), 200
    
    # Influencer Active Tasks [Page]
    @app.route('/influencer/active_tasks', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def influencer_active_tasks():

        influencer = Influencer.query.filter_by(user_id = current_user.id).first()
        active_tasks = AdRequest.query.filter_by(influencer_id = influencer.id, status = "Accepted").filter(AdRequest.work_status != "Payment Received").all()
        
        return jsonify({"active_tasks": [task.to_dict_with_relations() for task in active_tasks]}), 200

    # Influencer Completed Tasks [Page]
    @app.route('/influencer/completed_tasks', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def influencer_completed_tasks():

        influencer = Influencer.query.filter_by(user_id = current_user.id).first()
        completed_tasks = AdRequest.query.filter_by(influencer_id = influencer.id, status = "Accepted", work_status = "Payment Received").all()
        
        return jsonify({"completed_tasks": [task.to_dict_with_relations() for task in completed_tasks]}), 200

    # Influencer Find a Campaign [Page]
    @app.route('/influencer/public_campaigns', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def influencer_find_campaign():

        public_campaigns = Campaign.query.filter_by(visibility = "Public", status = "Active", flag_status = "Unflagged").all()

        return jsonify({"public_campaigns": [campaign.to_dict_with_relations() for campaign in public_campaigns]}), 200

    # Influencer New Ad Requests Received [Page]
    @app.route('/influencer/new_adrequests', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def influencer_new_adrequests():

        influencer = Influencer.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.filter_by(influencer_id = influencer.id, owner = "Sponsor", status = "Pending").all()

        return jsonify({"new_adrequests": [adrequest.to_dict_with_relations() for adrequest in adrequests]}), 200
    
    # Influencer Ad Requests Sent [Page]
    @app.route('/influencer/sent_adrequests', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def influencer_sent_adrequests():

        influencer = Influencer.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.filter_by(influencer_id = influencer.id, owner = "Influencer").all()

        return jsonify({"sent_adrequests": [adrequest.to_dict_with_relations() for adrequest in adrequests]}), 200
    
    # Influencer Ad Requests Directory [Page]
    @app.route('/influencer/adrequests_directory', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def influencer_adrequests_directory():

        influencer = Influencer.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.filter(AdRequest.influencer_id == influencer.id, AdRequest.status != "Pending").all()

        return jsonify({"adrequests": [adrequest.to_dict_with_relations() for adrequest in adrequests]}), 200

# Sponsor Routes------------------------------------------------------------------------------------------------------------------------------
    
    # Sponsor Dashboard
    @app.route('/sponsor/dashboard', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def sponsor_dashboard():

        if current_user.active == True:
            sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
            return jsonify({"message": f"Welcome {sponsor.name}"}), 200
        else:
            return jsonify({"message": "Your Account is not yet approved by Admin"}), 400
    
    # Sponsor Profile [Page]
    @app.route('/sponsor/profile', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_profile():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()

        return jsonify({"sponsor": sponsor.to_dict()}), 200
    
    # Sponsor My Campaigns [Page]
    @app.route('/sponsor/my_campaigns', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_my_campaigns():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
        campaigns = Campaign.query.filter_by(sponsor_id = sponsor.id).all()

        return jsonify({"my_campaigns": [campaign.to_dict() for campaign in campaigns]}), 200
    
    # Sponsor Monitor Influencer's Tasks [Page]
    @app.route('/sponsor/monitor_influencer_tasks', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_monitor_influencer_tasks():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor.id, AdRequest.status == "Accepted", AdRequest.work_status != "Payment Received").all()

        return jsonify({"monitor_influencer_tasks": [adrequest.to_dict_with_relations() for adrequest in adrequests]}), 200

    # Sponsor Review Completed Tasks [Page]
    @app.route('/sponsor/review_completed_tasks', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def sponsor_review_completed_tasks():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor.id, AdRequest.status == "Accepted", AdRequest.work_status == "Payment Received").all()

        return jsonify({"review_completed_tasks": [adrequest.to_dict_with_relations() for adrequest in adrequests]}), 200
    
    # Sponsor Find an Influencer [Page]
    @app.route('/sponsor/platform_influencers', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_find_influencer():

        platform_influencers = Influencer.query.filter_by(flag_status = "Unflagged").all()

        return jsonify({"platform_influencers": [influencer.to_dict() for influencer in platform_influencers]}), 200
    
    # Sponsor New Ad Requests Received [Page]
    @app.route('/sponsor/new_adrequests', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_new_adrequests():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor.id, AdRequest.owner == "Influencer", AdRequest.status == "Pending").all()

        return jsonify({"new_adrequests": [adrequest.to_dict_with_relations() for adrequest in adrequests]}), 200
    
    # Sponsor Ad Requests Sent [Page]
    @app.route('/sponsor/sent_adrequests', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_sent_adrequests():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor.id, AdRequest.owner == "Sponsor").all()

        return jsonify({"sent_adrequests": [adrequest.to_dict_with_relations() for adrequest in adrequests]}), 200
    
    # Sponsor Ad Requests Directory [Page]
    @app.route('/sponsor/adrequests_directory', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 30)
    def sponsor_adrequests_directory():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor.id, AdRequest.status != "Pending").all()

        return jsonify({"adrequests": [adrequest.to_dict_with_relations() for adrequest in adrequests]}), 200
    
# -----------------------------------------------------------------------------------------------------------------------------------------

    # Influencer Total Earnings
    @app.route('/influencer/total_earnings', methods = ['GET'])
    @roles_required('Influencer')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def influencer_total_earnings():

        influencer = Influencer.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.filter_by(influencer_id = influencer.id, work_status = "Payment Received").all()
        total_earnings = sum([adrequest.payment for adrequest in adrequests])

        return jsonify({"total_earnings": total_earnings}), 200

    # Sponsor Total Payments
    @app.route('/sponsor/total_payments', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_total_payments():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
        adrequests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor.id, AdRequest.work_status == "Payment Received").all()
        total_payments = sum([adrequest.payment for adrequest in adrequests])

        return jsonify({"total_payments": total_payments}), 200
    
    # Sponsor Create Adrequest - Get Influencer List
    @app.route('/sponsor/all_influencers', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_all_influencers():

        all_influencers = Influencer.query.filter_by(flag_status = "Unflagged").all()

        return jsonify({"all_influencers": [influencer.to_dict() for influencer in all_influencers]}), 200
    
    # Sponsor Create Adrequest - Get Campaign List
    @app.route('/sponsor/all_campaigns', methods = ['GET'])
    @roles_required('Sponsor')
    @auth_required('token')
    @cache.cached(timeout = 3)
    def sponsor_campaigns_list():

        sponsor = Sponsor.query.filter_by(user_id = current_user.id).first()
        my_campaigns = Campaign.query.filter_by(sponsor_id = sponsor.id, flag_status = "Unflagged").all()

        return jsonify({"my_campaigns": [campaign.to_dict_with_relations() for campaign in my_campaigns]}), 200
    
    # Search Influencers
    @app.route('/search-influencers', methods=['POST'])
    @roles_required('Sponsor')
    @auth_required('token')
    def search_influencers():
        data = request.get_json()
        name = data.get('name', '')
        category = data.get('category', '')
        reach = data.get('reach', '')

        searchQuery = Influencer.query.filter_by(flag_status = "Unflagged").all()

        filtered_influencers = [
            influencer for influencer in searchQuery
            if (not name or name.lower() in influencer.name.lower()) and
            (not category or category == influencer.category) and
            (not reach or reach == influencer.reach)
        ]

        return jsonify({"searchQuery": [influencer.to_dict() for influencer in filtered_influencers]}), 200
    
    # Search Campaigns
    @app.route('/search-campaigns', methods=['POST'])
    @roles_required('Influencer')
    @auth_required('token')
    def search_campaign():
        data = request.get_json()
        name = data.get('name', '')
        budget = data.get('budget', '')
        target_audience = data.get('target_audience', '')

        searchQuery = Campaign.query.filter_by(visibility = "Public", flag_status = "Unflagged").all()

        filtered_campaigns = [
            campaign for campaign in searchQuery
            if (not name or name.lower() in campaign.name.lower()) and
            (not budget or budget == campaign.budget) and
            (not target_audience or target_audience == campaign.target_audience)
        ]

        return jsonify({"searchQuery": [campaign.to_dict_with_relations() for campaign in filtered_campaigns]}), 200
    
# Backend Job Routes------------------------------------------------------------------------------------------------------------------------------

    # Trigger Job to export Campaign Data of a Sponsor as CSV
    @app.route('/sponsor/export_campaigns', methods = ['GET'])
    def export_campaigns():
        user_id = current_user.id
        task = create_csv.delay(user_id)
        return jsonify({"task_id": task.id}), 200
    
    # Route of the button to trigger the export job
    @app.route('/download_campaigns/<task_id>', methods=['GET'])
    def download_campaigns(task_id):

        response = AsyncResult(task_id)

        if response.ready():
            filename = response.result

            if filename is None or not isinstance(filename, str):
                return jsonify({"message": "Failed to generate CSV file"}), 500

            if os.path.exists(filename):
                return send_file(filename, as_attachment=True, download_name="campaigns.csv")
            else:
                return jsonify({"message": "File not found"}), 404
        else:
            return jsonify({"message": "Job is still running"}), 404