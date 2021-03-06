"""

TODO:
    * Would be amazing if we did not have to maintain a schema here and
      also a seperate but exactly similar database model. Is there a way
      to share attributes?

"""
from flask_restplus import Model, fields

from _orchest.internals import config as _config


# Namespace: Sessions
server = Model('Server', {
    'url': fields.String(
        required=True,
        description='URL of the server'),
    'hostname': fields.String(
        required=True,
        default='localhost',
        description='Hostname'),
    'port': fields.Integer(
        required=True,
        default=8888,
        description='Port to access the server'),
    'secure': fields.Boolean(
        required=True,
        description='Any extra security measures'),
    'base_url': fields.String(
        required=True,
        default='/',
        description='Base URL'),
    'token': fields.String(
        required=True,
        description='Token for authentication'),
    'notebook_dir': fields.String(
        required=True,
        default=_config.PIPELINE_DIR,
        description='Working directory'),
    'password': fields.Boolean(
        required=True,
        description='Password if one is set'),
    'pid': fields.Integer(
        required=True,
        description='PID'),
})

session = Model('Session', {
    'pipeline_uuid': fields.String(
        required=True,
        description='UUID of pipeline'),
    'status': fields.String(
        required=True,
        description='Status of session'),
    'jupyter_server_ip': fields.String(
        required=True,
        description='IP of the jupyter-server'),
    'notebook_server_info': fields.Nested(
        server,
        required=True,
        description='Jupyter notebook server connection info')
})

sessions = Model('Sessions', {
    'sessions': fields.List(
        fields.Nested(session),
        description='Currently running sessions')
})

pipeline = Model('Pipeline', {
    'pipeline_uuid': fields.String(
        required=True,
        description='UUID of pipeline'),
    'pipeline_dir': fields.String(
        required=True,
        description='Path to pipeline files'),
    'host_userdir': fields.String(
        required=True,
        description='Host path to userdir')
})

# Namespace: Runs & Experiments
pipeline_run_config = Model('PipelineRunConfig', {
    'pipeline_dir': fields.String(
        required=True,
        description='Path to pipeline files'),
})

pipeline_run_spec = Model('PipelineRunSpec', {
    'uuids': fields.List(
        fields.String(),
        required=False,
        description='UUIDs of pipeline steps'),
    'run_type': fields.String(
        required=False,
        default='full',  # TODO: check whether default is used if required=False
        description='Type of run',
        enum=['full', 'selection', 'incoming']),
})

pipeline_run_pipeline_step = Model('PipelineRunPipelineStep', {
    'run_uuid': fields.String(
        required=True,
        description='UUID of the run'),
    'step_uuid': fields.String(
        required=True,
        description='UUID of the pipeline step'),
    'status': fields.String(
        required=True,
        description='Status of the step',
        enum=['PENDING', 'STARTED', 'SUCCESS', 'FAILURE', 'ABORTED', 'REVOKED']),
    'started_time': fields.String(
        required=True,
        description='Time at which the step started executing'),
    'finished_time': fields.String(
        required=True,
        description='Time at which the step finished executing'),
})

pipeline_run = Model('Run', {
    'run_uuid': fields.String(
        required=True,
        description='UUID of run'),
    'pipeline_uuid': fields.String(
        required=True,
        description='UUID of pipeline'),
    'status': fields.String(
        required=True,
        description='Status of the run'),
    'pipeline_steps': fields.List(  # TODO: rename
        fields.Nested(pipeline_run_pipeline_step),
        description='Status of each pipeline step'),
})

interactive_run_config = pipeline_run_config.inherit('InteractiveRunConfig', {
    'pipeline-dir': fields.String(
        required=True,
        description='Absolute path on the host to the "pipeline-dir"'),
})

interactive_run_spec = pipeline_run_spec.inherit('InteractiveRunSpec', {
    'pipeline_description': fields.Raw(
        required=True,
        description='Pipeline description in JSON'),
    'run_config': fields.Nested(
        interactive_run_config,
        required=True,
        description='Configuration for compute backend'),
})

interactive_run = pipeline_run.inherit('InteractiveRun', {})

interactive_runs = Model('InteractiveRuns', {
    'runs': fields.List(
        fields.Nested(interactive_run),
        description='All ran interactive runs during this "lifecycle" of Orchest')
})

status_update = Model('StatusUpdate', {
    'status': fields.String(
        required=True,
        description='New status of executable, e.g. pipeline or step',
        enum=['PENDING', 'STARTED', 'SUCCESS', 'FAILURE', 'ABORTED', 'REVOKED']),
})

# Namespace: Experiments.
non_interactive_run_config = pipeline_run_config.inherit('NonInteractiveRunConfig', {
    # Needed for the celery-worker to set the new pipeline-dir for
    # experiments. Note that the `orchest-webserver` has this value
    # stored in the ENV variable `HOST_USER_DIR`.
    'host_user_dir': fields.String(
        required=True,
        description='Path to the /userdir on the host'),
})

non_interactive_run_spec = pipeline_run_spec.inherit('NonInteractiveRunSpec', {
    'run_config': fields.Nested(
        non_interactive_run_config,
        required=True,
        description='Configuration for compute backend'),
    'scheduled_start': fields.String(  # TODO: make DateTime
        required=False,
        # default=datetime.utcnow().isoformat(),
        description='Time at which the run is scheduled to start'),
})

non_interactive_run = pipeline_run.inherit('NonInteractiveRun', {
    'experiment_uuid': fields.String(
        required=True,
        description='UUID for experiment'),
    'pipeline_run_id': fields.Integer(
        required=True,
        description='Respective run ID in experiment'),
})

experiment_spec = Model('ExperimentSpecification', {
    'experiment_uuid': fields.String(
        required=True,
        description='UUID for experiment'),
    'pipeline_uuid': fields.String(
        required=True,
        description='UUID of pipeline'),
    'pipeline_descriptions': fields.List(
        fields.Raw(
            description='Pipeline description in JSON'
        ),
        required=True,
        description='Collection of pipeline descriptions',
    ),
    'pipeline_run_ids': fields.List(
        fields.Integer(
            description=('Pipeline index corresponding to respective '
                         'list entries in pipeline_descriptions.')
        ),
        required=True,
        description='Collection of pipeline description indices.',
    ),
    'pipeline_run_spec': fields.Nested(
        non_interactive_run_spec,
        required=True,
        description='Specification of the pipeline runs, e.g. "full", "incoming" etc'),
    'scheduled_start': fields.String(
        required=True,
        description='Time at which the experiment is scheduled to start'),
})

experiment = Model('Experiment', {
    'experiment_uuid': fields.String(
        required=True,
        description='UUID for experiment'),
    'pipeline_uuid': fields.String(
        required=True,
        description='UUID of pipeline'),
    'total_number_of_pipeline_runs': fields.Integer(
        required=True,
        description='Total number of pipeline runs part of the experiment'),
    'pipeline_runs': fields.List(
        fields.Nested(non_interactive_run),
        description='Collection of pipeline runs part of the experiment'),
    'scheduled_start': fields.String(
        required=True,
        description='Time at which the experiment is scheduled to start'),
    'completed_pipeline_runs': fields.Integer(
        required=True,
        default=0,
        description='Number of completed pipeline runs part of the experiment'),
})

experiments = Model('Experiments', {
    'experiments': fields.List(
        fields.Nested(experiment),
        description='Collection of all experiments'),
})
