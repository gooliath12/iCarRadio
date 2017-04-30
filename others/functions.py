def get_tod():
    """
    Get time of day,
    Return time interval.
    """
    import datetime
    t1 = 16200  # 4:30
    t2 = 34200  # 8:30
    t3 = 63000  # 17:30
    t4 = 73800  # 20:30
    t5 = 82800  # 23:00
    now = datetime.datetime.now()
    bod = now.replace(hour=0, minute=0, second=0, microsecond=0)
    t = (now - bod).total_seconds()
    
    if t > t1 and t <= t2:  # 4:30 -- 9:30
        return 'morning'
    if t > t2 and t <= t3:  # 9:30 -- 17:30
        return 'midday'
    if t > t3 and t <= t4:  # 17:30 -- 20:30
        return 'off work'
    if t > t4 and t <= t5:  # 20:30 -- 23:00
        return 'night'
    return 'midnight'  # 23:00 -- 4:30

