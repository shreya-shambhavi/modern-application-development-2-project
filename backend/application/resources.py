from flask_restful import Api, Resource, reqparse, fields, marshal_with, marshal
from flask_security import login_required, current_user, auth_required, roles_required, roles_accepted
from .extensions import db, cache
from .models import User, Role, Influencer, Sponsor, Campaign, AdRequest, UsersRoles
from .datastore import user_datastore
from flask import jsonify, request

api = Api(prefix='/api')

# User Resource
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type = str, required = False, help = 'Username required')
user_parser.add_argument('password', type = str, required = False, help = 'Password required')
user_parser.add_argument('roles', type = str, required = False, help = 'Role required')
user_parser.add_argument('active', type = bool, required = False, help = 'Active required')

# To extract role names from the roles list
class ListField(fields.Raw):
    def format(self, value):
        return ', '.join([v.name for v in value])

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'roles': ListField(attribute='roles'),
    'active': fields.Boolean,
    'influencer': fields.Nested({
        'id': fields.Integer,
        'user_id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'category': fields.String,
        'reach': fields.String,
        'description': fields.String,
        'flag_status': fields.String,
    }),
    'sponsor': fields.Nested({
        'id': fields.Integer,
        'user_id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'industry': fields.String,
        'valuation': fields.String,
        'description': fields.String,
        'flag_status': fields.String,
    })
}

class UserResource(Resource):
    
    @auth_required('token')
    @roles_accepted('Admin', 'Influencer', 'Sponsor')
    @cache.cached(timeout = 3)
    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {'message' : 'User not found'}, 404
        return user
    
    @roles_accepted('Admin', 'Influencer', 'Sponsor')
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User(username = args['username'], password = args['password'], active = args['active'])
        db.session.add(user)
        db.session.commit()
        role = Role.query.filter_by(name = args['roles']).first()
        if role:
            user_datastore.add_role_to_user(user, role)
            db.session.commit()
        return user, 201
    
    @auth_required('token')
    @roles_accepted('Admin', 'Influencer', 'Sponsor')
    @marshal_with(user_fields)
    def put(self, id):
        args = user_parser.parse_args()
        user = User.query.get(id)

        if not user:
            return {'message' : 'User not found'}, 404
        
        if args['username']:
            user.username = args['username']
        if args['password']:
            user.password = args['password']
        if args['active']:
            user.active = args['active']
        if args['roles']:
            role = Role.query.filter_by(name = args['roles']).first()
            if role and role not in user.roles:
                user_datastore.add_role_to_user(user, role)
        
        db.session.commit()
        return user
    
    @auth_required('token')
    @roles_accepted('Admin', 'Influencer', 'Sponsor')
    @marshal_with(user_fields)
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return {'message' : 'User not found'}, 404
        
        if user.influencer:
            AdRequest.query.filter_by(influencer_id = user.influencer.id).delete()
            db.session.delete(user.influencer)
        elif user.sponsor:
            campaigns = Campaign.query.filter_by(sponsor_id = user.sponsor.id).all()
            for campaign in campaigns:
                AdRequest.query.filter_by(campaign_id = campaign.id).delete()
                db.session.delete(campaign)
            db.session.delete(user.sponsor)

        UsersRoles.query.filter_by(user_id = user.id).delete()

        db.session.delete(user)
        db.session.commit()
        return '', 204
        
# Influencer Resource
influencer_parser = reqparse.RequestParser()
influencer_parser.add_argument('user_id', type = int, required = False, help = 'User ID required')
influencer_parser.add_argument('name', type = str, required = False, help = 'Name required')
influencer_parser.add_argument('email', type = str, required = False, help = 'Email required')
influencer_parser.add_argument('category', type = str, required = False, help = 'Category required')
influencer_parser.add_argument('reach', type = str, required = False, help = 'Reach required')
influencer_parser.add_argument('description', type = str, required = False, help = 'Description required')
influencer_parser.add_argument('flag_status', type = str, default = "Unflagged", help = 'Flag Status required')

influencer_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'category': fields.String,
    'reach': fields.String,
    'description': fields.String,
    'flag_status': fields.String,
    'adrequests': fields.Nested({
        'id': fields.Integer,
        'campaign_id': fields.Integer,
        'influencer_id': fields.Integer,
        'title': fields.String,
        'message': fields.String,
        'requirements': fields.String,
        'payment': fields.Float,
        'status': fields.String,
        'owner': fields.String,
        'work_status': fields.String,
    }),
    'campaigns': fields.List(fields.Nested({
        'id': fields.Integer,
        'sponsor_id': fields.Integer,
        'name': fields.String,
        'start_date': fields.String,
        'end_date': fields.String,
        'budget': fields.Float,
        'visibility': fields.String,
        'target_audience': fields.String,
        'description': fields.String,
        'status': fields.String,
        'flag_status': fields.String,
    }))
}

class InfluencerResource(Resource):

    @auth_required('token')
    @roles_accepted('Admin', 'Influencer', 'Sponsor')
    @cache.cached(timeout = 3)    
    @marshal_with(influencer_fields)
    def get(self, id):
        influencer = Influencer.query.get(id)
        if not influencer:
            return {'message' : 'Influencer not found'}, 404
        return influencer
    
    @roles_required('Influencer')
    @marshal_with(influencer_fields)
    def post(self):
        args = influencer_parser.parse_args()
        influencer = Influencer(user_id = args['user_id'], name = args['name'], email = args['email'], category = args['category'], reach = args['reach'], description = args['description'], flag_status = args['flag_status'])
        db.session.add(influencer)
        db.session.commit()
        return influencer, 201
    
    @auth_required('token')
    @roles_accepted('Admin', 'Influencer')
    @marshal_with(influencer_fields)
    def put(self, id):
        args = influencer_parser.parse_args()
        influencer = Influencer.query.get(id)
        if not influencer:
            return {'message' : 'Influencer not found'}, 404
        
        if args['user_id']:
            influencer.user_id = args['user_id']
        if args['name']:
            influencer.name = args['name']
        if args['email']:
            influencer.email = args['email']
        if args['category']:
            influencer.category = args['category']
        if args['reach']:
            influencer.reach = args['reach']
        if args['description']:
            influencer.description = args['description']
        if args['flag_status']:
            influencer.flag_status = args['flag_status']
        
        db.session.commit()
        return influencer

    @auth_required('token')
    @roles_accepted('Admin', 'Influencer')
    @marshal_with(influencer_fields)
    def delete(self, id):
        influencer = Influencer.query.get(id)
        if not influencer:
            return {'message' : 'Influencer not found'}, 404
        
        AdRequest.query.filter_by(influencer_id = id).delete()
        db.session.delete(influencer)

        user = User.query.get(influencer.user_id)
        if user:
            UsersRoles.query.filter_by(user_id = user.id).delete()
            db.session.delete(user)

        db.session.commit()
        return '', 204

# Sponsor Resource
sponsor_parser = reqparse.RequestParser()
sponsor_parser.add_argument('user_id', type = int, required = False, help = 'User ID required')
sponsor_parser.add_argument('name', type = str, required = False, help = 'Name required')
sponsor_parser.add_argument('email', type = str, required = False, help = 'Email required')
sponsor_parser.add_argument('industry', type = str, required = False, help = 'Industry required')
sponsor_parser.add_argument('valuation', type = str, required = False, help = 'Valuation required')
sponsor_parser.add_argument('description', type = str, required = False, help = 'Description required')
sponsor_parser.add_argument('flag_status', type = str, default = "Unflagged", help = 'Flag Status required')

sponsor_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'industry': fields.String,
    'valuation': fields.String,
    'description': fields.String,
    'flag_status': fields.String,
    'campaigns': fields.Nested({
        'id': fields.Integer,
        'sponsor_id': fields.Integer,
        'name': fields.String,
        'start_date': fields.String,
        'end_date': fields.String,
        'budget': fields.Float,
        'visibility': fields.String,
        'target_audience': fields.String,
        'description': fields.String,
        'status': fields.String,
        'flag_status': fields.String,
    }),
    'adrequests': fields.List(fields.Nested({
        'id': fields.Integer,
        'campaign_id': fields.Integer,
        'influencer_id': fields.Integer,
        'title': fields.String,
        'message': fields.String,
        'requirements': fields.String,
        'payment': fields.Float,
        'status': fields.String,
        'owner': fields.String,
        'work_status': fields.String,
    }))
}

class SponsorResource(Resource):

    @auth_required('token')
    @roles_accepted('Admin', 'Influencer', 'Sponsor')
    @cache.cached(timeout = 3)        
    @marshal_with(sponsor_fields)
    def get(self, id):
        sponsor = Sponsor.query.get(id)
        if not sponsor:
            return {'message' : 'Sponsor not found'}, 404
        return sponsor
    
    @roles_required('Sponsor')
    @marshal_with(sponsor_fields)
    def post(self):
        args = sponsor_parser.parse_args()
        sponsor = Sponsor(user_id = args['user_id'], name = args['name'], email = args['email'], industry = args['industry'], valuation = args['valuation'], description = args['description'], flag_status = args['flag_status'])
        db.session.add(sponsor)
        db.session.commit()
        return sponsor, 201
    
    @auth_required('token')
    @roles_accepted('Admin', 'Sponsor')
    @marshal_with(sponsor_fields)
    def put(self, id):
        args = sponsor_parser.parse_args()
        sponsor = Sponsor.query.get(id)
        if not sponsor:
            return {'message' : 'Sponsor not found'}, 404
        
        if args['user_id']:
            sponsor.user_id = args['user_id']
        if args['name']:
            sponsor.name = args['name']
        if args['email']:
            sponsor.email = args['email']
        if args['industry']:
            sponsor.industry = args['industry']
        if args['valuation']:
            sponsor.valuation = args['valuation']
        if args['description']:
            sponsor.description = args['description']
        if args['flag_status']:
            sponsor.flag_status = args['flag_status']
        
        db.session.commit()
        return sponsor
    
    @auth_required('token')
    @roles_accepted('Admin', 'Sponsor')
    @marshal_with(sponsor_fields)
    def delete(self, id):
        sponsor = Sponsor.query.get(id)
        if not sponsor:
            return {'message' : 'Sponsor not found'}, 404
        
        campaigns = Campaign.query.filter_by(sponsor_id = id).all()
        for campaign in campaigns:
            AdRequest.query.filter_by(campaign_id = campaign.id).delete()
            db.session.delete(campaign)

        db.session.delete(sponsor)

        user = User.query.get(sponsor.user_id)
        if user:
            UsersRoles.query.filter_by(user_id = user.id).delete()
            db.session.delete(user)

        db.session.commit()
        return '', 204

# Campaign Resource
campaign_parser = reqparse.RequestParser()
campaign_parser.add_argument('sponsor_id', type = int, required = False, help = 'Sponsor ID required')
campaign_parser.add_argument('name', type = str, required = False, help = 'Name required')
campaign_parser.add_argument('start_date', type = str, required = False, help = 'Start Date required')
campaign_parser.add_argument('end_date', type = str, required = False, help = 'End Date required')
campaign_parser.add_argument('budget', type = float, required = False, help = 'Budget required')
campaign_parser.add_argument('visibility', type = str, required = False, help = 'Visibility required')
campaign_parser.add_argument('target_audience', type = str, required = False, help = 'Target Audience required')
campaign_parser.add_argument('description', type = str, required = False, help = 'Description required')
campaign_parser.add_argument('status', type = str, default = "Active", help = 'Status required')
campaign_parser.add_argument('flag_status', type = str, default = "Unflagged", help = 'Flag Status required')

campaign_fields = {
    'id': fields.Integer,
    'sponsor_id': fields.Integer,
    'name': fields.String,
    'start_date': fields.String,
    'end_date': fields.String,
    'budget': fields.Float,
    'visibility': fields.String,
    'target_audience': fields.String,
    'description': fields.String,
    'status': fields.String,
    'flag_status': fields.String,
    'sponsor': fields.Nested({
        'id': fields.Integer,
        'user_id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'industry': fields.String,
        'valuation': fields.String,
        'description': fields.String,
        'flag_status': fields.String,
    }),
    'adrequests': fields.List(fields.Nested({
        'id': fields.Integer,
        'campaign_id': fields.Integer,
        'influencer_id': fields.Integer,
        'title': fields.String,
        'message': fields.String,
        'requirements': fields.String,
        'payment': fields.Float,
        'status': fields.String,
        'owner': fields.String,
        'work_status': fields.String,
    }))
}

class CampaignResource(Resource):

    @auth_required('token')
    @roles_accepted('Admin', 'Influencer', 'Sponsor')
    @cache.cached(timeout = 3)      
    @marshal_with(campaign_fields)
    def get(self, id):
        campaign = Campaign.query.get(id)
        if not campaign:
            return {'message' : 'Campaign not found'}, 404
        return campaign
    
    @auth_required('token')
    @roles_required('Sponsor')
    @marshal_with(campaign_fields)
    def post(self):
        args = campaign_parser.parse_args()
        campaign = Campaign(sponsor_id = args['sponsor_id'], name = args['name'], start_date = args['start_date'], end_date = args['end_date'], budget = args['budget'], visibility = args['visibility'], target_audience = args['target_audience'], description = args['description'], status = args['status'], flag_status = args['flag_status'])
        db.session.add(campaign)
        db.session.commit()
        return campaign, 201
    
    @auth_required('token')
    @roles_accepted('Admin', 'Sponsor')
    @marshal_with(campaign_fields)
    def put(self, id):
        args = campaign_parser.parse_args()
        campaign = Campaign.query.get(id)

        if not campaign:
            return {'message' : 'Campaign not found'}, 404
        
        if args['sponsor_id']:
            campaign.sponsor_id = args['sponsor_id']
        if args['name']:
            campaign.name = args['name']
        if args['start_date']:
            campaign.start_date = args['start_date']
        if args['end_date']:
            campaign.end_date = args['end_date']
        if args['budget']:
            campaign.budget = args['budget']
        if args['visibility']:
            campaign.visibility = args['visibility']
        if args['target_audience']:
            campaign.target_audience = args['target_audience']
        if args['description']:
            campaign.description = args['description']
        if args['status']:
            campaign.status = args['status']
        if args['flag_status']:
            campaign.flag_status = args['flag_status']

        db.session.commit()
        return campaign
    
    @auth_required('token')
    @roles_accepted('Admin', 'Sponsor')
    @marshal_with(campaign_fields)
    def delete(self, id):
        campaign = Campaign.query.get(id)
        if not campaign:
            return {'message' : 'Campaign not found'}, 404
        
        AdRequest.query.filter_by(campaign_id = id).delete()

        db.session.delete(campaign)
        db.session.commit()
        return '', 204

# AdRequest Resource
adrequest_parser = reqparse.RequestParser()
adrequest_parser.add_argument('campaign_id', type = int, required = False, help = 'Campaign ID required')
adrequest_parser.add_argument('influencer_id', type = int, required = False, help = 'Influencer ID required')
adrequest_parser.add_argument('title', type = str, required = False, help = 'Title required')
adrequest_parser.add_argument('message', type = str, required = False, help = 'Message required')
adrequest_parser.add_argument('requirements', type = str, required = False, help = 'Requirements required')
adrequest_parser.add_argument('payment', type = float, required = False, help = 'Payment required')
adrequest_parser.add_argument('status', type = str, default = "Pending", help = 'Status required')
adrequest_parser.add_argument('owner', type = str, required = False, help = 'Owner required')
adrequest_parser.add_argument('work_status', type = str, default = "NA", help = 'Work Status required')

adrequest_fields = {
    'id': fields.Integer,
    'campaign_id': fields.Integer,
    'influencer_id': fields.Integer,
    'title': fields.String,
    'message': fields.String,
    'requirements': fields.String,
    'payment': fields.Float,
    'status': fields.String,
    'owner': fields.String,
    'work_status': fields.String,
    'campaign': fields.Nested({
        'id': fields.Integer,
        'sponsor_id': fields.Integer,
        'name': fields.String,
        'start_date': fields.String,
        'end_date': fields.String,
        'budget': fields.Float,
        'visibility': fields.String,
        'target_audience': fields.String,
        'description': fields.String,
        'status': fields.String,
        'flag_status': fields.String,
    }),
    'influencer': fields.Nested({
        'id': fields.Integer,
        'user_id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'category': fields.String,
        'reach': fields.String,
        'description': fields.String,
        'flag_status': fields.String,
    }),
}

class AdRequestResource(Resource):
    
    @auth_required('token')
    @roles_accepted('Admin', 'Influencer', 'Sponsor')
    @cache.cached(timeout = 3)
    @marshal_with(adrequest_fields)
    def get(self, id):
        adrequest = AdRequest.query.get(id)
        if not adrequest:
            return {'message' : 'Ad Request not found'}, 404
        return adrequest
    
    @auth_required('token')
    @roles_accepted('Sponsor', 'Influencer')
    @marshal_with(adrequest_fields)
    def post(self):
        args = adrequest_parser.parse_args()
        adrequest = AdRequest(campaign_id = args['campaign_id'], influencer_id = args['influencer_id'], title = args['title'], message = args['message'], requirements = args['requirements'], payment = args['payment'], status = args['status'], owner = args['owner'], work_status = args['work_status'])
        db.session.add(adrequest)
        db.session.commit()
        return adrequest, 201
    
    @auth_required('token')
    @roles_accepted('Sponsor', 'Influencer')
    @marshal_with(adrequest_fields)
    def put(self, id):
        args = adrequest_parser.parse_args()
        adrequest = AdRequest.query.get(id)
        if not adrequest:
            return {'message' : 'Ad Request not found'}, 404
        
        if 'campaign_id' in args:
            adrequest.campaign_id = args['campaign_id']
        if 'influencer_id' in args:
            adrequest.influencer_id = args['influencer_id']
        if 'title' in args:
            adrequest.title = args['title']
        if 'message' in args:
            adrequest.message = args['message']
        if 'requirements' in args:
            adrequest.requirements = args['requirements']
        if 'payment' in args:
            adrequest.payment = args['payment']
        if 'status' in args:
            adrequest.status = args['status']
        if 'owner' in args:
            adrequest.owner = args['owner']
        if 'work_status' in args:
            adrequest.work_status = args['work_status']

        db.session.commit()
        return adrequest
    
    @auth_required('token')
    @roles_accepted('Admin', 'Sponsor', 'Influencer')
    @marshal_with(adrequest_fields)
    def delete(self, id):
        adrequest = AdRequest.query.get(id)
        if not adrequest:
            return {'message' : 'Ad Request not found'}, 404
        db.session.delete(adrequest)
        db.session.commit()
        return '', 204

api.add_resource(UserResource, '/user', '/user/<int:id>')
api.add_resource(InfluencerResource, '/influencer', '/influencer/<int:id>')
api.add_resource(SponsorResource, '/sponsor', '/sponsor/<int:id>')
api.add_resource(CampaignResource, '/campaign', '/campaign/<int:id>')
api.add_resource(AdRequestResource, '/adrequest', '/adrequest/<int:id>')