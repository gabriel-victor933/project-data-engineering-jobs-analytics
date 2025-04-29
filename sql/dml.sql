/* SELECT * 
FROM jobs
JOIN jobs_skills
ON jobs.id = jobs_skills.job_id
JOIN skills
ON jobs_skills.skill_id = skills.id
LIMIT 10; */

SELECT COUNT(*) FROM jobs;