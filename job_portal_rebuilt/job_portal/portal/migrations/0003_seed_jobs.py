from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.db import migrations
from django.utils import timezone


def seed_jobs(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('portal', 'Profile')
    Job = apps.get_model('portal', 'Job')

    companies = [
        ('brightbyte', 'BrightByte Technologies', 'Pune', 'Technology solutions company building SaaS products and digital platforms.'),
        ('cloudnest', 'CloudNest Systems', 'Mumbai', 'Cloud infrastructure and software engineering team working on scalable platforms.'),
        ('finpulse', 'FinPulse Digital', 'Bengaluru', 'Digital finance company building customer-first payment and analytics products.'),
        ('designorbit', 'DesignOrbit Studio', 'Remote', 'Product design studio creating modern interfaces for web and mobile products.'),
        ('eduvista', 'EduVista Learning', 'Hyderabad', 'Education technology company building accessible online learning experiences.'),
        ('retailgrid', 'RetailGrid India', 'Nashik', 'Retail technology company developing commerce, inventory, and analytics solutions.'),
        ('healthsync', 'HealthSync Technologies', 'Pune', 'Technology company creating secure tools for healthcare operations.'),
        ('marketloop', 'MarketLoop', 'Ahmedabad', 'Growth and commerce platform helping brands reach customers online.'),
    ]

    company_users = {}
    for username, company_name, location, bio in companies:
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': company_name.split()[0],
                'last_name': 'Careers',
                'email': f'careers@{username}.example.com',
                'password': make_password('Demo@12345'),
            },
        )
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'role': 'company',
                'company_name': company_name,
                'location': location,
                'bio': bio,
                'company_website': f'https://www.{username}.example.com',
            },
        )
        company_users[company_name] = user

    sample_jobs = [
        ('BrightByte Technologies', 'Junior Python Developer', 'technology', 'Pune, Maharashtra', 'full_time', 'hybrid', 'fresher', 'Python, Django, SQL, REST API, Git', 28000, 48000, 3, 'Build backend modules, REST APIs and database-driven features for a growing SaaS product.', 'Diploma or degree in Computer Engineering. Good Python and SQL fundamentals. Freshers with project experience are welcome.', 42, True),
        ('BrightByte Technologies', 'Frontend Developer Intern', 'technology', 'Pune, Maharashtra', 'internship', 'hybrid', 'fresher', 'HTML, CSS, JavaScript, Git, Responsive Design', 10000, 18000, 4, 'Work with the product team to turn wireframes into responsive, accessible web pages.', 'Basic HTML, CSS and JavaScript knowledge with a portfolio or academic project.', 35, True),
        ('BrightByte Technologies', 'QA Automation Engineer', 'technology', 'Pune, Maharashtra', 'full_time', 'on_site', '1_3', 'Python, Selenium, PyTest, API Testing, Git', 45000, 70000, 2, 'Create automated test suites and improve release quality across web applications.', '1–3 years of testing experience with Python or another scripting language and API testing knowledge.', 40, False),
        ('CloudNest Systems', 'Cloud Support Engineer', 'it_support', 'Mumbai, Maharashtra', 'full_time', 'on_site', '0_1', 'Linux, AWS, Networking, Python, Bash', 35000, 60000, 4, 'Monitor cloud workloads, troubleshoot incidents and assist engineers with deployments.', 'Understanding of Linux, networking basics and cloud concepts. AWS certification is a plus.', 45, True),
        ('CloudNest Systems', 'DevOps Engineer', 'technology', 'Mumbai, Maharashtra', 'full_time', 'hybrid', '1_3', 'AWS, Docker, CI/CD, Linux, GitHub Actions', 65000, 95000, 2, 'Build reliable CI/CD pipelines and infrastructure automation for production services.', '1–3 years in DevOps or cloud engineering with hands-on AWS and Docker experience.', 28, False),
        ('CloudNest Systems', 'Technical Support Intern', 'it_support', 'Remote, India', 'internship', 'remote', 'fresher', 'Linux, Networking, SQL, Communication', 9000, 16000, 5, 'Help customers diagnose product issues and document repeatable solutions.', 'Basic networking and operating-system concepts with good written communication.', 50, False),
        ('FinPulse Digital', 'Java Developer', 'technology', 'Bengaluru, Karnataka', 'full_time', 'hybrid', '1_3', 'Java, Spring Boot, SQL, REST API, Git', 55000, 90000, 3, 'Develop secure APIs and backend services for financial products.', '1–3 years of Java development experience, strong OOP and SQL knowledge.', 31, True),
        ('FinPulse Digital', 'Data Analyst', 'data', 'Bengaluru, Karnataka', 'full_time', 'hybrid', '0_1', 'Excel, SQL, Python, Power BI, Data Visualization', 40000, 65000, 2, 'Analyze business data and build dashboards that support product and operations teams.', 'Strong SQL and Excel skills. Python or Power BI experience preferred.', 34, True),
        ('FinPulse Digital', 'Product Management Intern', 'management', 'Bengaluru, Karnataka', 'internship', 'hybrid', 'fresher', 'Product Research, Excel, Communication, Documentation', 12000, 20000, 2, 'Support product discovery, competitor research and release documentation.', 'Curiosity, communication skills and comfort working with spreadsheets and documents.', 46, False),
        ('DesignOrbit Studio', 'UI/UX Designer', 'design', 'Remote, India', 'full_time', 'remote', '1_3', 'Figma, UX Research, Wireframing, Prototyping', 45000, 75000, 2, 'Design intuitive web and mobile experiences from research through high-fidelity prototypes.', 'A strong Figma portfolio and understanding of user-centered design processes.', 37, True),
        ('DesignOrbit Studio', 'Graphic Design Intern', 'design', 'Remote, India', 'internship', 'remote', 'fresher', 'Figma, Photoshop, Illustrator, Canva', 8000, 15000, 3, 'Create social media, presentation and marketing visuals for product teams.', 'Basic visual design principles and a portfolio of creative work.', 39, False),
        ('EduVista Learning', 'Full Stack Developer', 'technology', 'Hyderabad, Telangana', 'full_time', 'hybrid', '1_3', 'Python, Django, JavaScript, React, PostgreSQL', 60000, 100000, 2, 'Build end-to-end learning platform features across frontend and backend systems.', '1–3 years full-stack experience, strong JavaScript and Python fundamentals.', 29, True),
        ('EduVista Learning', 'Content Writer', 'content', 'Hyderabad, Telangana', 'full_time', 'on_site', '0_1', 'Content Writing, SEO, Research, WordPress', 25000, 42000, 2, 'Create clear educational and SEO-focused articles for students and professionals.', 'Strong English writing skills, research ability and basic SEO knowledge.', 41, False),
        ('EduVista Learning', 'Python Developer Intern', 'technology', 'Remote, India', 'internship', 'remote', 'fresher', 'Python, Django, SQLite, Git, HTML, CSS', 10000, 18000, 6, 'Assist with Django applications, bug fixes, database queries and API development.', 'Python basics plus a college project using Django or Flask is preferred.', 55, True),
        ('RetailGrid India', 'React Developer', 'technology', 'Nashik, Maharashtra', 'full_time', 'hybrid', '1_3', 'React, JavaScript, TypeScript, REST API, Git', 50000, 80000, 2, 'Develop responsive commerce interfaces and reusable frontend components.', 'Strong React and JavaScript knowledge with API integration experience.', 33, True),
        ('RetailGrid India', 'Business Development Executive', 'sales', 'Nashik, Maharashtra', 'full_time', 'on_site', '0_1', 'Sales, CRM, Communication, Lead Generation', 22000, 38000, 5, 'Generate and qualify leads while building relationships with retail businesses.', 'Confident communication and willingness to work with measurable sales targets.', 26, False),
        ('RetailGrid India', 'Operations Executive', 'operations', 'Nashik, Maharashtra', 'full_time', 'on_site', 'fresher', 'Excel, Operations, Documentation, Communication', 20000, 32000, 4, 'Coordinate daily operational workflows, reports and partner communication.', 'Graduate or diploma holder with basic Excel and communication skills.', 48, False),
        ('HealthSync Technologies', 'Backend Developer', 'technology', 'Pune, Maharashtra', 'full_time', 'hybrid', '1_3', 'Python, Django, PostgreSQL, APIs, Docker', 60000, 95000, 2, 'Build secure backend services for healthcare workflow products.', '1–3 years in backend development and solid database/API fundamentals.', 44, True),
        ('HealthSync Technologies', 'Customer Success Executive', 'customer_service', 'Pune, Maharashtra', 'full_time', 'on_site', '0_1', 'Communication, CRM, Customer Support, Excel', 24000, 36000, 3, 'Support customers through onboarding, issue resolution and product education.', 'Strong communication and problem-solving skills with a customer-first approach.', 30, False),
        ('MarketLoop', 'Digital Marketing Executive', 'marketing', 'Ahmedabad, Gujarat', 'full_time', 'hybrid', '0_1', 'SEO, Social Media, Google Analytics, Content', 28000, 50000, 3, 'Plan digital campaigns, track performance and improve organic traffic.', 'Basic digital marketing knowledge with familiarity in SEO and analytics.', 32, True),
        ('MarketLoop', 'Business Analyst', 'data', 'Ahmedabad, Gujarat', 'full_time', 'hybrid', '1_3', 'SQL, Excel, Power BI, Business Analysis', 50000, 80000, 2, 'Translate business requirements into actionable dashboards and process improvements.', '1–3 years of analytics or business analysis experience with strong SQL/Excel.', 38, False),
        ('MarketLoop', 'Recruitment Coordinator', 'human_resources', 'Ahmedabad, Gujarat', 'part_time', 'on_site', 'fresher', 'Recruitment, Communication, Excel, Interview Scheduling', 18000, 28000, 2, 'Coordinate interview schedules, candidate communication and hiring documentation.', 'Good communication, organization and basic spreadsheet skills.', 24, False),
    ]

    today = timezone.localdate()
    for company_name, title, category, location, job_type, work_mode, experience, skills, salary_min, salary_max, openings, description, requirements, days_from_now, is_featured in sample_jobs:
        Job.objects.update_or_create(
            company=company_users[company_name],
            title=title,
            defaults={
                'category': category,
                'description': description,
                'requirements': requirements,
                'location': location,
                'job_type': job_type,
                'work_mode': work_mode,
                'experience': experience,
                'skills': skills,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'openings': openings,
                'deadline': today + timedelta(days=days_from_now),
                'is_active': True,
                'is_featured': is_featured,
            },
        )


def unseed_jobs(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('portal', '0002_job_fields')]
    operations = [migrations.RunPython(seed_jobs, unseed_jobs)]
