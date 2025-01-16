from .extensions import db
from flask_security import UserMixin, RoleMixin

class UsersRoles(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role_id": self.role_id
        }

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    active = db.Column(db.Boolean(), default = True)
    fs_uniquifier = db.Column(db.String(), nullable = False)

    roles = db.relationship('Role', secondary = 'users_roles')
    influencer = db.relationship('Influencer', back_populates = 'user', uselist = False)
    sponsor = db.relationship('Sponsor', back_populates = 'user', uselist = False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "active": self.active,
            "roles": [role.name for role in self.roles]
        }
    
    def to_dict_with_relations(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "active": self.active,
            "roles": [role.to_dict() for role in self.roles],
            "influencer": self.influencer.to_dict() if self.influencer else None,
            "sponsor": self.sponsor.to_dict() if self.sponsor else None
        }

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), unique = True, nullable = False) # Admin / Sponsor / Influencer
    description = db.Column(db.String(), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class Influencer(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False)
    category = db.Column(db.String(), nullable = False)
    reach = db.Column(db.String(), nullable = False)
    description = db.Column(db.Text(), nullable = False)
    flag_status = db.Column(db.String(), default = "Unflagged") # Unflagged / Flagged

    user = db.relationship('User', back_populates = 'influencer')
    adrequests = db.relationship('AdRequest', backref = 'influencer', lazy = True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "category": self.category,
            "reach": self.reach,
            "description": self.description,
            "flag_status": self.flag_status
        }
    
    def to_dict_with_relations(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "category": self.category,
            "reach": self.reach,
            "description": self.description,
            "flag_status": self.flag_status,
            "user": self.user.to_dict(),
            "adrequests": [adrequest.to_dict() for adrequest in self.adrequests],
            "campaigns": [adrequest.campaign.to_dict() if adrequest.campaign else None for adrequest in self.adrequests]
        }

class Sponsor(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False)
    industry = db.Column(db.String(), nullable = False)
    valuation = db.Column(db.String(), nullable = False)
    description = db.Column(db.Text(), nullable = False)
    flag_status = db.Column(db.String(), default = "Unflagged") # Unflagged / Flagged

    user = db.relationship('User', back_populates = 'sponsor')
    campaigns = db.relationship('Campaign', backref = 'sponsor', lazy = True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "industry": self.industry,
            "valuation": self.valuation,
            "description": self.description,
            "flag_status": self.flag_status
        }
    
    def to_dict_with_relations(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "industry": self.industry,
            "valuation": self.valuation,
            "description": self.description,
            "flag_status": self.flag_status,
            "user": self.user.to_dict(),
            "campaigns": [campaign.to_dict() for campaign in self.campaigns],
            "adrequests": [adrequest.to_dict() for campaign in self.campaigns for adrequest in campaign.adrequests.all()]
        }

class Campaign(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    sponsor_id = db.Column(db.Integer(), db.ForeignKey('sponsor.id'))
    name = db.Column(db.String(), nullable = False)
    start_date = db.Column(db.String(), nullable = False)
    end_date = db.Column(db.String(), nullable = False)
    budget = db.Column(db.Float(), nullable = False)
    visibility = db.Column(db.String(), nullable = False) # Public / Private
    target_audience = db.Column(db.String(), nullable = False)
    status = db.Column(db.String(), default = "Active") # Active / Over
    description = db.Column(db.Text(), nullable = False)
    flag_status = db.Column(db.String(), default = "Unflagged") # Unflagged / Flagged

    adrequests = db.relationship('AdRequest', backref = 'campaign', lazy = 'dynamic')

    def to_dict(self):
        return {
            "id": self.id,
            "sponsor_id": self.sponsor_id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "visibility": self.visibility,
            "target_audience": self.target_audience,
            "status": self.status,
            "description": self.description,
            "flag_status": self.flag_status
        }
    
    def to_dict_with_relations(self):
        return {
            "id": self.id,
            "sponsor_id": self.sponsor_id,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "visibility": self.visibility,
            "target_audience": self.target_audience,
            "status": self.status,
            "description": self.description,
            "flag_status": self.flag_status,
            "sponsor": self.sponsor.to_dict(),
            "adrequests": [adrequest.to_dict() for adrequest in self.adrequests.all()]
        }

class AdRequest(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    campaign_id = db.Column(db.Integer(), db.ForeignKey('campaign.id'))
    influencer_id = db.Column(db.Integer(), db.ForeignKey('influencer.id'))
    title = db.Column(db.String(), nullable = False)
    message = db.Column(db.Text(), nullable = False)
    requirements = db.Column(db.Text(), nullable = False)
    payment = db.Column(db.Float(), nullable = False)
    status = db.Column(db.String(), default = "Pending") # Pending / Accepted / Rejected
    owner = db.Column(db.String(), nullable = False) # Influencer / Sponsor
    work_status = db.Column(db.String(), default = "NA") # NA / 0% / 25% / 50% / 75% / 100% / Confirmation Pending / Payment Pending / Payment Received

    def to_dict(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "influencer_id": self.influencer_id,
            "title": self.title,
            "message": self.message,
            "requirements": self.requirements,
            "payment": self.payment,
            "status": self.status,
            "owner": self.owner,
            "work_status": self.work_status
        }
    
    def to_dict_with_relations(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "influencer_id": self.influencer_id,
            "title": self.title,
            "message": self.message,
            "requirements": self.requirements,
            "payment": self.payment,
            "status": self.status,
            "owner": self.owner,
            "work_status": self.work_status,
            "campaign": self.campaign.to_dict(),
            "influencer": self.influencer.to_dict()
        }