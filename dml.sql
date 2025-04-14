/* SELECT * 
FROM jobs
JOIN jobs_skills
ON jobs.id = jobs_skills.job_id
JOIN skills
ON skills.id = jobs_skills.skill_id; */


/* DELETE FROM jobs_skills;
DELETE FROM jobs; */