import subprocess
import os
import datetime
import warnings


def get_duration_ffmpeg(video_file):
    """ Returns the video duration in seconds using ffmpeg.

    :param str video_file: Path to the video file.
    :return float: Video duration.

    - REQUIRES ffmpeg!
    """
    # Get the video duration in seconds, see: https://trac.ffmpeg.org/wiki/FFprobeTips#Streamduration
    duration = float(subprocess.check_output(
        'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ' + video_file))
    return duration


def get_start_end_time(video_file):
    """ Returns the start time of the video.

    :param str video_file: Path to the video file, must follow the naming format below.
    :return list: (datetime.datetime) Video start time and video end time, both with an arbitrary day.

    - The format for the video file path is: '[directory]_[Camera]_[Location]_[#]_[HMS]_[ms], where H is the hour,
    M is the minute, S is the second, and ms is the time in milliseconds. This is the time of the end of the video.
    - Since no information is given about the day of the video, it is assumed to be epoch.
    """
    _, file_name = os.path.split(video_file)
    split_name = file_name.split('_')
    time_hms = split_name[-2]
    time_milli, _ = split_name[-1].split('.')
    time_micro = time_milli + '000'
    end_time = datetime.datetime.strptime(time_hms + time_micro, '%H%M%S%f')
    duration = datetime.timedelta(seconds=get_duration_ffmpeg(video_file))
    start_time = end_time - duration
    return [start_time, end_time]


def check_times_within_video_time(start, end, times):
    """ Checks the bounds of the video times with the provided time list.

    :param datetime.datetime start: Video start time.
    :param datetime.datetime end: Video end time.
    :param list times: (datetime.datetime) Times to check in ascending chronological order.
    :return bool: True if the times are valid, False otherwise.
    """
    valid_times = True
    start_check = start - times[0]
    end_check = end - times[-1]
    if start_check.total_seconds() > 0. or end_check.total_seconds() < 0.:
        warnings.warn('The provided video and times are incompatible!')
        valid_times = False
    return valid_times


def dion7_times_to_video_times(video_file, times):
    """ Returns the times in seconds in the video that correspond to the given Dion7 times.

    :param str video_file: Path to the video file.
    :param list times: (datetime.datetime) Times of interest from Dion7 recordings in ascending chronological order.
    :return list: (float) Time in seconds since the start of the video to each Dion7 recording provided.

    - It is assumed that the video is recorded on the same date (Day, Month, Year) as the provided times.
    - It is assumed that the video only spans a signle day.
    """
    # Get the video start time (assumed same date as the provided times)
    vst, vet = get_start_end_time(video_file)
    t1 = times[0]
    video_start = vst.replace(year=t1.year, month=t1.month, day=t1.day)
    video_end = vet.replace(year=t1.year, month=t1.month, day=t1.day)
    check_times_within_video_time(video_start, video_end, times)
    # Calculate the elapsed time in seconds
    video_times = []
    for t in times:
        t_delta = t - video_start
        video_times.append(t_delta.total_seconds())
    return video_times
