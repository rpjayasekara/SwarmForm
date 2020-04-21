from fireworks import Firework, ScriptTask
from swarmform import ParallelTask


def combine_fws_sequentially(swarmpad, fw_ids, parallely_clustered_fws, parallely_clustered_fw_ids):
    """
    Combine a set of fireworks into a single firework

    Args:
        swarmpad (SwarmPad)
        fw_ids (list): id of the fireworks to be combined sequentially
        parallely_clustered_fws(list): list of fireworks which are clustered parallely,but not added to the SwarmPad
        parallely_clustered_fw_ids(dict): dictionary of {cluster id: firework id } of parallely clustered fireworks

    Returns:
        combinedFW (Firework)
    """

    fws = parallely_clustered_fws

    parallel_fw_ids = parallely_clustered_fw_ids.values()

    firetask = []

    # Get the firetasks of parallel fireworks and add to firetask list
    for parallel_fw in fws:
        for task in parallel_fw.tasks:
            firetask.append(task)

    # Get firework from swarmpad if it is not available in parallely_clustered_fws list
    for fw_id in fw_ids:
        if fw_id not in parallel_fw_ids:
            firetask_list = swarmpad.get_fw_by_id(fw_id).spec['_tasks']
            num_firetasks = len(firetask_list)
            # Check whether a firework has no firetasks
            if num_firetasks == 0:
                raise ValueError('No Firetasks available in the Firework')
            # Check whether the firework has multiple firetasks - Not checking firetasks recursively at the moment
            if num_firetasks > 1:
                # If multiple firetasks are available, add each task to firetask list
                for firetask_index in range(0, num_firetasks):
                    firetask.append(firetask_list[firetask_index])
            # If only a single firetask is there, get the first firetask and add it to the combined firetask
            else:
                firetask.append(firetask_list[0])

    # Create a firework from the combined firetasks
    combined_fw = Firework(firetask)
    swarmpad.m_logger.info('Sequentially clustered {} Fireworks to firework_id {}'.format(fw_ids, combined_fw.fw_id))
    return combined_fw


# TODO: Resolve the following assumptions
'''
* Only scriptTasks are given
* Command in scriptTasks are static
* fws to combine parallely have only a single firetask
'''


def combine_fws_parallely(swarmpad, fw_ids):
    """
    Combine a set of firetasks into a single firetask which runs all the given tasks parallely

    Args:
        swarmpad (SwarmPad)
        fw_ids (list): id of the fireworks to be combined

    Returns:
        combined_firework (FireWork): Parallely combined FireWork object
    """

    # Get each task in each firework and append to firetask list in the order of traversal
    firetasks_to_combine = []
    for fw_id in fw_ids:
        firetask_in_fw = swarmpad.get_fw_by_id(fw_id).spec['_tasks'][0]
        if isinstance(firetask_in_fw, ScriptTask):
            firetasks_to_combine.append(firetask_in_fw)
        else:
            raise ValueError('Spec of Firework with id {} does not contain an object of type ScriptTask '.format(fw_id))

    combined_firetask = ParallelTask.from_firetasks(firetasks_to_combine)
    combined_firework = Firework(combined_firetask)
    swarmpad.m_logger.info('Parallely Clustered {} to firework_id {}'.format(fw_ids, combined_firework.fw_id))

    return combined_firework


def update_parent_child_relationships(links_dict, old_id, new_id):
    """
        Update the parent-child relationships after clustering a firework
        by replacing all the instances of old_id with new_id
        Args:
            links_dict (list): Existing parent-child relationship list
            old_id (int): Existing id of the firework
            new_id (int): New id of the firework

        Returns:
            links_dict (list): Updated parent-child relationship list
        """

    # Enumerate child ids and replace it with the new id
    for parent_id in links_dict:
        child_id_list = links_dict[parent_id]
        for index, ID in enumerate(child_id_list):
            if ID == old_id:
                child_id_list[index] = new_id
                break

    # Enumerate parent ids and replace it with the new id
    if old_id in links_dict:
        links_dict[new_id] = links_dict.pop(old_id)
    return links_dict
