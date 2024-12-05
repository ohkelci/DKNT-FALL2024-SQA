# Report

# Dan Mogaka - (activity)
- [lesson learned]
  
# Kelci Jenkins - Continuous Integration (Part 4.d.)
- I implemented continuous integration (CI) in our GitHub repo utilizing GitHub actions. From the lessons learned in class, I ended up using Codacy with GitHub code scanning to ensure each commit and pull request to the main branch is being analyzed and reported. Throughout this process, static code analysis is being utilized, reported, and uploaded to GitHub. To do this, I used resources from class, experience from workshop 9, and the Codacy documentation.
  
- The first thing I learned is that the use cases of Codacy can be adapted to other CI workflows. Even without GitHub Actions, similar results can be achieved by creating a custom YAML file and implementing CI through third-party tools like Jenkins. The second thing I learned is to make sure the branch name in the YAML file matches the repo branches that you want to monitor. If not, it will not work. I made the mistake of having the branch name as "master", but the branch name was "main" so it did not work at first. The third thing I learned is that through CI, issues can be found and reported. You can assign issues to other users who are in the repository, make the needed changes, and resolve the issue. It's similar to Jira, and during my internship, the company utilized GitLab and had it integrated with Jira. Any issues that were caught through CI could be sent to Jira, users were assigned to the issue, and it could be resolved through GitLab.
  
# Noah Jones - (activity)
- My part of this project was an automated security scanning system using Git hooks to analyze Python code for vulnerabilities during commits. The system consists of a pre-commit hook and a Python script that leverages the Bandit security scanner, automatically generating CSV reports detailing any security issues found.
The system uses Python's subprocess for Git integration and Bandit for security scanning. Through this implementation, I learned valuable lessons about Git hook capabilities and cross-platform development challenges. The project highlighted the importance of robust error handling and clear security reporting in development workflows.

# Traevon Wright Fuzzing (Part 4.b) & Forensics (Part 4.c)
- With the Fuzzing, I ran different inputs with 5 different python methods and logged the results. I learned about the importance of good input handling and an effective way of testing the system resillience.
- I integrated forensics into my code by establishing logging for the inputs, key events, and outputs of the program. I learned about how forensics can be used to trace the flow of a program and how it can be an effective way of ensuring the integrity of the program and its data. 
