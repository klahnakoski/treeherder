SELECT
  repo.name as `repo.branch.name`,
  repo.dvcs_type as `repo.branch.type`,
  repo.url as `repo.branch.url`,
  repo.codebase as `repo.branch.codebase`,
  coalesce(push.long_revision, push.short_revision, push.revision_hash) as `repo.push.revision`,
  push.id as `repo.push.id`,
  push.author as `repo.push.author`,
  push.push_timestamp as `repo.push.timestamp`,
  n.id as `note.id`,
  nfc.name as `note.failure_classification`,
  n.who as `note.who`,
  n.note as `note.text`,
  n.note_timestamp as `note.timestamp`, 
  coalesce(build.os_name, build.architecture) as `build.platform`,
  build.platform as `build.raw_platform`,
  m_platform.os_name as `run.machine.os_type`,
  m_platform.platform as `run.machine.os`,
  m_platform.architecture as `machine.architecture`,
  machine.name as `run.machine.name`,
  machine.first_timestamp as `run.machine.first_timestamp`,
  machine.last_timestamp as `run.machine.last_timestamp`,
  oo.name as `build.type`, 
  j.id as `job.id`,
  jt.name as `job.name`,
  jt.symbol as `job.symbol`,
  jg.name as `job.group.name`,
  jg.symbol as `job.group.symbol`,
  prod.name as `build.product`,
  fc.name as `job.failure_classification`,
  j.who as `run.key`,
  j.reason as `action.reason`,
  j.result as `action.buildbot_status`,
  j.state as `action.state`,
  j.submit_timestamp as `action.request_time`,
  j.start_timestamp as `action.start_time`,
  j.end_timestamp as `action.end_time`,
  j.last_modified as `job.last_modified`,
  j.running_eta as `action.eta`,
  j.tier as `action.tier`
FROM
  job j
LEFT JOIN
  (
  SELECT
    vr.result_set_id id, 
    concat('[', GROUP_CONCAT(concat('{"id":', rev.id, 
    ', "revision":', string.quote(coalesce(rev.long_revision, rev.short_revision, rev.revision)),
    ', "author":', string.quote(rev.author),
    ', "comments":', string.quote(rev.comments),
    '}')), ']') as `description`
  FROM    
    revision rev
  LEFT JOIN
    revision_map vr on rev.id=vr.revision_id
  GROUP BY
    vr.result_set_id
  ) revs on revs.id=j.result_set_id
LEFT JOIN
  revision rev on vr.revision_id = rev.id
LEFT JOIN
  job_note n on n.job_id = j.id
LEFT JOIN
  job_log_url u on u.job_id = j.id
LEFT JOIN
  bug_job_map bj on bj.job_id = j.id
LEFT JOIN
  treeherder.repository repo on repo.id=rev.repository_id
LEFT JOIN
  treeherder.build_platform build on build.id = j.build_platform_id
LEFT JOIN
  treeherder.machine_platform m_platform on m_platform.id = j.machine_platform_id
LEFT JOIN
  treeherder.machine on machine.id = j.machine_id
LEFT JOIN
  treeherder.option_collection oc on oc.option_collection_hash = j.option_collection_hash
LEFT JOIN
  treeherder.`option` oo on oo.id = oc.option_id
LEFT JOIN
  treeherder.job_type jt on jt.id = j.job_type_id
LEFT JOIN
  treeherder.job_group jg on jg.id = jt.job_group_id
LEFT JOIN
  treeherder.product prod on prod.id = j.product_id
LEFT JOIN
  treeherder.failure_classification fc on fc.id = j.failure_classification_id
LEFT JOIN
  treeherder.failure_classification nfc on fc.id = n.failure_classification_id