# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import re
from copy import deepcopy

STANDARD_PROMETHEUS_METRICS = {
    'server_cleanup_lastStarted_startTimestamp_milliseconds': 'server.cleanup.lastStarted.startTimestamp.milliseconds',
    'server_cleanup_lastFinished_startTimestamp_milliseconds': 'server.cleanup.lastFinished.startTimestamp.milliseconds',
    'server_cleanup_lastFinished_finishTimestamp_milliseconds': 'server.cleanup.lastFinished.finishTimestamp.milliseconds',
    'runningBuilds_numberOfUnprocessedMessages': 'runningBuilds.numberOfUnprocessedMessages',
    'node_locks_taken': 'node.locks.taken',
    'io_build_artifacts_writes_bytes': 'io.build.artifacts.writes.bytes',
    'io_build_artifacts_reads_bytes': 'io.build.artifacts.reads.bytes',
    'io_agent_updates_reads_bytes': 'io.agent.updates.reads.bytes',
    'cloud_tccPluginsLoaded': 'cloud.tccPluginsLoaded',
    'cloud_license_runningSelfHostedBuilds': 'cloud.license.runningSelfHostedBuilds',
    'cleanup_build_processing': 'cleanup.build.processing',
    'buildType_branches_updateTime_milliseconds': 'buildType.branches.updateTime.milliseconds',
    'build_statistics_delay': 'build.statistics.delay',
    'build_log_flowAwareIndex_init_time_milliseconds': 'build.log.flowAwareIndex.init.time.milliseconds',
    'agents_cloud_starting': 'agents.cloud.starting',
    'agents_connected_authorized': 'agents.connected.authorized',
    'agents_running_builds': 'agents.running.builds',
    'buildConfigurations_active': 'build.configs.active',
    'buildConfigurations_composite_active': 'build.configs.composite.active',
    'buildConfigurations': 'build.configs',
    'build_messages_incoming': 'build.messages.incoming',
    'build_messages_processing': 'build.messages.processing',
    'build_queue_estimates_processing': 'build.queue.estimates.processing',
    'build_queue_incoming': 'build.queue.incoming',
    'build_queue_processing': 'build.queue.processing',
    'build_service_messages': 'build.service.messages',
    'builds_finished': 'builds.finished',
    'builds': 'builds',
    'builds_queued': 'builds.queued',
    'builds_running': 'builds.running',
    'builds_started': 'builds.started',
    'building_hosted_agents': 'building_hosted_agents',
    'cloud_active_nodes': 'cloud.active_nodes',
    'cloud_agent_afterBuild': 'cloud.agent.active_duration_afterBuild',
    'cloud_agent_beforeBuild': 'cloud.agent.active_duration_beforeBuild',
    'cloud_agent_beforeRegister': 'cloud.agent.starting_duration_beforeRegister',
    'cloud_agent_betweenBuild': 'cloud.agent.active_duration_betweenBuilds',
    'cloud_agent_totalBuild': 'cloud.agent.total_build_duration',
    'cloud_agent_totalBuildBeforeFinish': 'cloud.agent.total_build_duration_beforeFinish',
    'cloud_agent_useless': 'cloud.agent.idle_duration',
    'cloud_build_stuckCanceled': 'cloud.build_stuck_canceled',
    'cloud_pluginsFailedToLoad': 'cloud.plugins.failed_loading',
    'cloud_server_lowMemory_gcUsageExceeded': 'cloud.server.gc_usage_exceeded_errors',
    'cloud_server_lowMemory_highTotal': 'cloud.server.high_total_memory_errors',
    'cloud_tccPluginLoaded': 'cloud.tcc_plugin_loaded',
    'cloud_images_count': 'cloud.images',
    'current_full_agent_waiting_instances': 'current_full_agent_wait_instances',
    'current_full_agent_waiting_time_total': 'current_full_agent_wait_time_total',
    'current_full_agent_waiting_time_max': 'current_full_agent_wait_time_max',
    'full_agent_waiting_time_quantile': 'full_agent_wait_time.quantile',
    'cpu_count': 'cpu.count',
    'cpu_usage_process': 'cpu.usage.process',
    'cpu_usage_system': 'cpu.usage.system',
    'database_connections_active': 'database.connections.active',
    'db_table_writes': 'db.table.writes',
    'diskUsage_artifacts_bytes': 'disk_usage.artifacts.bytes',
    'diskUsage_logs_bytes': 'disk_usage.logs.bytes',
    'executors_asyncXmlRpc_activeTasks': 'executors.asyncXmlRpc.activeTasks',
    'executors_asyncXmlRpc_completedTasks': 'executors.asyncXmlRpc.completedTasks',
    'executors_asyncXmlRpc_maxQueueCapacity': 'executors.asyncXmlRpc.maxQueueCapacity',
    'executors_asyncXmlRpc_poolSize': 'executors.asyncXmlRpc.poolSize',
    'executors_asyncXmlRpc_queuedTasks': 'executors.asyncXmlRpc.queuedTasks',
    'executors_asyncXmlRpc_rejectsCount': 'executors.asyncXmlRpc.rejectsCount',
    'executors_baseVcsExecutor_activeTasks': 'executors.baseVcsExecutor.activeTasks',
    'executors_baseVcsExecutor_completedTasks': 'executors.baseVcsExecutor.completedTasks',
    'executors_baseVcsExecutor_maxQueueCapacity': 'executors.baseVcsExecutor.maxQueueCapacity',
    'executors_baseVcsExecutor_poolSize': 'executors.baseVcsExecutor.poolSize',
    'executors_baseVcsExecutor_queuedTasks': 'executors.baseVcsExecutor.queuedTasks',
    'executors_baseVcsExecutor_rejectsCount': 'executors.baseVcsExecutor.rejectsCount',
    'executors_cleanupExecutor_activeTasks': 'executors.cleanupExecutor.activeTasks',
    'executors_cleanupExecutor_completedTasks': 'executors.cleanupExecutor.completedTasks',
    'executors_cleanupExecutor_maxQueueCapacity': 'executors.cleanupExecutor.maxQueueCapacity',
    'executors_cleanupExecutor_poolSize': 'executors.cleanupExecutor.poolSize',
    'executors_cleanupExecutor_queuedTasks': 'executors.cleanupExecutor.queuedTasks',
    'executors_cleanupExecutor_rejectsCount': 'executors.cleanupExecutor.rejectsCount',
    'executors_lowPriorityExecutor_activeTasks': 'executors.lowPriorityExecutor.activeTasks',
    'executors_lowPriorityExecutor_completedTasks': 'executors.lowPriorityExecutor.completedTasks',
    'executors_lowPriorityExecutor_maxQueueCapacity': 'executors.lowPriorityExecutor.maxQueueCapacity',
    'executors_lowPriorityExecutor_poolSize': 'executors.lowPriorityExecutor.poolSize',
    'executors_lowPriorityExecutor_queuedTasks': 'executors.lowPriorityExecutor.queuedTasks',
    'executors_lowPriorityExecutor_rejectsCount': 'executors.lowPriorityExecutor.rejectsCount',
    'executors_normalExecutor_activeTasks': 'executors.normalExecutor.activeTasks',
    'executors_normalExecutor_completedTasks': 'executors.normalExecutor.completedTasks',
    'executors_normalExecutor_maxQueueCapacity': 'executors.normalExecutor.maxQueueCapacity',
    'executors_normalExecutor_poolSize': 'executors.normalExecutor.poolSize',
    'executors_normalExecutor_queuedTasks': 'executors.normalExecutor.queuedTasks',
    'executors_normalExecutor_rejectsCount': 'executors.normalExecutor.rejectsCount',
    'executors_periodicalVcsExecutor_activeTasks': 'executors.periodicalVcsExecutor.activeTasks',
    'executors_periodicalVcsExecutor_completedTasks': 'executors.periodicalVcsExecutor.completedTasks',
    'executors_periodicalVcsExecutor_maxQueueCapacity': 'executors.periodicalVcsExecutor.maxQueueCapacity',
    'executors_periodicalVcsExecutor_poolSize': 'executors.periodicalVcsExecutor.poolSize',
    'executors_periodicalVcsExecutor_queuedTasks': 'executors.periodicalVcsExecutor.queuedTasks',
    'executors_periodicalVcsExecutor_rejectsCount': 'executors.periodicalVcsExecutor.rejectsCount',
    'executors_tomcatHttpThreadPool_activeTasks': 'executors.tomcatHttpThreadPool.activeTasks',
    'executors_tomcatHttpThreadPool_poolSize': 'executors.tomcatHttpThreadPool.poolSize',
    'executors_triggersExecutor_activeTasks': 'executors.triggersExecutor.activeTasks',
    'executors_triggersExecutor_completedTasks': 'executors.triggersExecutor.completedTasks',
    'executors_triggersExecutor_maxQueueCapacity': 'executors.triggersExecutor.maxQueueCapacity',
    'executors_triggersExecutor_poolSize': 'executors.triggersExecutor.poolSize',
    'executors_triggersExecutor_queuedTasks': 'executors.triggersExecutor.queuedTasks',
    'executors_triggersExecutor_rejectsCount': 'executors.triggersExecutor.rejectsCount',
    'httpSessions_active': 'httpSessions.active',
    'io_build_log_reads_bytes': 'io.build.log.reads.bytes',
    'io_build_log_writes_bytes': 'io.build.log.writes.bytes',
    'io_build_patch_writes_bytes': 'io.build.patch.writes.bytes',
    'jvm_buffer_count': 'jvm.buffers_count',
    'jvm_buffer_memory_used_bytes': 'jvm.buffer.memory.used.bytes',
    'jvm_buffer_total_capacity_bytes': 'jvm.buffer.total.capacity.bytes',
    'jvm_gc_count': 'jvm.gc.count',
    'jvm_gc_duration_total_milliseconds': 'jvm.gc.duration.total.milliseconds',
    'jvm_gc_live_data_size_bytes': 'jvm.gc.live.data.size.bytes',
    'jvm_gc_max_data_size_bytes': 'jvm.gc.max.data.size.bytes',
    'jvm_gc_memory_allocated_bytes': 'jvm.gc.memory.allocated.bytes',
    'jvm_gc_memory_promoted_bytes': 'jvm.gc.memory.promoted.bytes',
    'jvm_memory_committed_bytes': 'jvm.memory.committed.bytes',
    'jvm_memory_max_bytes': 'jvm.memory.max.bytes',
    'jvm_memory_used_bytes': 'jvm.memory.used.bytes',
    'jvm_threads_daemon': 'jvm.threads.daemon',
    'jvm_threads': 'jvm.threads',
    'node_events_unprocessed': 'node.events.unprocessed',
    'node_events_processing': 'node.events.processing',
    'node_events_publishing': 'node.events.publishing',
    'node_tasks_accepted': 'node.tasks.accepted',
    'node_tasks_finished': 'node.tasks.finished',
    'node_tasks_pending': 'node.tasks.pending',
    'projects_active': 'projects.active',
    'projects': 'projects',
    'runningBuildsOfUnprocessedMessages': 'runningBuilds.UnprocessedMessages',
    'server_uptime_milliseconds': 'server.uptime.milliseconds',
    'system_load_average_1m': 'system.load.average.1m',
    'teamcity_cache_InvestigationTestRunsHolder_projectScopes': 'cache.InvestigationTestRunsHolder'
    '.projectScopes',
    'teamcity_cache_InvestigationTestRunsHolder_testNames': 'cache.InvestigationTestRunsHolder.testNames',
    'teamcity_cache_InvestigationTestRunsHolder_testRuns': 'cache.InvestigationTestRunsHolder.testRuns',
    'users_active': 'users.active',
    'vcsRootInstances_active': 'vcsRootInstances.active',
    'vcsRoots': 'vcsRoots',
    'vcs_get_current_state_calls': 'vcs.get.current.state.calls',
}

HISTOGRAM_METRICS = {'http_requests_duration_milliseconds': 'http.requests.duration.milliseconds'}

SUMMARY_METRICS = {
    'build_triggers_execution_milliseconds': 'build.triggers.execution.milliseconds',
    'build_triggers_per_type_execution_milliseconds': 'build.triggers.per.type.execution.milliseconds',
    'finishingBuild_buildFinishDelay_milliseconds': 'finishingBuild.buildFinishDelay.milliseconds',
    'full_agent_waiting_time_milliseconds': 'full.agent.waiting.time.milliseconds',
    'build_queue_optimization_time_milliseconds': 'build.queue.optimization.time.milliseconds',
    'process_queue_milliseconds': 'process.queue.milliseconds',
    'process_queue_parts_milliseconds': 'process.queue.parts.milliseconds',
    'process_websocket_send_pending_messages_milliseconds': 'process.websocket.send.pending.messages.milliseconds',
    'pullRequests_batch_time_milliseconds': 'pullRequests.batch.time.milliseconds',
    'pullRequests_single_time_milliseconds': 'pullRequests.single.time.milliseconds',
    'queuedBuild_waitingTime_milliseconds': 'queuedBuild.waitingTime.milliseconds',
    'startingBuild_buildStartDelay_milliseconds': 'startingBuild.buildStartDelay.milliseconds',
    'startingBuild_runBuildDelay_milliseconds': 'startingBuild.runBuildDelay.milliseconds',
    'vcs_changes_checking_milliseconds': 'vcs.changes.checking.milliseconds',
    'vcsChangesCollection_delay_milliseconds': 'vcsChangesCollection.delay.milliseconds',
    'vcs_git_fetch_duration_milliseconds': 'vcs.git.fetch.duration.milliseconds',
}

METRIC_MAP = deepcopy(STANDARD_PROMETHEUS_METRICS)
METRIC_MAP.update(HISTOGRAM_METRICS)
METRIC_MAP.update(SUMMARY_METRICS)

SIMPLE_BUILD_STATS_METRICS = {
    'ArtifactsSize': {'name': 'artifacts_size', 'metric_type': 'gauge'},
    'BuildDuration': {'name': 'build_duration', 'metric_type': 'gauge'},
    'BuildDurationNetTime': {'name': 'build_duration.net_time', 'metric_type': 'gauge'},
    'BuildTestStatus': {'name': 'build_test_status', 'metric_type': 'gauge'},
    'InspectionStatsE': {'name': 'inspection_stats_e', 'metric_type': 'gauge'},
    'InspectionStatsW': {'name': 'inspection_stats_w', 'metric_type': 'gauge'},
    'PassedTestCount': {'name': 'passed_test_count', 'metric_type': 'gauge'},
    'FailedTestCount': {'name': 'failed_test_count', 'metric_type': 'gauge'},
    'serverSideBuildFinishing': {'name': 'server_side_build_finishing', 'metric_type': 'gauge'},
    'SuccessRate': {'name': 'success_rate', 'metric_type': 'gauge'},
    'TimeSpentInQueue': {'name': 'time_spent_in_queue', 'metric_type': 'gauge'},
    'TotalTestCount': {'name': 'total_test_count', 'metric_type': 'gauge'},
    'VisibleArtifactsSize': {'name': 'visible_artifacts_size', 'metric_type': 'gauge'},
    'CodeCoverageB': {'name': 'code_coverage.blocks.pct', 'metric_type': 'gauge'},
    'CodeCoverageC': {'name': 'code_coverage.classes.pct', 'metric_type': 'gauge'},
    'CodeCoverageL': {'name': 'code_coverage.lines.pct', 'metric_type': 'gauge'},
    'CodeCoverageM': {'name': 'code_coverage.methods.pct', 'metric_type': 'gauge'},
    'CodeCoverageR': {'name': 'code_coverage.branches.pct', 'metric_type': 'gauge'},
    'CodeCoverageS': {'name': 'code_coverage.statements.pct', 'metric_type': 'gauge'},
    'CodeCoverageAbsBCovered': {'name': 'code_coverage.blocks.covered', 'metric_type': 'gauge'},
    'CodeCoverageAbsBTotal': {'name': 'code_coverage.blocks.total', 'metric_type': 'gauge'},
    'CodeCoverageAbsCCovered': {'name': 'code_coverage.classes.covered', 'metric_type': 'gauge'},
    'CodeCoverageAbsCTotal': {'name': 'code_coverage.classes.total', 'metric_type': 'gauge'},
    'CodeCoverageAbsLCovered': {'name': 'code_coverage.lines.covered', 'metric_type': 'gauge'},
    'CodeCoverageAbsLTotal': {'name': 'code_coverage.lines.total', 'metric_type': 'gauge'},
    'CodeCoverageAbsMCovered': {'name': 'code_coverage.methods.covered', 'metric_type': 'gauge'},
    'CodeCoverageAbsMTotal': {'name': 'code_coverage.methods.total', 'metric_type': 'gauge'},
    'CodeCoverageAbsRCovered': {'name': 'code_coverage.branches.covered', 'metric_type': 'gauge'},
    'CodeCoverageAbsRTotal': {'name': 'code_coverage.branches.total', 'metric_type': 'gauge'},
    'CodeCoverageAbsSCovered': {'name': 'code_coverage.statements.covered', 'metric_type': 'gauge'},
    'CodeCoverageAbsSTotal': {'name': 'code_coverage.statements.total', 'metric_type': 'gauge'},
    'DuplicatorStats': {'name': 'duplicator_stats', 'metric_type': 'gauge'},
    'IgnoredTestCount': {'name': 'ignored_test_count', 'metric_type': 'gauge'},
}

REGEX_BUILD_STATS_METRICS = [
    {
        'regex': r'buildStageDuration\:([\s\S]*)',
        'name': 'build_stage_duration',
        'tags': ('build_stage',),
        'metric_type': 'gauge',
    },
    {
        'regex': r'queueWaitReason\:([\s\S]*)',
        'name': 'queue_wait_reason',
        'tags': ('reason',),
        'metric_type': 'gauge',
    },
    {
        'regex': r'custom\:([\s\S]*)',
        'name': 'custom',
        'tags': ('custom',),
        'metric_type': 'gauge',
    },
]


def build_metric(metric_name):
    additional_tags = []
    name = None
    metric_type = None
    if metric_name in SIMPLE_BUILD_STATS_METRICS:
        metric_mapping = SIMPLE_BUILD_STATS_METRICS[metric_name]
        name = metric_mapping['name']
        metric_type = metric_mapping['metric_type']
    else:
        for regex in REGEX_BUILD_STATS_METRICS:
            name = str(regex['name'])
            metric_type = regex['metric_type']
            results = re.findall(str(regex['regex']), metric_name)
            if len(results) == 0:
                continue
            if len(results) > 0 and isinstance(results[0], tuple):
                tags_values = list(results[0])
            else:
                tags_values = results
            if len(tags_values) == len(regex['tags']):
                for i in range(len(regex['tags'])):
                    additional_tags.append('{}:{}'.format(regex['tags'][i], tags_values[i]))
                return name, additional_tags, metric_type
            return name, tags_values, metric_type
    return name, additional_tags, metric_type
