import zkrq_repository


def get(queue_id=None, time_to_wait=None):
    validate_queue_id(queue_id)
    validate_time_to_wait(time_to_wait)

    params = {}
    if queue_id:
        params['queueID'] = queue_id
    if time_to_wait:
        params['ttw'] = time_to_wait

    response = zkrq_repository.get(params)
    response.raise_for_status()

    parsed_response = response.json()
    if parsed_response['package'] is None:
        return None
    return parsed_response


def validate_queue_id(queue_id):
    if isinstance(queue_id, str):
        if queue_id == '' or ' ' in queue_id:
            raise ValueError('queue_id')
        return
    if queue_id is not None:
        raise TypeError('queue_id')


def validate_time_to_wait(time_to_wait):
    if isinstance(time_to_wait, int):
        if time_to_wait <= 0:
            raise ValueError('time_to_wait')
        return
    if time_to_wait is not None:
        raise TypeError('time_to_wait')
