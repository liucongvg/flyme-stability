import gzip
import os
import re
import shutil
import subprocess
from datetime import datetime
import sys

# from com.flyme.autoanalyser.anranalyser.BaseAnrObj import BaseAnrObj
# from com.flyme.autoanalyser.anranalyser.state.Blocked import Blocked
# from com.flyme.autoanalyser.anranalyser.state.Native import Native
# from com.flyme.autoanalyser.anranalyser.state.Otherstate import Otherstate
# from com.flyme.autoanalyser.anranalyser.state.Runnable import Runnable
# from com.flyme.autoanalyser.anranalyser.state.Suspended import Suspended
# from com.flyme.autoanalyser.anranalyser.state.TimedWaiting import \
#    TimedWaiting
# from com.flyme.autoanalyser.anranalyser.state.Waiting import Waiting
# from com.flyme.autoanalyser.anranalyser.state.WaitingForGcToComplete \
#    import \
#    WaitingForGcToComplete
# from com.flyme.autoanalyser.anranalyser.state.WaitingPerformingGc import \
#    WaitingPerformingGc
from com.flyme.autoanalyser.utils import flymeprint


# def parseDropbox(root_path):
#    try:
#        is_dir = os.path.isdir(root_path)
#        if not is_dir:
#            flymeprint.warning('invalid root dir:' + root_path)
#    except Exception as ex:
#        flymeprint.warning(ex)
#        return
#    # anranalyser
#    anranalyser = os.path.join(root_path, '__anranalyser__')
#    # extract
#    extractall = os.path.join(anranalyser, 'extractall')
#    # use main stack to merge content
#    merge = os.path.join(anranalyser, 'merge')
#    # report bug according to policy
#    bug = os.path.join(anranalyser, 'bug')
#    # undetermined entry which should by analysed manually
#    undetermined = os.path.join(anranalyser, 'undetermined')
#    # notbug directory
#    notbug = os.path.join(anranalyser, 'notbug')
#    if not cleanAndBuildDir(extractall, merge, bug, undetermined, notbug):
#        flymeprint.warning('can not cleanAndBuildDir')
#        return
#    state_obj_dict = dict()
#    all_entries = get_all_entries(root_path)
#    drop_box_entries = all_entries[0]
#    if len(drop_box_entries) == 0:
#        flymeprint.warning('no dropbox files found')
#    data_anr_entries = all_entries[1]
#    if len(data_anr_entries) == 0:
#        flymeprint.warning('no data anr files found')
#    event_log_entries = all_entries[2]
#    if len(event_log_entries) == 0:
#        flymeprint.warning('no event log files found')
#    for fullName in drop_box_entries:
#        # only system_app_anr is concerned
#        # match = re.match('(system_app_anr|data_app_anr).*\.gz', entry)
#        # match = re.match('(system_app_anr).*\.gz', entry)
#        # if not match:
#        #    continue
#        entry = os.path.basename(fullName)
#        flymeprint.debug('start process ---> ' + entry)
#        newEntry = entry.rstrip('.gz')
#        fullNew = os.path.join(extractall, newEntry)
#        wholeFile = extractGz(fullName, fullNew)
#        if wholeFile == '':
#            continue
#        anrobj = parseContent(wholeFile, fullNew, data_anr_entries,
#                              event_log_entries)
#        if not is_a_valid_anr_obj(anrobj):
#            flymeprint.error(entry + ' ---> 信息不完整')
#            continue
#        repair_pid_if_needed(anrobj)
#        if anrobj.mainTrace["thread_state"] == 'Blocked':
#            obj = Blocked(anrobj)
#        elif anrobj.mainTrace["thread_state"] == 'Native':
#            obj = Native(anrobj)
#        elif anrobj.mainTrace["thread_state"] == 'Runnable':
#            obj = Runnable(anrobj)
#        elif anrobj.mainTrace["thread_state"] == 'Suspended':
#            obj = Suspended(anrobj)
#        elif anrobj.mainTrace["thread_state"] == 'TimedWaiting':
#            obj = TimedWaiting(anrobj)
#        elif anrobj.mainTrace["thread_state"] == 'Waiting':
#            obj = Waiting(anrobj)
#        elif anrobj.mainTrace["thread_state"] == 'WaitingForGcToComplete':
#            obj = WaitingForGcToComplete(anrobj)
#        elif anrobj.mainTrace["thread_state"] == 'WaitingPerformGc':
#            obj = WaitingPerformingGc(anrobj)
#        else:
#            obj = Otherstate(anrobj)
#        append_to_merge_or_match(obj, state_obj_dict)
#        flymeprint.debug('end process ---> ' + entry)
#    generate_report(state_obj_dict.values(), merge, bug, undetermined, notbug)


# def get_all_entries(root_path):
#    dropbox_entries = list()
#    data_anr_enties = list()
#    event_log_enties = list()
#    for current_root_dir, current_dir_entries, current_file_entries in os.walk(
#            root_path):
#        for i in current_file_entries:
#            match = re.match('(system_app_anr).*\.gz', i)
#            if match:
#                dropbox_entries.append(os.path.join(current_root_dir, i))
#            match = re.match('traces.*?\.txt', i)
#            if match:
#                data_anr_enties.append(os.path.join(current_root_dir, i))
#            match = re.match('events.*', i)
#            if match:
#                event_log_enties.append(os.path.join(current_root_dir, i))
#    return (dropbox_entries, data_anr_enties, event_log_enties)


# def append_to_merge_or_match(stateObj, state_obj_dict):
#    key = stateObj.get_key()
#    if key in state_obj_dict:
#        flymeprint.debug('duplication for:' + key)
#        state_obj_dict[key].matched_state_list.append(stateObj)
#    else:
#        state_obj_dict[key] = stateObj


# def generate_report(state_obj_list, merge, bug, undetermined, notbug):
#    if len(state_obj_list) == 0:
#        return
#    for i in state_obj_list:
#        i.generate_merge(merge)
#        i.generate_bug_and_undetermined_if_needed(bug, undetermined, notbug)


# def is_a_valid_anr_obj(anrobj):
#    if (anrobj.packageName == 'null'):
#        return False
#    if ('anr_time' not in anrobj.time_and_filepath or 'trace_time' not in
#        anrobj.time_and_filepath or 'dropbox_file_name' not in
#        anrobj.time_and_filepath):
#        return False
#    if (
#                    'trace' not in anrobj.mainTrace or 'thread_state' not in
#                anrobj.mainTrace):
#        return False
#    if ('content' not in anrobj.allMain):
#        return False
#    return True


# def mergeOutput(output, merge):
#    mergedList = list()
#    for outputEntry in os.listdir(output):
#        output_entry = os.path.join(output, outputEntry)
#        fo = open(output_entry, 'r')
#        content = fo.read()
#        entry_mainConcerndTrace = getMainConcernedTrace(content)
#        entry_thread_state = entry_mainConcerndTrace['main']['thread_state']
#        entry_trace = entry_mainConcerndTrace['main']['trace']
#        entry_trace_list = re.findall('at .*?\(', entry_trace)
#        match = re.search('package name:(\n|\r\n)(.*)', content)
#        if not match:
#            print('warning package name not match')
#            continue
#        entry_packageName = match.group(2)
#
#        matched = False
#        for i in mergedList:
#            if entry_packageName in i:
#                state = i[entry_packageName]['thread_state']
#                trace = i[entry_packageName]['trace']
#                if state == entry_thread_state and entry_trace_list_equal(
#                        entry_trace_list, trace):
#                    print("match")
#                    matched = True
#                    break
#
#        if not matched:
#            mergedList.append({entry_packageName: {'thread_state':
# entry_thread_state,
#                                                   'trace': entry_trace_list}})
#            merge_entry = os.path.join(merge, outputEntry)
#            print('Producing ' + merge_entry)
#            shutil.copy(output_entry, merge_entry)


# def entry_trace_list_equal(entry_trace_list, list):
#    if entry_trace_list.__len__() != list.__len__():
#        return False
#    for i in range(list.__len__()):
#        if (entry_trace_list[i] != list[i]):
#            return False
#    return True


def cleanAndBuildDir(*dirs):
    try:
        for i in dirs:
            if os.path.exists(i):
                shutil.rmtree(i)
            os.makedirs(i)
    except Exception as ex:
        flymeprint.warning(ex)
        return False
    return True


def clean_files(*files):
    try:
        for file in files:
            if os.path.exists(file):
                if os.path.isdir(file):
                    shutil.rmtree(file)
                else:
                    os.remove(file)
    except Exception as ex:
        flymeprint.error(ex)


def extractGz(src, dest=None):
    try:
        gz = gzip.open(src, 'rb')
        wholeFile = gz.read().decode('utf-8')
        gz.close()
        if dest != None:
            newFile = open(dest, 'w', encoding='utf-8')
            newFile.write(wholeFile)
            newFile.close()
    except Exception as ex:
        flymeprint.warning(ex)
        return None
    return wholeFile


# def parseContent(content, filename, data_anr_entries, event_log_entries):
#    # processName = getProcessName(content)
#    packageName = get_pname_dropbox(content)
#    anrReason = get_subject_dropbox(content)
#    # build = getbuild(content)
#    cpuUsage = get_cpu_dropbox(content)
#
#    anrTime = get_anr_time_event_log(content, packageName)
#    pid = getPid(content, packageName)
#    anr_in_time = get_anr_in_time(packageName, content)
#    if len(anrTime) == 0:
#        flymeprint.warning('no dropbox anr time, get eventlog anr time')
#        anrTime = getEventLogAnrTime(event_log_entries, packageName)
#        if (len(anrTime) == 0):
#            flymeprint.warning('no eventlog anr time')
#
#    traceTime = get_trace_time_for_anr(content, packageName)
#    if len(traceTime) == 0:
#        flymeprint.warning('no dropbox trace time')
#
#    matchedTime = get_matched_time_for_anr(traceTime, anrTime, anr_in_time)
#    if len(matchedTime) == 0 and len(traceTime) != 0:
#        flymeprint.warning('no dropbox trace matches')
#
#    allMain = get_whole_trace_for_anr(content, packageName, matchedTime,
#                                      anrTime,
#                                      data_anr_entries, anr_in_time)
#    # renderThreadTrace = getRenderThreadTrace(allMain['content'])
#    # binderTrace = getBinderTrace(allMain['content'])
#
#    mainTrace = getTrace(allMain, 'main')
#    # mainThreadstate = mainTrace["thread_state"]
#
#    time_and_filepath = dict()
#    if 'anr_time' in allMain:
#        time_and_filepath['anr_time'] = allMain['anr_time']
#    if 'trace_time' in allMain:
#        time_and_filepath['trace_time'] = allMain['trace_time']
#    if 'anr_trace_file_name' in allMain:
#        time_and_filepath['anr_trace_file_name'] = allMain[
#            'anr_trace_file_name']
#    if 'event_log_path' in allMain:
#        time_and_filepath['event_log_path'] = allMain['event_log_path']
#    if 'anr_time_str' in anr_in_time:
#        time_and_filepath['anr_in_time_str'] = anr_in_time['anr_time_str']
#
#    time_and_filepath['dropbox_file_name'] = filename
#
#    anrobj = BaseAnrObj(time_and_filepath, packageName, anrReason, cpuUsage,
#                        pid,
#                        mainTrace, allMain, content)
#
#    return anrobj


# def repair_pid_if_needed(anrobj):
#    pid = anrobj.pid
#    repaired = False
#    if pid == 'null' or pid == '0':
#        flymeprint.warning('pid:' + pid + ', not valid, try to repair')
#        anr_time = anrobj.time_and_filepath['anr_time']
#        if 'event_log_path' in anrobj.time_and_filepath:
#            # find pid in event log
#            match = re.search(
#                '^\d{2}-\d{2} ' + anr_time + '.*?am_anr.*?\[\d+,(\d+),'
#                                             '' + anrobj.packageName,
#                event_log_entries_cache[
#                    anrobj.time_and_filepath['event_log_path']], re.M)
#            if match:
#                pid = match.group(1)
#                if pid == 'null' or pid == '0':
#                    repaired = False
#                else:
#                    repaired = True
#                    anrobj.pid = pid
#            else:
#                repaired = False
#        if not repaired:
#            if 'anr_trace_file_name' in anrobj.time_and_filepath:
#                # find pid in data anr trace
#                content = data_anr_entries_cache[
#                    anrobj.time_and_filepath['anr_trace_file_name']]
#                repaired = fix_anr_obj_with_content(anrobj, content)
#            else:
#                # find pid in dropbox trace
#                content = anrobj.content
#                repaired = fix_anr_obj_with_content(anrobj, content)
#        if not repaired:
#            flymeprint.warning('repair pid failed')
#        else:
#            flymeprint.debug('repair pid successfully ---> pid:' + anrobj.pid)

def get_trace_pid(content, trace_time, package_name):
    match = re.search(
        '^----- pid (\d+) at \d{4}-\d{2}-\d{2} ' + trace_time + ' -----(\n)Cmd '
                                                                'line: ' +
        package_name,
        content, re.M)
    if match:
        pid = match.group(1)
        return pid
    else:
        return None


# def fix_anr_obj_with_content(anrobj, content):
#    trace_time = anrobj.time_and_filepath['trace_time']
#    match = re.search(
#        '^----- pid (\d+) at \d{4}-\d{2}-\d{2} ' + trace_time + ' -----(
# \n)Cmd '
#                                                                'line: ' +
#        anrobj.packageName,
#        content, re.M)
#    if match:
#        pid = match.group(1)
#        if pid == 'null' or pid == '0':
#            repaired = False
#        else:
#            repaired = True
#            anrobj.pid = pid
#    else:
#        repaired = False
#    return repaired


# event_log_entries_cache = dict()
# event_log_package_cache = dict()


# def getEventLogAnrTime(event_log_entries, packageName):
#    anrTime = dict()
#    # for event_log_path in event_log_path_list:
#    #    try:
#    #        listDir = os.listdir(event_log_path)
#    #    except Exception as ex:
#    #        flymeprint.errorprint(ex)
#    #        return anrTime
#    if packageName in event_log_package_cache:
#        return event_log_package_cache[packageName]
#    if len(event_log_entries_cache) == 0:
#        flymeprint.debug('building cache start')
#        for i in event_log_entries:
#            if i.endswith('.gz'):
#                # src = os.path.join(event_log_path, i)
#                src = i
#                filename = i.rstrip('.gz')
#                content = extractGz(src, filename)
#            else:
#                filename = i
#                content = open(filename, encoding='utf-8').read()
#            am_anr_list = re.findall(
#                '(^\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}.*?am_anr.*)', content,
#                re.M)
#            content = str()
#            if len(am_anr_list) != 0:
#                for j in am_anr_list:
#                    content += j + '\n'
#            event_log_entries_cache[i] = content
#        flymeprint.debug('building cache end')
#    for file_name in event_log_entries_cache.keys():
#        temp_anr_time = get_anr_time_event_log(
#            event_log_entries_cache[file_name],
#            packageName)
#        for i in temp_anr_time.keys():
#            anrTime[i] = {'anr_time': temp_anr_time[i]['anr_time'],
#                          'event_log_path': file_name}
#    event_log_package_cache[packageName] = anrTime
#    return anrTime


def get_matched_time_for_anr(traceTime, anrTime, anr_in_time):
    matchedTime = dict()
    matchedTimeList = list()
    for i in anrTime.keys():
        for j in traceTime.keys():
            # if anrTime[i] < 1 * 60 * 60 * 1000 and traceTime[j] > 11 * 60 *
            #  60 * 1000:
            #     if (
            #                                         11 * 60 * 60 * 1000 +
            # 59 * 60 *
            #                             1000 +
            #                             59 * 1000 - traceTime[j] + anrTime[
            # i]) < 3 *
            # 1000:
            #         matchedTime.append(
            #             {'anr_time': anrTime[i], 'trace_time': traceTime[j]})
            #         continue
            if traceTime[j] < 1 * 60 * 60 * 1000 and anrTime[
                i]['anr_time'] > 11 * 60 * 60 * 1000:
                if (
                                                    11 * 60 * 60 * 1000 + 59
                                        * 60 *
                                        1000 +
                                        60 * 1000 - anrTime[i]['anr_time'] +
                            traceTime[
                                j]) < 3 * 1000:
                    # matchedTime['anr_time'] = i
                    # matchedTime['trace_time'] = j
                    matchedTimeList.append({'anr_time': i, 'trace_time': j})
                    continue
                    # matchedTime.append(
                    #     {'anr_time': anrTime[i], 'trace_time': traceTime[j]})
                    # continue
            else:
                if (traceTime[j] - anrTime[i]['anr_time'] < 3000 and traceTime[
                    j] - anrTime[
                    i]['anr_time'] >= 0) or (
                                traceTime[j] // 1000 == anrTime[i][
                            'anr_time'] // 1000):
                    # matchedTime.append(
                    #     {'anr_time': anrTime[i], 'trace_time': traceTime[j]})
                    # continue
                    # matchedTime['anr_time'] = i
                    # matchedTime['trace_time'] = j
                    matchedTimeList.append({'anr_time': i, 'trace_time': j})
                    continue

    if len(matchedTimeList) == 0:
        return matchedTime;
    if 'anr_time' not in anr_in_time:
        return matchedTimeList[0]

    index = len(matchedTimeList) - 1
    while anrTime[matchedTimeList[index]['anr_time']]['anr_time'] > anr_in_time[
        'anr_time']:
        matchedTimeList.pop(index)
        index = len(matchedTimeList) - 1
        if (index < 0):
            break
    if len(matchedTimeList) == 0:
        return matchedTime
    matchedTime = matchedTimeList.pop(len(matchedTimeList) - 1)

    if (len(matchedTimeList) > 0):
        for i in matchedTimeList:
            cur_anr_time_count = anrTime[i['anr_time']]['anr_time']
            last_anr_time_count = anrTime[matchedTime['anr_time']]['anr_time']
            anr_in_time_count = anr_in_time['anr_time']
            if (cur_anr_time_count < anr_in_time_count) and (
                        (anr_in_time_count - cur_anr_time_count) < (
                                anr_in_time_count - last_anr_time_count)):
                matchedTime = i
    return matchedTime


# data_anr_entries_cache = dict()


# def parse_data_anr(packageName, anrTime, data_anr_entries, anr_in_time):
#    # anrentries = os.listdir(anrPath)
#    if len(data_anr_entries_cache) == 0:
#        for i in data_anr_entries:
#            entry_content = open(i, encoding='utf-8').read()
#            data_anr_entries_cache[i] = entry_content
#    for file_name in data_anr_entries_cache.keys():
#        traceTime = get_trace_time_for_anr(data_anr_entries_cache[file_name],
#                                           packageName)
#        matchedTime = get_matched_time_for_anr(traceTime, anrTime, anr_in_time)
#        if len(matchedTime) == 0:
#            continue
#        allMain = get_whole_trace_final(matchedTime,
#                                        data_anr_entries_cache[file_name])
#        allMain['anr_trace_file_name'] = file_name
#        if 'event_log_path' in anrTime[matchedTime['anr_time']]:
#            allMain['event_log_path'] = anrTime[matchedTime['anr_time']][
#                'event_log_path']
#        return allMain
#    flymeprint.warning('no data anr time matches')
#    return dict()


# def get_whole_trace_for_anr(content, packageName, matchedTime, anrTime,
#                            data_anr_entries, anr_in_time):
#    if len(anrTime) == 0:
#        return dict()
#    if len(matchedTime) == 0:
#        flymeprint.debug('parse data anr trace')
#        return parse_data_anr(packageName, anrTime, data_anr_entries,
#                              anr_in_time)
#    return get_whole_trace_final(matchedTime, content)


def get_whole_trace_final(matched_time, content):
    if 'trace_time' not in matched_time or 'anr_time' not in matched_time:
        return dict()
    match = re.search(
        '^----- pid ' + '\d+' + ' at \d{4}-\d{2}-\d{2} ' + matched_time[
            'trace_time'] + ' -----' + "((.|\n)*?)" + "----- end " + '\d+' +
        " -----",
        content, re.M)
    if not match:
        return dict()
    whole_trace = dict()
    whole_trace['trace_time'] = matched_time['trace_time']
    whole_trace['anr_time'] = matched_time['anr_time']
    whole_trace['content'] = match.group(1)
    return whole_trace


# def getProcessName(content):
#    match = re.match("^Process: (.*)\s", content)
#    if not match:
#        return "null"
#    return match.group(1)


def get_pname_dropbox(content):
    match = re.search("Package: (.*) v.*\s", content)
    if not match:
        return None
    return match.group(1)


def get_subject_dropbox(content):
    match = re.search("Subject: (.*)\s", content)
    if not match:
        return None
    return match.group(1)


# def get_build(content):
#    match = re.search("Build: (.*)\s", content)
#    if not match:
#        return "null"
#    return match.group(1)


def get_cpu_dropbox(content):
    # match = re.search("Build.*\s*((.|\n)*?)\s*----- pid.", content)
    # match = re.search(
    #    "(\n|\r\n){2}((.|\n)*?(CPU usage from(.|\n)*?)(\r\n|\n){2}?)",
    #    content)
    match = re.search(
        '(^CPU usage from .*?ms to .*?ms ago:(.|\n)*?)(\n{2}|\nnull\n----- '
        'pid )',
        content, re.M)
    if not match:
        return None
    # cpu_usage = match.group(4)
    # match = re.search('((.|\n)*?)null\n-----', cpu_usage)
    # if not match:
    #    return cpu_usage
    return match.group(1)


def get_anr_pid_event_log(content, time, package_name):
    # match = re.search(
    #    "(.|\n)*?----- pid ((\d)*).*(\n|\r\n)Cmd line: " + packageName,
    # content)

    # if not match:
    #    return "null"
    # return match.group(2)
    if not content:
        return None
    match = re.search(
        '^' + time + '.*?am_anr.*?\[\d+,(\d+),'
                     '' + package_name,
        content, re.M)
    if not match:
        return None
    return match.group(1)


def get_am_anr_list(content):
    return get_list_final(content, 'am_anr')


def get_watchdog_list(content):
    return get_list_final(content, 'I watchdog: ')


def get_list_final(content, keyword):
    match_list = re.findall(
        '^\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}.*?' + keyword + '.*', content,
        re.M)
    if not match_list:
        return None
    else:
        return match_list


def get_anr_time_event_log(content, package_name):
    match = re.findall(
        '^\d{2}-\d{2} (\d{2}:\d{2}:\d{2}.\d{3}).*?am_anr.*?' + package_name,
        content, re.M)
    anrTime = dict()
    for i in match:
        match = re.search('^(\d{2}):(\d{2}):(\d{2}).(\d{3})', i, re.M)
        hour = match.group(1)
        minute = match.group(2)
        second = match.group(3)
        minisecond = match.group(4)
        wholeMinisecond = int(minisecond) + int(second) * 1000 + int(
            minute) * 60 * 1000 + int(hour) * \
                                  60 * 60 \
                                  * 1000
        # anrTime[i] = wholeMinisecond
        anrTime[i] = {'anr_time': wholeMinisecond}
    return anrTime


def get_anr_in_time(content, packageName):
    anr_in_time = dict()
    match = re.search(
        '^\d{2}-\d{2} ((\d{2}):(\d{2}):(\d{2}).(\d{3})).*ANR in ' + packageName,
        content, re.M)
    if not match:
        return anr_in_time
    whole_time = match.group(1)
    hour = match.group(2)
    minute = match.group(3)
    second = match.group(4)
    minisecond = match.group(5)
    wholeMinisecond = int(minisecond) + int(second) * 1000 + int(
        minute) * 60 * 1000 + int(hour) * \
                              60 * 60 \
                              * 1000
    anr_in_time['anr_time_str'] = whole_time
    anr_in_time['anr_time'] = wholeMinisecond
    return anr_in_time


def get_trace_time_for_anr(content, package_name):
    traceTime = dict()  # key is string time, value is integer time
    match = re.findall(
        '^----- pid ' + '\d+' + ' at \d*-\d*-\d* (\d{2}:\d{2}:\d{2}) '
                                '-----\nCmd line: ' + package_name,
        content, re.M)
    for i in match:
        match = re.search('(\d{2}):(\d{2}):(\d{2})', i)
        hour = match.group(1)
        minute = match.group(2)
        second = match.group(3)
        wholeMinisecond = int(second) * 1000 + int(minute) * 60 * 1000 + int(
            hour) * 60 * 60 * 1000
        traceTime[i] = wholeMinisecond
    return traceTime


# def getRenderThreadTrace(allMain):
#    match = re.search("^(.|\n)*?(\"RenderThread\" prio=(.|\n)*?)(\n|\r\n){2}?",
#                      allMain, re.M)
#    if not match:
#        return "null"
#    return match.group(2)


# def getBinderTrace(allMain):
#    match = re.findall("^(\"Binder_\d{1,2}\" prio=(.|\n)*?)(\n|\r\n){2}?",
#                       allMain, re.M)
#    if not match:
#        return "null"
#    binderList = list()
#    for i in match:
#        binderList.append(i[0])
#    return tuple(binderList)


def get_blocked_trace(whole_trace_content, thread_name):
    # mainConcernedTrace = dict()
    # match = re.search("^(\"(main)\".*?tid=(\d+).*? (\w*)(.|\n)*?)(\n|\r\n){
    # 2}?",
    #                  allMain, re.M)
    # if not match:
    #    return mainConcernedTrace
    # mainTrace = match.group(1)
    # mainName = match.group(2)
    # mainLocalTid = match.group(3)
    # mainState = match.group(4)
    # mainConcernedTrace[mainLocalTid] = {"trace": mainTrace,
    #                                    "thread_state": mainState,
    #                                    "thread_name": mainName}
    # mainConcernedTrace["__thread_sequece__"] = mainLocalTid
    # lastLocalThreadTid = mainLocalTid
    # while mainConcernedTrace[lastLocalThreadTid]["thread_state"] == 'Blocked':
    #    match = re.search("waiting to lock.*held by thread (\d+)",
    #                      mainConcernedTrace[lastLocalThreadTid]["trace"])
    #    if not match:
    #        return mainConcernedTrace
    #    lockedTid = match.group(1)
    #    mainConcernedTrace[lastLocalThreadTid]["locked_tid"] = lockedTid
    #    match = re.search(
    #        "\"(.*)\" prio=.*tid=" + lockedTid + " (\w*)(.|\n)*?((\n|\r\n){"
    #                                             "2}?)",
    #        allMain)
    #    if not match:
    #        return mainConcernedTrace
    #    threadTrace = match.group(0).rstrip(match.group(4))
    #    threadName = match.group(1)
    #    threadState = match.group(2)
    #    mainConcernedTrace[lockedTid] = {"trace": threadTrace,
    #                                     "thread_state": threadState,
    #                                     'thread_name': threadName}
    #    mainConcernedTrace["__thread_sequece__"].append(lockedTid)
    #    lastLocalThreadTid = lockedTid
    # return mainConcernedTrace
    mainConcernedTrace = dict()
    # match = re.search(
    #    "(\"(" + thread_name + ")\".*?tid=(\d+).*? (\w*)(.|\n)*?)(\n|\r\n){
    # 2}?",
    #    whole_trace_content)
    match = parse_trace(whole_trace_content, thread_name)
    if not match:
        return mainConcernedTrace
    mainTrace = match.group(1)
    mainName = match.group(2)
    mainLocalTid = match.group(3)
    mainState = match.group(4)
    mainConcernedTrace[mainLocalTid] = {"trace": mainTrace,
                                        "thread_state": mainState,
                                        "thread_name": mainName}
    mainConcernedTrace["__thread_sequece__"] = [mainLocalTid]
    lastLocalThreadTid = mainLocalTid
    while mainConcernedTrace[lastLocalThreadTid][
        "thread_state"] == 'Blocked':
        match = re.search("waiting to lock.*held by thread (\d+)",
                          mainConcernedTrace[lastLocalThreadTid]["trace"])
        if not match:
            return mainConcernedTrace
        lockedTid = match.group(1)

        mainConcernedTrace[lastLocalThreadTid]["locked_tid"] = lockedTid

        match = re.search(
            "\"(.*)\" prio=.*tid=" + lockedTid + " (\w*)(.|\n)*?(("
                                                 "\n|\r\n){2}?)",
            whole_trace_content)
        if not match:
            return mainConcernedTrace
        threadTrace = match.group(0).rstrip(match.group(4))
        threadName = match.group(1)
        threadState = match.group(2)
        if lockedTid in mainConcernedTrace:
            break
        mainConcernedTrace[lockedTid] = {"trace": threadTrace,
                                         "thread_state": threadState,
                                         'thread_name': threadName}
        mainConcernedTrace["__thread_sequece__"].append(lockedTid)
        lastLocalThreadTid = lockedTid

    return mainConcernedTrace


def get_blocked_trace_str(whole_trace, thread_name):
    trace_dict = get_blocked_trace(whole_trace, thread_name)
    trace = str()
    for i in trace_dict['__thread_sequece__']:
        trace += (trace_dict[i]['trace'] + '\n')
    return trace


def get_thread_state(whole_trace, thread_name):
    match = parse_trace(whole_trace, thread_name)
    if match:
        return match.group(4)
    else:
        return None


def parse_trace(whole_trace, thread_name):
    return re.search(
        "^(\"(" + thread_name + ")\".*?tid=(\d+).*? (\w*)(.|\n)*?)(\n|\r\n){"
                                "2}?",
        whole_trace, re.M)


def get_trace(whole_trace, thread_name):
    trace_dict = dict()
    # if 'content' not in whole_trace:
    #    return trace_dict
    match = parse_trace(whole_trace, thread_name)
    if not match:
        return trace_dict
    trace_dict['trace'] = match.group(1)
    trace_dict['thread_state'] = match.group(4)
    return trace_dict


# def anrobjtofile(anrObj, fullName):
#    newFile = open(fullName, 'w', encoding='utf-8')
#    mainConcernedTrace = ''
#    for i in anrObj.mainConcernedTrace["__thread_sequece__"]:
#        mainConcernedTrace += anrObj.mainConcernedTrace[i]["trace"] + '\n'
#    outputMessage = 'package name:\n' + anrObj.packageName + '\n\n' + 'anr ' \
#
# 'time:\n' \
#                    + \
#                    anrObj.anrTime + '\n\n' + 'trace time:\n' + \
#                    str(anrObj.traceTime) \
#                    + '\n\n' + 'anr reason:\n' + \
#                    anrObj.anrReason + '\n\n' + 'cpu usage:\n' + \
#                    anrObj.cpuUsage \
#                    + '\n\n' + \
#                    "main concerned stack trace:\n" + mainConcernedTrace + \
#                    '\n\n'
#    newFile.write(outputMessage)
#    newFile.close()

def is_fname_match(file_name, pattern):
    match = re.match(pattern, file_name)
    if match:
        return True
    else:
        return False


def extract_db(db_file):
    flymeprint.debug('extract db...')
    win_extracter = 'com\\flyme\\autoanalyser\\bin\\windows\\aee_extract.exe'
    un_extracter = 'com/flyme/autoanalyser/bin/unix/aee_extract'
    dnull = open(os.devnull, 'w')
    if os.name == 'nt':  # windows
        subprocess.call([win_extracter, db_file], stdout=dnull)
    else:
        subprocess.call([un_extracter, db_file], stdout=dnull)


def get_watchdog_time_event_log(content):  # content is matched watchdog content
    match = re.search('(^\d{2}-\d{2} (\d{2}):(\d{2}):(\d{2}))\.(\d{3})',
                      content, re.M)
    if not match:
        return None
    else:
        return match.group(1)


def get_wd_ss_pid(content):  # content is matched watchdog content
    match = re.search(
        '^\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}.*? {1,2}(\d+) {1,2}\d+ I '
        'watchdog: ('
        'Blocked|surfaceflinger  hang\.)',
        content, re.M)
    if not match:
        return None
    else:
        return match.group(1)


def get_watchdog_hlist_event_log(content):
    match = re.findall(
        '(Blocked in handler on (?P<handler_name>.*?) \(('
        '?P<thread_name>.*?)\))',
        content)
    if match:
        return match
    else:
        return None


def get_watchdog_mlist_event_log(content):
    match = re.findall(
        '(Blocked in monitor (?P<class_name>.*?) on ('
        '?P<checker_name>.*?) '
        '\((?P<thread_name>.*?)\))',
        content)
    if match:
        return match
    else:
        return None


def get_trace_time_pid_for_wd(content):
    return get_trace_time_pid(content, '\d+', 'system_server')


def get_trace_time_pid(content, pid, process_name):
    match = re.findall(
        '^----- pid ' + '(' + pid + ')' + ' at (\d{4}-\d{2}-\d{2} \d{2}:\d{'
                                          '2}:\d{2}) '
                                          '-----\nCmd line: ' + process_name
        # + '\n(.|\n)*?----- end ' + pid + ' -----',
        , content, re.M)
    if match:
        return match
    else:
        return None


def is_trace_blocked_in_binder(content):  # content is single thread trace
    # content
    match = re.findall('^  native: #\d{2} pc \w+  .*', content, re.M)
    if not match or len(match) < 3:
        return False
    if match[2].find('talkWithDriverEb') == -1:
        return False
    return True


def parse_db_pt_by_pid_tname(content, pid, thread_name):
    if thread_name == 'main':
        match = re.search(
            '^u:r:system_server:s0 +system +(?P<pid>' + pid + ') +(?P<ppid>'
            + '\d+' +
            ').*? +' +
            '(?P<name>' + 'system_server' + ')$', content, re.M)
    else:
        match = re.search(
            '^u:r:system_server:s0 +system +(?P<pid>\d+) +(?P<ppid>' + pid +
            ').*?' +
            '(?P<name>' + thread_name + ')$', content, re.M)
    if not match:
        return None
    return match.groupdict()


def parse_db_bi_by_pid_tid(content, pid, tid):
    match = re.search(
        '^    outgoing transaction \d+: \w+ from ' + pid + ':' + tid + ' to ('
                                                                       '?P<pid>\d+):(?P<tid>\d+)',
        content, re.M)
    if not match:
        return None
    return match.groupdict()


def parse_db_pt_by_pid_tid(content, pid, tid):
    match_t = re.search(
        '^(\w|:|_)+ +\w+ +' + tid + ' +' + pid + '.* +(?P<thread_name>('
                                                 '\w|:|_)+)$',
        content, re.M)
    if not match_t:
        return None
    match_t = match_t.groupdict()
    match_p = re.search(
        '^(\w|:|_)+ +\w+ +' + pid + ' +' + '\d+' + '.* +('
                                                   '?P<process_name>('
                                                   '\w|:|_|/)+)$',
        content, re.M)
    if not match_p:
        return None
    match_p = match_p.groupdict()
    match_t['process_name'] = match_p['process_name']
    match_t['pid'] = pid
    return match_t


def get_ss_pid_by_swtdir(dir):
    swt_dir = os.path.dirname(dir)
    for file in os.listdir(swt_dir):
        if file == 'ZZ_INTERNAL':
            content = open(os.path.join(swt_dir, file), 'r',
                           encoding='utf-8').read()
            match = re.search('^SWT,(\d+),', content)
            if not match:
                return None
            return match.group(1)
    return None


def is_swt_dir(dir):
    return is_fname_match(dir, 'db\.fatal\.\d{2}\.SWT\.dbg\.DEC')


def find_min_time(target_time_str, tl_str_to_be_compared, is_later):
    target_time_struct = datetime.strptime(target_time_str, '%Y-%m-%d %H:%M:%S')
    count = target_time_struct.timestamp()
    interval = sys.maxsize
    time_str = None
    for i in tl_str_to_be_compared:
        time_struct = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
        temp = abs(count - time_struct.timestamp())
        if temp < interval:
            interval = temp
            time_str = i
    return time_str


def get_whole_trace_str(content, package_name, matched_time_str):
    match = re.search(
        '(^----- pid (?P<pid>\d+) at ' + matched_time_str + ' -----\nCmd line: '
        + package_name + '\n('
                         '.|\n)*?----- end (?P=pid) '
                         '-----)',
        content, re.M)
    if not match:
        return None
    return match.group(1)


def get_whole_trace_str_pid_process_time(content, pid, time, process):
    match = re.search(
        '(^----- pid ' + pid + ' at ' + time + ' -----\nCmd line: '
        + process + '\n('
                    '.|\n)*?----- end ' + pid + ' '
                                                '-----)',
        content, re.M)
    if not match:
        return None
    return match.group(1)
