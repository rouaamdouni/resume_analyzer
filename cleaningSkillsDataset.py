import csv

# Define the job categories and their corresponding recommended skills
job_categories = {
    'Web Development': ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento', 'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK'],
    'Mobile App Development': ['Swift', 'Kotlin', 'Java', 'React Native', 'iOS', 'Android', 'Flutter', 'Xamarin', 'Mobile UI/UX Design'],
    'Data Science': ['Python', 'R', 'SQL', 'Machine Learning', 'Data Analysis', 'Statistics', 'TensorFlow', 'PyTorch', 'Big Data', 'Hadoop', 'Spark', 'Deep Learning'],
    'Database Administration': ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Database Optimization', 'Data Modeling'],
    'Network Engineering': ['Cisco', 'CCNA', 'CCNP', 'Network Security', 'Routing and Switching', 'Firewall Configuration', 'TCP/IP'],
    'DevOps': ['Docker', 'Kubernetes', 'Jenkins', 'Ansible', 'Git', 'Continuous Integration/Continuous Deployment (CI/CD)', 'Infrastructure as Code (IaC)'],
    'Cybersecurity': ['Penetration Testing', 'Ethical Hacking', 'Firewall Management', 'Security Auditing', 'SIEM (Security Information and Event Management)', 'Network Security'],
    'Data Analyst': ['Excel', 'SQL', 'Data Visualization', 'Statistics', 'Python', 'R', 'Data Cleaning', 'Data Wrangling'],
    'Web Developer (Senior)': ['React', 'Node.js', 'Express', 'MongoDB', 'RESTful APIs', 'Webpack', 'GraphQL', 'CI/CD', 'Microservices Architecture', 'Responsive Design'],
    'Web Developer (Junior)': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Git', 'Basic SQL', 'Responsive Design', 'Web Accessibility'],
    'Engineer': ['Problem Solving', 'Algorithm Design', 'Object-Oriented Programming (OOP)', 'Debugging', 'Version Control (Git)', 'Linux', 'Scripting (e.g., Python)'],
    'iOS Development': ['Swift', 'iOS SDK', 'Xcode', 'UIKit', 'Core Data', 'RESTful APIs', 'Auto Layout', 'MVVM Architecture', 'Unit Testing in iOS'],
    'Business Analyst': ['Business Intelligence', 'Requirements Analysis', 'Data Modeling', 'Process Mapping', 'SQL', 'Excel', 'Tableau', 'Power BI'],
    'UX/UI Designer': ['User Research', 'Wireframing', 'Prototyping', 'UI Design', 'UX Design', 'Figma', 'Sketch', 'Adobe XD', 'Usability Testing'],
    'Quality Assurance (QA) Tester': ['Manual Testing', 'Automated Testing', 'Test Planning', 'Bug Tracking', 'Selenium', 'JUnit', 'TestNG', 'Performance Testing'],
    'Project Manager': ['Project Planning', 'Agile Methodology', 'Scrum', 'Risk Management', 'Communication Skills', 'Team Collaboration', 'Budgeting', 'Jira'],
    'Full Stack Developer': ['React', 'Node.js', 'Express', 'MongoDB', 'RESTful APIs', 'HTML', 'CSS', 'Javascript', 'SQL', 'Git', 'CI/CD'],
    'Machine Learning Engineer': ['Python', 'TensorFlow', 'PyTorch', 'Machine Learning Algorithms', 'Deep Learning', 'Natural Language Processing (NLP)', 'Computer Vision', 'Data Engineering'],
    'Cloud Solutions Architect': ['AWS', 'Azure', 'Google Cloud Platform (GCP)', 'Cloud Architecture', 'Microservices', 'Docker', 'Kubernetes', 'Serverless'],
    'Blockchain Developer': ['Blockchain', 'Smart Contracts', 'Solidity', 'Ethereum', 'Hyperledger Fabric', 'Decentralized Applications (DApps)', 'Cryptocurrency'],
    'Game Developer': ['Unity', 'C#', 'Game Design', '3D Modeling', 'Game Physics', 'VR/AR Development', 'Game Testing', 'OpenGL'],
    'Technical Writer': ['Technical Writing', 'Documentation', 'API Documentation', 'Markdown', 'Version Control (Git)', 'Communication Skills'],
    # Add more job categories and their skills as needed
}

# Specify the CSV file path
csv_file_path = 'job_skills_extended.csv'

# Write data to CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['Job Category', 'Skills'])

    # Write data rows
    for job_category, skills in job_categories.items():
        csv_writer.writerow([job_category, ', '.join(skills)])

print(f"CSV file '{csv_file_path}' created successfully.")
