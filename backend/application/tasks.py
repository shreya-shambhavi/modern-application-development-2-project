from celery import shared_task
import flask_excel as excel
from .mail_service import send_email
from .models import Sponsor, Campaign, Influencer, AdRequest, User
from jinja2 import Template, Environment, FileSystemLoader
from flask import jsonify

# Job to create CSV for Campaign Data of a Sponsor
@shared_task(ignore_result = False)
def create_csv(user_id):
    
    sponsor = Sponsor.query.filter_by(user_id = user_id).first()

    if not sponsor:
        return None

    campaigns = Campaign.query.filter_by(sponsor_id = sponsor.id).all()

    csv_output = excel.make_response_from_query_sets(campaigns, ["id", "name", "start_date", "end_date", "budget", "visibility", "target_audience", "status", "description", "flag_status"], "csv")

    filename = f"campaigns_{user_id}.csv"

    try:
        with open(filename, "w", newline = "") as f:
            f.write(csv_output.get_data(as_text = True))
    except Exception as e:
        return None

    return filename

# Job to send daily reminders to Influencers with pending Ad Requests
@shared_task(ignore_result = True)
def daily_reminder():

    inactive_influencers = Influencer.query.join(AdRequest).filter(AdRequest.influencer_id == Influencer.id, AdRequest.status == "Pending").all()

    for influencer in inactive_influencers:
        send_email(influencer.email, "Reminder: Ad Requests Pending", "Dear Influencer, You have some Ad Requests pending. Additionally, there are some more public campaigns available for you to apply since your last visit. Please check your dashboard for more details.")

    return "Daily reminders sent"

# Job to send monthly reports to Sponsors
@shared_task(ignore_result = True)
def monthly_report():

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')

    sponsors = Sponsor.query.join(User).filter(User.id == Sponsor.user_id, User.active == True).all()

    for sponsor in sponsors:

        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        campaigns_count = len(campaigns)
        adrequests_count = sum([AdRequest.query.filter_by(campaign_id=campaign.id).count() for campaign in campaigns])
        total_budget = sum([campaign.budget for campaign in campaigns])
        accepted_adrequests_count = sum([AdRequest.query.filter_by(campaign_id=campaign.id, status="Accepted").count() for campaign in campaigns])
        rejected_adrequests_count = sum([AdRequest.query.filter_by(campaign_id=campaign.id, status="Rejected").count() for campaign in campaigns])
        completed_adrequests_count = sum([AdRequest.query.filter_by(campaign_id=campaign.id, work_status="Payment Received").count() for campaign in campaigns])
        pending_adrequests_count = sum([AdRequest.query.filter_by(campaign_id=campaign.id, status="Pending").count() for campaign in campaigns])

        html = template.render(
            sponsor = sponsor,
            campaigns_count = campaigns_count,
            adrequests_count = adrequests_count,
            total_budget = total_budget,
            accepted_adrequests_count = accepted_adrequests_count,
            rejected_adrequests_count = rejected_adrequests_count,
            completed_adrequests_count = completed_adrequests_count,
            pending_adrequests_count = pending_adrequests_count
        )
        
        send_email(sponsor.email, "Monthly Report", html)

    return "Monthly reports sent"