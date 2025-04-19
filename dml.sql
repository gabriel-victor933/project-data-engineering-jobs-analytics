/* SELECT * 
FROM jobs
JOIN jobs_skills
ON jobs.id = jobs_skills.job_id
JOIN skills
ON jobs_skills.skill_id = skills.id
LIMIT 10; */

SELECT 
  relname AS tabela,
  pg_size_pretty(pg_total_relation_size(relid)) AS tamanho
FROM pg_catalog.pg_statio_user_tables 
ORDER BY pg_total_relation_size(relid) DESC;